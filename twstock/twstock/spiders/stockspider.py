# -*- coding: utf-8 -*-
import scrapy
import pandas as pd

class StockSpider(scrapy.Spider):
    name = 'stock'
    allowed_domains = ['mops.twse.com.tw']
    start_urls = ['https://mops.twse.com.tw/mops/web/t146sb05']

    # https://www.youtube.com/watch?v=Lo3aswJ7lzw
    # https://doc.scrapy.org/en/latest/topics/request-response.html
    def parse(self, response):
        fordata = {
            'co_id': '2330',
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
        return scrapy.FormRequest(
            url='https://mops.twse.com.tw/mops/web/ajax_t146sb05',
            formdata=fordata,
            callback=self.after_submit
        )

    def after_submit(self, response):
        self.write_page(response)

        fordata = {
            'co_id': '2330',
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
            callback=self.handle_eps
        )

    def write_page(self, response):
        page = response.url.split("/")[-1]
        filename = '%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log("Writ to file %s" % filename)

    def handle_eps(self, response):
        self.write_page(response)
        #formatted_body = str(response.body).replace("TABLE", "table")
        formatted_body = response.body.decode("utf-8").replace("TABLE", "table")
        formatted_body = formatted_body.replace("TH", "th")
        formatted_body = formatted_body.replace("TR", "tr")
        formatted_body = formatted_body.replace("TD", "td")

        data = pd.read_html(formatted_body, skiprows=1, encoding='big5')
        #data = pd.read_html(formatted_body, skiprows=1, encoding='utf-8')
        #data = pd.read_html(formatted_body, skiprows=1)

        print("df: ", data)
        #data[0].to_csv("2330-eps.csv", encoding='utf-8', index=False)
        #data[0].encode('utf-8').to_csv("2330-eps.csv", index=False)
        #data[0].to_csv("2330-eps.csv", encoding='big5', index=False)
        data[0].to_csv("2330-eps.csv", index=False)







