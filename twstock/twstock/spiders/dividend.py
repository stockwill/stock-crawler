# -*- coding: utf-8 -*-
import scrapy
import pandas as pd
from .parse import format_time_at
from .utils import write_page_to, get_meta_data
from .stocks import get_co_ids

debug = False
output_dir = "dividend/"


class DividendSpider(scrapy.Spider):
    name = 'dividend'
    allowed_domains = ['mops.twse.com.tw/mops/web/t05st09_2']

    def parse(self, response):
        pass

    def start_requests(self):
        for co_id in get_co_ids():
            formdata = {
                'encodeURIComponent': '1',
                'step': '1',
                'firstin': '1',
                'off': '1',
                'keyword4': '',
                'code1': '',
                'TYPEK2': '',
                'checkbtn': '',
                'queryName': 'co_id',
                'inpuType': 'co_id',
                'TYPEK': 'all',
                'isnew': 'false',
                'co_id': co_id,
                'date1': '100',
                'date2': '108',
                'qryType': '1',
            }

            yield scrapy.FormRequest(
                url='https://mops.twse.com.tw/mops/web/ajax_t05st09_2',
                formdata=formdata,
                callback=self.parse_dividend,
                cb_kwargs=dict(co_id=co_id)
            )

    def parse_dividend(self, response, co_id):
        if debug:
            write_page_to(response, output_dir)

        try:
            data = pd.read_html(response.body, skiprows=0, encoding='utf8')
        except ValueError:
            self.logger.error('No table found')
            return

        df = data[2]
        if debug:
            df.to_csv(output_dir + co_id + "-dividend-full.csv", index=False)

        if debug:
            print('index: ', df.index)
            print('column: ', df.columns)
        df0 = df['股利所屬年(季)度']
        df1 = df['董事會決議(擬議)股利分派日']
        df2 = df['股東配發內容']['盈餘分配之現金股利(元/股)']
        df3 = df['股東配發內容']['盈餘轉增資配股(元/股)']
        if debug:
            print('sample 0: ', df0)
            print('sample 1: ', df1)
            print('sample 2: ', df2)
            print('sample 3: ', df3)
        result = pd.concat([df0, df1, df2, df3], axis=1)
        if debug:
            print('result: ', result)

        wanted = [{'name': 'time', 'transform': format_time_at},
                  {'name': 'at', 'transform': lambda x: x},
                  {'name': 'cash', 'transform': lambda x: x},
                  {'name': 'stock', 'transform': lambda x: x}]

        rows = []
        for index, row in result.iterrows():
            vals = []

            for pos_col, col in enumerate(wanted):
                data = row[result.columns[pos_col]]
                vals.append(wanted[pos_col]['transform'](data))
            rows.append(vals)

        columns = []
        for w in wanted:
            columns.append(w['name'])

        dividend_df = pd.DataFrame(rows, columns=columns)
        dividend_path = output_dir + co_id + "-dividend.csv"
        dividend_df.to_csv(dividend_path, index=False)

        yield {
            "meta_data": get_meta_data("Time Series for Dividend", co_id),
            "dividend": dividend_path,
        }
