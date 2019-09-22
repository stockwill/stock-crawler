# -*- coding: utf-8 -*-
import scrapy
import pandas as pd
from .parse import reformat_html_for_table, format_time_at
from .stocks import get_co_ids
from .utils import write_page, get_data_dir, get_meta_data

debug = False


class StockSpider(scrapy.Spider):
    name = 'stock'
    allowed_domains = ['mops.twse.com.tw']

    # https://www.youtube.com/watch?v=Lo3aswJ7lzw
    # https://doc.scrapy.org/en/latest/topics/request-response.html
    def start_requests(self):
        for co_id in get_co_ids():
            formdata = {
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
                formdata=formdata,
                callback=self.after_submit,
                cb_kwargs=dict(co_id=co_id)
            )

            yield request

    def after_submit(self, response, co_id):
        if debug:
            write_page(response)

        formdata = {
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
            formdata=formdata,
            callback=self.handle_eps,
            cb_kwargs=dict(co_id=co_id)
        )

    def parse(self, response):
        pass

    def handle_eps(self, response, co_id):
        if debug:
            write_page(response)
        formatted_body = reformat_html_for_table(response)

        data = pd.read_html(formatted_body, skiprows=0, encoding='big5')
        df = data[2]

        wanted_cols = [['股利所屬年(季)度', 'time', -1, '', format_time_at],
                       ['盈餘分配之現金股利(元/股)', 'cash', -1, '0.0', lambda x: x],
                       ['盈餘轉增資配股(元/股)', 'stock', -1, '0.0', lambda x: x]]

        # print('columns: ', df.columns)
        for pos_cols, cols in enumerate(df.columns):
            for pos_wanted_cols, w in enumerate(wanted_cols):
                # print('w: ', w, 'cols: ', cols)
                if w[0] == cols[1]:
                    wanted_cols[pos_wanted_cols][2] = pos_cols
                    break

        if debug:
            df.to_csv(get_data_dir() + co_id + "-dividend-full.csv", index=False)

        rows = []
        for index, row in df.iterrows():
            vals = []

            for pos_wanted_cols, wanted_col in enumerate(wanted_cols):
                vals.append(wanted_col[3])
                wanted_col_pos = wanted_col[2]
                # print('vals: ', vals, ' pos_wanted_cols: ', pos_wanted_cols)
                if wanted_col_pos != -1:
                    f = wanted_col[4]
                    original_data = row[df.columns[wanted_col_pos]]
                    vals[pos_wanted_cols] = f(original_data)

            rows.append(vals)

        columns = []
        for wanted_col in wanted_cols:
            columns.append(wanted_col[1])

        # print('rows: ', rows, ' columns: ', columns)
        dividend_df = pd.DataFrame(rows, columns=columns)
        dividend_path = get_data_dir() + co_id + "-dividend.csv"
        dividend_df.to_csv(dividend_path, index=False)

        yield {
            "meta_data": get_meta_data("Time Series for Dividend", "TW:" + co_id),
            "dividend": dividend_path,
        }
