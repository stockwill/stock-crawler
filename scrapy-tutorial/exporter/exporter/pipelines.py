# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from .exporters import FanItemExporter


class ExporterPipeline(object):
    def process_item(self, item, spider):
        return item


class FanExportPipeline(object):
    def __init__(self, file_name):
        self.file_name = file_name
        self.file_handle = None

    @classmethod
    def from_crawler(cls, crawler):
        # output_file_name = crawler.settings.get('FILE_NAME')
        output_file_name = 'sample_output.json'
        return cls(output_file_name)

    def open_spider(self, spider):
        file = open(self.file_name, 'wb')
        self.file_handle = file

        self.exporter = FanItemExporter(file)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file_handle.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item