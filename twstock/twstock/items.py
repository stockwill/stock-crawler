# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class TwstockItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


# https://en.wikipedia.org/wiki/Candlestick_chart
# https://www.twse.com.tw/zh/page/trading/exchange/STOCK_DAY.html
class DailyStockPriceItem(scrapy.Item):
    date = scrapy.Field()  # 日期
    trade_volume = scrapy.Field()  # 成交股數
    trade_value = scrapy.Field()  # 成交金額
    opening_price = scrapy.Field()  # 開盤價
    highest_price = scrapy.Field()  # 最高價
    lowest_price = scrapy.Field()  # 最低價
    closing_price = scrapy.Field()  # 收盤價
    price_change = scrapy.Field()  # 漲跌價差
    transaction = scrapy.Field()  # 成交筆數
    co_id = scrapy.Field()