from scrapy.exporters import JsonItemExporter
from scrapy.exporters import CsvItemExporter


# https://docs.scrapy.org/en/latest/topics/exporters.html
class EPSJsonExportPipeline(object):

    def open_spider(self, spider):
        self.eps_exporter = {}

    def close_spider(self, spider):
        for exporter in self.eps_exporter.values():
            exporter.finish_exporting()
            exporter.file.close()

    def _exporter_for_item(self, item):
        co_id = item['co_id']
        if co_id not in self.eps_exporter:
            output_file_name = 'eps/{}-eps.json'.format(co_id)
            f = open(output_file_name, 'wb')
            print('write to file: ', output_file_name)
            exporter = JsonItemExporter(f)
            exporter.start_exporting()
            self.eps_exporter[co_id] = exporter
        return self.eps_exporter[co_id]

    def process_item(self, item, spider):
        exporter = self._exporter_for_item(item)
        exporter.export_item(item)
        return item

class EPSCSVExportPipeline(object):

    def open_spider(self, spider):
        self.eps_exporter = {}

    def close_spider(self, spider):
        for exporter in self.eps_exporter.values():
            exporter['exporter'].finish_exporting()
            exporter['file'].close()

    def _exporter_for_item(self, item):
        co_id = item['co_id']
        if co_id not in self.eps_exporter:
            output_file_name = 'eps/{}-eps.csv'.format(co_id)
            f = open(output_file_name, 'wb')
            print('write to file: ', output_file_name)
            exporter = CsvItemExporter(f)
            exporter.start_exporting()
            self.eps_exporter[co_id] = {
                'exporter': exporter,
                'file': f,
            }

        return self.eps_exporter[co_id]['exporter']

    def process_item(self, item, spider):
        exporter = self._exporter_for_item(item)
        exporter.export_item(item)
        return item