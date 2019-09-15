# -*- coding: utf-8 -*-
import scrapy


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

    def write_page(self, response):
        page = response.url.split("/")[-1]
        filename = '%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log("Writ to file %s" % filename)
