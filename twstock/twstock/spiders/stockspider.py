# -*- coding: utf-8 -*-
import scrapy
import pandas as pd
from time import gmtime, strftime
from .parse import format_time_at
from .stocks import get_co_ids


class StockSpider(scrapy.Spider):
    name = 'stock'
    allowed_domains = ['mops.twse.com.tw']
    start_urls = ['https://mops.twse.com.tw/mops/web/t146sb05']

    # https://www.youtube.com/watch?v=Lo3aswJ7lzw
    # https://doc.scrapy.org/en/latest/topics/request-response.html
    def parse(self, response):
        for co_id in get_co_ids():
            fordata = {
                'co_id': co_id,
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
            }
            # https://doc.scrapy.org/en/latest/topics/request-response.html
            request = scrapy.FormRequest(
                url='https://mops.twse.com.tw/mops/web/ajax_t146sb05',
                formdata=fordata,
                callback=self.after_submit,
                cb_kwargs=dict(co_id=co_id)
            )


            yield request

    def after_submit(self, response, co_id):
        # self.write_page(response) # For debug

        fordata = {
            'co_id': co_id,
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
            'isgood': '1',
            'year': '108',
        }
        # 最近五年股利分派情形
        return scrapy.FormRequest(
            url='https://mops.twse.com.tw/mops/web/ajax_t05st09_2',
            formdata=fordata,
            callback=self.handle_eps,
            cb_kwargs=dict(co_id=co_id)
        )

    def write_page(self, response):
        page = response.url.split("/")[-1]
        filename = '%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log("Writ to file %s" % filename)

    def handle_eps(self, response, co_id):
        # self.write_page(response) # For debug
        formatted_body = response.body.decode("utf-8").replace("TABLE", "table")
        formatted_body = formatted_body.replace("TH", "th")
        formatted_body = formatted_body.replace("TR", "tr")
        formatted_body = formatted_body.replace("TD", "td")

        data = pd.read_html(formatted_body, skiprows=0, encoding='big5')
        df = data[2]

        # df.to_csv(co_id + "-dividend-full.csv", index=False) # For debug

        meta_data = {
            "1. Information": "Time Series for Dividend",
            "2. Symbol": "TW:" + co_id,
            "3. Last Refreshed": strftime("%Y-%m-%d %H:%M:%S", gmtime()),
            "4. Time Zone": 'UTC',
        }

        rows = []
        for index, row in df.iterrows():
            time_at = format_time_at(row[df.columns[1]])
            dividend = row[df.columns[10]]
            rows.append([time_at, dividend])

        dividend_df = pd.DataFrame(rows, columns=['time', 'dividend'])
        dividend_path = co_id + "-dividend.csv"
        dividend_df.to_csv(co_id + "-dividend.csv", index=False)

        yield {
            "meta_data": meta_data,
            "dividend": dividend_path,
        }
