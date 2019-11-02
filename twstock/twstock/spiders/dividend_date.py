# -*- coding: utf-8 -*-
import scrapy
from .stocks import get_co_ids


# TODO: write dividend_date.csv
# TODO: remove at in the original dividend.py

class DividendDateItem(scrapy.Item):
    date = scrapy.Field()
    co_id = scrapy.Field()


class DividendDateSpider(scrapy.Spider):
    name = "dividend_date"
    allowed_domains = ['mops.twse.com.tw']
    custom_settings = {
        'ITEM_PIPELINES': {
            'twstock.exporters.csv_exporter.CSVExportPipeline': 1,
        }
    }

    # Exporter settings
    output_dir = "dividend/"
    filename_suffix = "-dividend-date"

    def parse(self, response):
        pass

    # https://mops.twse.com.tw/mops/web/t108sb19_q1
    def start_requests(self):
        for co_id in get_co_ids():
            formdata = {
                'encodeURIComponent': '1',
                'run': 'Y',
                'step': '1',
                'TYPEK': 'sii',
                'year': '',
                'co_id': co_id,
                'month': 'all',
                'b_date': '',
                'e_date': '',
                'isnew': 'false',
                'firstin': 'true',
            }
            yield scrapy.FormRequest(
                url='https://mops.twse.com.tw/mops/web/ajax_t108sb19',
                formdata=formdata,
                callback=self.parse_for_button,
                cb_kwargs=dict(co_id=co_id)
            )

    def parse_for_button(self, response, co_id):
        buttons = response.xpath('//input[@value="詳細資料"]')
        for btn in buttons:
            date1 = btn.xpath('@onclick').get()
            date1 = str.split(date1, ";")[0]
            date1 = str.split(date1, '"')[1]
            formdata = {
                'encodeURIComponent': '1',
                'run': 'Y',
                'step': '1',
                'TYPEK': 'sii',
                'year': '',
                'co_id': co_id,
                'month': 'all',
                'b_date': '',
                'e_date': '',
                'isnew': 'false',
                'firstin': 'true',
                'DATE1': date1,
                "SEQ_NO": "1",
                "COMP": co_id,
                "isnew:": "false",
                "SKIND": "G",
                "step": "2",
            }
            yield scrapy.FormRequest(
                url='https://mops.twse.com.tw/mops/web/ajax_t108sb22',
                formdata=formdata,
                callback=self.parse_for_date,
                cb_kwargs=dict(co_id=co_id)
            )

    def parse_for_date(self, response, co_id):
        for td in response.xpath("//td"):
            if td.xpath("./b/text()").get() == u'除權/除息交易日：':
                date = td.xpath("./nobr/text()").get().strip().strip('\n')
                print("date: ", date)
                val = {'co_id': co_id, 'date': date}
                yield self.get_dividend_date_item(val)

    @staticmethod
    def get_dividend_date_item(d):
        item = DividendDateItem()
        for k, v in d.items():
            item[k] = v

        return item
