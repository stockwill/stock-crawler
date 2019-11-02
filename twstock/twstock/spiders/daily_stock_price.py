# -*- coding: utf-8 -*-
import scrapy
import pandas as pd
import datetime
from .stocks import get_co_ids


# https://stackoverflow.com/questions/22604564/create-pandas-dataframe-from-a-string
from io import StringIO

debug = False


# https://en.wikipedia.org/wiki/Candlestick_chart
# https://www.twse.com.tw/zh/page/trading/exchange/STOCK_DAY.html
class DailyStockPriceItem(scrapy.Item):
    date = scrapy.Field()  # 日期
    total_trade_stocks = scrapy.Field()  # 成交股數
    total_trade_dollar = scrapy.Field()  # 成交金額
    open = scrapy.Field()  # 開盤價
    high = scrapy.Field()  # 最高價
    low = scrapy.Field()  # 最低價
    close = scrapy.Field()  # 收盤價
    difference_percentage = scrapy.Field()  # 漲跌價差
    total_trade_count = scrapy.Field()  # 成交筆數
    co_id = scrapy.Field()


class DailyStockPriceSpider(scrapy.Spider):
    name = 'daily_stock_price'
    allowed_domains = ['www.twse.com.tw']
    start_urls = ['http://www.twse.com.tw/']

    custom_settings = {
        'ITEM_PIPELINES': {
            'twstock.exporters.csv_exporter.CSVExportPipeline': 1,
        }
    }

    # Exporter settings
    output_dir = "price/"
    filename_suffix = "-daily-stock-price"

    def start_requests(self):
        for co_id in get_co_ids():

            now = datetime.datetime.now()
            year, month = now.year, now.month
            # year, month = 1988, 1
            # date = "{0:d}{1:d}01".format(now.year, now.month)
            # date = '20191001'
            yield self.create_request_internal(co_id, year, month)

    def create_request_internal(self, co_id, year, month):
        date = "{0:d}{1:02d}01".format(year, month)

        url = 'https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=csv&date=' + date + '&stockNo=' + str(1101)
        return scrapy.http.Request(
            url,
            callback=self.parse_csv,
            cb_kwargs=dict(co_id=co_id,
                           year=year,
                           month=month))

    def parse(self, response):
        pass

    def parse_csv(self, response, co_id, year, month):
        content = str(response.body)
        # print("content before: ", content)
        contents = content.split("\\r\\n")
        # for line in contents:
        #    print("line: ", line)
        # print("contents: ", contents)
        for i in range(len(contents)):
            contents[i] = contents[i].strip(",")
        content_stripped = "\n".join(contents[1:])  # We remove first row

        s = StringIO(content_stripped)
        df = pd.read_csv(s)
        if debug:
            print(df.columns)

        # date_index = b'\xa4\xe9\xb4\xc1'.decode('big5') # you can see it in Chinese
        wants = [{'index': b'\\xa4\\xe9\\xb4\\xc1', 'pos': -1, 'name': 'date'},
                 {'index': b'\\xa6\\xa8\\xa5\\xe6\\xaa\\xd1\\xbc\\xc6', 'pos': -1, 'name': 'total_trade_stocks'},
                 {'index': b'\\xa6\\xa8\\xa5\\xe6\\xaa\\xf7\\xc3B', 'pos': -1, 'name': 'total_trade_dollar'},
                 {'index': b'\\xb6}\\xbdL\\xbb\\xf9', 'pos': -1, 'name': 'open'},
                 {'index': b'\\xb3\\xcc\\xb0\\xaa\\xbb\\xf9', 'pos': -1, 'name': 'high'},
                 {'index': b'\\xb3\\xcc\\xa7C\\xbb\\xf9', 'pos': -1, 'name': 'low'},
                 {'index': b'\\xa6\\xac\\xbdL\\xbb\\xf9', 'pos': -1, 'name': 'close'},
                 {'index': b'\\xba\\xa6\\xb6^\\xbb\\xf9\\xaet', 'pos': -1, 'name': 'difference_percentage'},
                 {'index': b'\\xa6\\xa8\\xa5\\xe6\\xb5\\xa7\\xbc\\xc6', 'pos': -1, 'name': 'total_trade_count'}
                 ]
        for i in range(len(df.columns)):
            now = bytes(df.columns[i], encoding='utf-8')
            for w in wants:
                if now == w['index']:
                    w['pos'] = i

        for w in wants:
            if w['pos'] == -1:
                self.logger.warning('Fail to find pos')
                return

        for i in range(len(df.index)):
            val = {'co_id': co_id}
            ok = True
            for w in wants:
                if w['pos'] == -1:
                    continue

                # https://pandas.pydata.org/pandas-docs/stable/user_guide/missing_data.html
                if pd.isna(df.iloc[i, w['pos']]):
                    ok = False
                    break
                val[w['name']] = df.iloc[i, w['pos']]
            if ok:
                # print('val: ', val)
                yield self.get_daily_stock_price_item(val)

        next_year, next_month = self.get_previous_year_month(year, month)
        yield self.create_request_internal(co_id, next_year, next_month)

    @staticmethod
    def get_previous_year_month(year, month):
        if month == 1:
            return year - 1, 12
        return year, month - 1

    @staticmethod
    def get_daily_stock_price_item(d):
        item = DailyStockPriceItem()
        for k, v in d.items():
            item[k] = v
        return item
