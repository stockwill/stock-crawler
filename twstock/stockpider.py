import scrapy

class StockSpider(scrapy.Spider):
    name = 'stockspider'
    start_urls = ['https://mops.twse.com.tw/mops/web/t146sb05']

    def parse(self, response):
        pass