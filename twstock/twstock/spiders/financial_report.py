# -*- coding: utf-8 -*-
import scrapy
import pandas as pd
from urllib import parse
from .utils import write_page, get_meta_data
from .stocks import get_co_ids

debug = False
output_dir = 'eps/'


class Done(Exception):
    pass


# https://mops.twse.com.tw/server-java/t164sb01?step=1&CO_ID=2330&SYEAR=2019&SSEASON=2&REPORT_ID=C
class FinancialReportSpider(scrapy.Spider):
    name = 'financial_report'
    allowed_domains = ['mops.twse.com.tw']

    def start_requests(self):
        for co_id in get_co_ids():
            yield self.create_request(co_id, 2019, 2, [], True)  # original
            # yield self.create_request(co_id, 2018, 3, [])
            # yield self.create_request(co_id, 2013, 1, [])

    def create_request(self, co_id, year, season, rows, follow):
        return self.create_request_internal(co_id, year, season, rows, follow, 'C')

    def create_request_internal(self, co_id, year, season, rows, follow, report_id):
        params = {
            'step': 1,
            'CO_ID': co_id,
            'SYEAR': year,
            'SSEASON': season,
            'REPORT_ID': report_id,
        }
        url = 'https://mops.twse.com.tw/server-java/t164sb01?' + parse.urlencode(params)
        # print('url: ', url)
        return scrapy.Request(url=url,
                              callback=self.response_handler,
                              cb_kwargs=dict(co_id=co_id, year=year, season=season, rows=rows, follow=follow,
                                             report_id=report_id))

    def response_handler(self, response, co_id, year, season, rows, follow, report_id):
        try:
            # I just try to flatten the alternative request solutions ...
            try:
                new_rows = self.parse_new_ifrs(response, co_id, year, season, rows)
                raise Done
            except ValueError:
                pass
            try:
                new_rows = self.parse_older_ifrs(response, co_id, year, season, rows)
                raise Done
            except ValueError:
                pass

            if report_id == 'C':
                yield self.create_request_internal(co_id, year, season, rows, follow, 'A')
            else:
                follow = False
                raise Done
            # follow = False
            # raise Done

            # eps_path = self.write_eps_file(rows, co_id)
            # yield self.generate(co_id, eps_path)
            # return

        except Done:
            if follow:
                next_year, next_season = self.get_previous_season(year, season)
                yield self.create_request(co_id, next_year, next_season, new_rows, follow)
            else:
                eps_path = self.write_eps_file(rows, co_id)
                yield self.generate(co_id, eps_path)

    # TODO: 1240 no EPS
    # TODO: 1235 EPS ()
    # TODO: https://mops.twse.com.tw/server-java/t164sb01?step=1&CO_ID=1213&SYEAR=2019&SSEASON=2&REPORT_ID=C
    # https://mops.twse.com.tw/server-java/t164sb01?step=1&CO_ID=2330&SYEAR=2018&SSEASON=2&REPORT_ID=C
    # https://mops.twse.com.tw/server-java/t164sb01?step=1&CO_ID=2330&SYEAR=2012&SSEASON=2&REPORT_ID=C
    def parse_older_ifrs(self, response, co_id, year, season, rows):
        eps_index_heading = b'\xef\xbf\xbd@\xef\xbf\xbd@ \xef\xbf\xbd\xf2\xa5\xbb\xa8C\xef\xbf\xbd\xd1\xac\xd5\xbel\xef\xbf\xbdX\xef\xbf\xbdp'.decode(
            'utf-8')

        if debug:
            write_page(response)
        try:
            # FIXME: We can only decode html using utf8 but the representation of characters would go unrecognizable so
            #  we need to use binary representation for it
            data = pd.read_html(response.body, skiprows=0, encoding='utf8')
        except ValueError:
            self.logger.warning('No table found')
            raise ValueError
            # eps_path = self.write_eps_file(rows, co_id)
            # yield self.generate(co_id, eps_path)
            # return

        if len(data) < 3:
            # eps_path = self.write_eps_file(rows, co_id)
            # yield self.generate(co_id, eps_path)
            self.logger.warning('No data found')
            raise ValueError

        df = data[2]
        if debug:
            df.to_csv(output_dir + co_id + "-financial-full-" + str(year) + "Q" + str(season) + ".csv", index=False)

        vals = ["%d Q%d" % (year, season)]
        if season == 4:
            vals = ["%d" % year]
        found = False
        for index, row in df.iterrows():
            # self.logger.debug('row[%d]: %s' % (index, str(row[df.columns[0]])))
            if row[df.columns[0]] == eps_index_heading:
                eps = row[df.columns[1]]
                found = True
                break

        if not found:
            self.logger.warning('No eps found')
            # eps_path = self.write_eps_file(rows, co_id)
            # yield self.generate(co_id, eps_path)
            # return
            raise ValueError

        vals.append(eps)
        print('vals: ', vals)
        rows.append(vals)

        return rows
        # if follow:
        #    next_year, next_season = self.get_previous_season(year, season)
        #    yield self.create_request(co_id, next_year, next_season, rows)
        # else:
        #    eps_path = self.write_eps_file(rows, co_id)
        #    yield self.generate(co_id, eps_path)

    def parse_new_ifrs(self, response, co_id, year, season, rows):
        if debug:
            write_page(response)

        try:
            data = pd.read_html(response.body, skiprows=0, encoding='UTF-8')
        except ValueError:
            self.logger.warning('No table found')
            # eps_path = self.write_eps_file(rows, co_id)
            # yield self.generate(co_id, eps_path)
            # return
            raise ValueError
        if len(data) < 2:
            raise ValueError

        df = data[1]
        if debug:
            df.to_csv(output_dir + co_id + "-financial-full.csv", index=False)

        total_basic_earnings_per_share_s = b'\xef\xbf\xbd@\xef\xbf\xbd\xf2\xa5\xbb\xa8C\xef\xbf\xbd\xd1\xac\xd5\xbel\xef\xbf\xbdX\xef\xbf\xbdp\xef\xbf\xbd@Total basic earnings per share'.decode(
            'utf-8')
        total_primary_earnings_per_share_s = b'\xef\xbf\xbd@\xef\xbf\xbd\xf2\xa5\xbb\xa8C\xef\xbf\xbd\xd1\xac\xd5\xbel\xef\xbf\xbdX\xef\xbf\xbdp\xef\xbf\xbd@Total primary earnings per share'.decode(
            'utf-8')
        vals = ["%d Q%d" % (year, season)]
        found = False
        for index, row in df.iterrows():
            # print('row: ', row[df.columns[1]], " data: ", row[df.columns[2]], " row in utf-8: ", row[df.columns[1]].encode('utf-8'))
            if row[df.columns[1]] == total_basic_earnings_per_share_s or row[
                df.columns[1]] == total_primary_earnings_per_share_s:
                eps = row[df.columns[2]]
                vals.append(eps)
                found = True
                break

        # FIXME: Should not happen
        if not found:
            # self.logger.critical('No eps found - but this should not happen')
            # return
            raise ValueError

        print('vals: ', vals)

        next_year, next_season = self.get_previous_season(year, season)
        rows.append(vals)
        # if follow:
        #    yield self.create_request(co_id, next_year, next_season, rows)
        return rows

    def parse(self, response):
        pass

    @staticmethod
    def get_previous_season(year, season):
        if season == 1:
            return year - 1, 4
        return year, season - 1

    @staticmethod
    def write_eps_file(rows, co_id):
        eps_df = pd.DataFrame(rows, columns=["time", "eps"])
        eps_path = output_dir + co_id + "-eps.csv"
        eps_df.to_csv(eps_path, index=False)

        return eps_path

    @staticmethod
    def generate(co_id, eps_path):
        return {'meta_data': get_meta_data("Time Series for EPS", co_id), 'eps': eps_path}
