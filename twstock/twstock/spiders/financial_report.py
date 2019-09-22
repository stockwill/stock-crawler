# -*- coding: utf-8 -*-
import scrapy
import pandas as pd
from urllib import parse
from .utils import write_page, get_data_dir, get_meta_data
from .stocks import get_co_ids
from .parse import reformat_html_for_table

debug = False


# https://mops.twse.com.tw/server-java/t164sb01?step=1&CO_ID=2330&SYEAR=2019&SSEASON=2&REPORT_ID=C
class FinancialReportSpider(scrapy.Spider):
    name = 'financial_report'
    allowed_domains = ['mops.twse.com.tw']

    def start_requests(self):
        for co_id in get_co_ids():
            yield self.create_request(co_id, 2019, 2, [])
            # yield self.create_request(co_id, 2013, 1, [])

    def create_request(self, co_id, year, season, rows):
        parse_method = self.parse_new_ifrs if year >= 2019 else self.parse_older_ifrs
        params = {
            'step': 1,
            'CO_ID': co_id,
            'SYEAR': year,
            'SSEASON': season,
            'REPORT_ID': 'C'
        }
        url = 'https://mops.twse.com.tw/server-java/t164sb01?' + parse.urlencode(params)
        # print('url: ', url)
        return scrapy.Request(url=url,
                              callback=parse_method,
                              cb_kwargs=dict(co_id=co_id, year=year, season=season, rows=rows))

    # https://mops.twse.com.tw/server-java/t164sb01?step=1&CO_ID=2330&SYEAR=2018&SSEASON=2&REPORT_ID=C
    # https://mops.twse.com.tw/server-java/t164sb01?step=1&CO_ID=2330&SYEAR=2012&SSEASON=2&REPORT_ID=C
    def parse_older_ifrs(self, response, co_id, year, season, rows):
        follow = True
        eps_index_heading = b'\xef\xbf\xbd@\xef\xbf\xbd@ \xef\xbf\xbd\xf2\xa5\xbb\xa8C\xef\xbf\xbd\xd1\xac\xd5\xbel\xef\xbf\xbdX\xef\xbf\xbdp'.decode(
            'utf-8')

        if debug:
            write_page(response)
        try:
            # FIXME: We can only decode html using utf8 but the representation of characters would go unrecognizable so
            #  we need to use binary reqpresentation for it
            data = pd.read_html(response.body, skiprows=0, encoding='utf8')
        except ValueError:
            self.logger.warning('No table found')
            eps_path = self.write_eps_file(rows, co_id)
            yield self.generate(co_id, eps_path)
            return

        if len(data) < 3:
            eps_path = self.write_eps_file(rows, co_id)
            yield self.generate(co_id, eps_path)
            self.logger.warning('No data found')

            return

        df = data[2]
        if debug:
            df.to_csv(get_data_dir() + co_id + "-financial-full-" + str(year) + "Q" + str(season) + ".csv", index=False)

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
            eps_path = self.write_eps_file(rows, co_id)
            yield self.generate(co_id, eps_path)
            return

        vals.append(eps)
        print('vals: ', vals)
        rows.append(vals)

        if follow:
            next_year, next_season = self.get_previous_season(year, season)
            yield self.create_request(co_id, next_year, next_season, rows)
        else:
            eps_path = self.write_eps_file(rows, co_id)
            yield self.generate(co_id, eps_path)

    def parse_new_ifrs(self, response, co_id, year, season, rows):
        if debug:
            write_page(response)

        try:
            data = pd.read_html(response.body, skiprows=0, encoding='UTF-8')
        except ValueError:
            self.logger.warning('No table found')
            eps_path = self.write_eps_file(rows, co_id)
            yield self.generate(co_id, eps_path)
            return

        df = data[1]
        if debug:
            df.to_csv(get_data_dir() + co_id + "-financial-full.csv", index=False)

        vals = ["%d Q%d" % (year, season)]
        found = False
        for index, row in df.iterrows():
            if row[df.columns[0]] == 9750.0:
                eps = row[df.columns[2]]
                vals.append(eps)
                found = True
                break

        # FIXME: Should not happen
        if not found:
            self.logger.critical('No eps found - but this should not happen')
            return

        print('vals: ', vals)

        next_year, next_season = self.get_previous_season(year, season)
        rows.append(vals)
        yield self.create_request(co_id, next_year, next_season, rows)

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
        eps_path = get_data_dir() + co_id + "-eps.csv"
        eps_df.to_csv(eps_path, index=False)

        return eps_path

    @staticmethod
    def generate(co_id, eps_path):
        return {'meta_data': get_meta_data("Time Series for EPS", "TW:" + co_id), 'eps': eps_path}
