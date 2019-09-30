# -*- coding: utf-8 -*-
import scrapy
import pandas as pd
from .parse import format_time_at
from .utils import write_page_to
from .stocks import get_co_ids

debug = False


class DividendItem(scrapy.Item):
    time = scrapy.Field()
    at = scrapy.Field()
    cash = scrapy.Field()
    stock = scrapy.Field()
    co_id = scrapy.Field()


class DividendSpider(scrapy.Spider):
    name = 'dividend'
    allowed_domains = ['mops.twse.com.tw/mops/web/t05st09_2']
    custom_settings = {
        'ITEM_PIPELINES': {
            'twstock.exporters.csv_exporter.CSVExportPipeline': 1,
        }
    }

    # Exporter settings
    output_dir = "dividend/"
    filename_suffix = "-dividend"

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
            write_page_to(response, self.output_dir)

        try:
            data = pd.read_html(response.body, skiprows=0, encoding='utf8')
        except ValueError:
            self.logger.error('No table found')
            return

        df = data[2]
        if debug:
            df.to_csv(self.output_dir + co_id + "-dividend-full.csv", index=False)

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

        for index, row in result.iterrows():
            val = {'co_id': co_id}
            for pos_col, col in enumerate(wanted):
                data = row[result.columns[pos_col]]
                name = wanted[pos_col]['name']
                val[name] = wanted[pos_col]['transform'](data)
            yield self.get_dividend_item(val)

    @staticmethod
    def get_dividend_item(d):
        item = DividendItem()
        for k, v in d.items():
            item[k] = v

        return item
