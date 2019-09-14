# -*- coding: utf-8 -*-
import scrapy


class StockspiderSpider(scrapy.Spider):
    name = 'stockspider'
    allowed_domains = ['mops.twse.com.tw']
    start_urls = ['https://mops.twse.com.tw/mops/web/t146sb05']

    def parse(self, response):
        page = response.url.split("/")[-1]
        filename = '%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log("Writ to file %s" % filename)
