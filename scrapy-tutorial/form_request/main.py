import scrapy


# from scrapy.selector import Selector

class FormRequestSpider(scrapy.Spider):
    name = 'form_request'

    def start_requests(self):
        co_id = '1101'
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

        return [scrapy.FormRequest(
            url='https://mops.twse.com.tw/mops/web/ajax_t108sb19',
            formdata=formdata,
            callback=self.parse,
            cb_kwargs=dict(co_id=co_id)
        )]

    def parse(self, response, co_id):
        filename = "test.html"
        with open(filename, 'wb') as f:
            f.write(response.body)

        print('response type: ', type(response))
        # sel = Selector(response)
        # print('result: ', response.xpath('//input').getall())
        # print('result[0]: ', response.xpath('//input')[0].get())
        # print('result[1]: ', response.xpath('//input')[1].get())
        # print('result[2]: ', response.xpath('//input')[2].get())
        # print('result[3]: ', response.xpath('//input')[3].get())
        # print('result[4]: ', response.xpath('//input')[4].get())
        # print('result[5]: ', response.xpath('//input')[5].get())
        # print('result[6]: ', response.xpath('//input')[6].get())
        # print('result[7]: ', response.xpath('//input')[7].get())
        # print('result[8]: ', response.xpath('//input')[8].get())
        # print('result[9]: ', response.xpath('//input')[9].get())
        # print('result[10]: ', response.xpath('//input')[10].get())
        # print('result[11]: ', response.xpath('//input')[11].get())

        # <input type="button" value="詳細資料" onclick='document.t108sb22_fm1.DATE1.value="20050816";document.t108sb22_fm1.SEQ_NO.value="1";document.t108sb22_fm1.COMP.value="1101";openWindow(this.form ,"");'>
        buttons = response.xpath('//input[@value="詳細資料"]')
        # print("buttons: ", buttons)

        for btn in buttons:
            # print(btn.xpath('@value'))
            date1 = btn.xpath('@onclick').get()
            date1 = str.split(date1, ";")[0]
            date1 = str.split(date1, '"')[1]
            # print(date1)
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
                callback=self.parse2,
                cb_kwargs=dict(co_id=co_id)
            )

    def parse1(self, response, co_id):
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
            'DATE1': '20050816',
            "SEQ_NO": "1",
            "COMP": co_id,
            "isnew:": "false",
            "SKIND": "G",
            "step": "2",
        }
        return [scrapy.FormRequest(
            url='https://mops.twse.com.tw/mops/web/ajax_t108sb22',
            formdata=formdata,
            callback=self.parse2,
            cb_kwargs=dict(co_id=co_id)
        )]

    def parse2(self, response, co_id):
        # print("target: ", response.xpath("//td"))
        for td in response.xpath("//td"):
            # print("b: ", td.xpath("./b"), " get: ", td.xpath("./b/text()").get())
            if td.xpath("./b/text()").get() == u'除權/除息交易日：':
                print("target b: ", td.xpath("./b"))
                print("target: ", td.xpath("./nobr/text()").get())

        # print("target: ", response.xpath("//td[/b = '除權/除息交易日：']"))
