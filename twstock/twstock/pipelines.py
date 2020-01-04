# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import mysql.connector
from mysql.connector import errorcode
import parse
import datetime

from twstock.items import DailyStockPriceItem


# https://stackoverflow.com/questions/9452775/converting-numpy-dtypes-to-native-python-types/11389998
def parse_int(val_str):
    return int(val_str.replace(',', '')) # val_str.item() #int(val_str.replace(',', ''))


def parse_float(val_str):
    if isinstance(val_str, str):
        return float(val_str.replace(',', ''))
    return val_str.item()


def parse_time(time_str):
    r = parse.parse('{}/{}/{}', time_str)
    year = int(r[0])
    month = int(r[1])
    day = int(r[2])
    if year < 200:
        year = year + 1911
    return datetime.datetime(year=year,month=month,day=day)


class TwstockPipeline(object):
    def process_item(self, item, spider):
        return item


class StockPriceMySQLPipeline(object):
    def __init__(self, mysql_user, mysql_password, mysql_host, mysql_database, mysql_port):
        self.cnx = None
        self.cursor = None
        self.mysql_user = mysql_user
        self.mysql_password = mysql_password
        self.mysql_host = mysql_host
        self.mysql_database = mysql_database
        self.mysql_port = mysql_port

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mysql_user=crawler.settings.get('MYSQL_USER'),
            mysql_password=crawler.settings.get('MYSQL_PASSWORD'),
            mysql_host=crawler.settings.get('MYSQL_HOST'),
            mysql_database=crawler.settings.get('MYSQL_DATABASE'),
            mysql_port=crawler.settings.get('MYSQL_PORT')
        )

    def open_spider(self, spider):
        try:
            cnx = mysql.connector.connect(user=self.mysql_user, password=self.mysql_password, host=self.mysql_host,
                                          database=self.mysql_database, port=self.mysql_port)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
                logging.log(logging.FATAL, "Fail to connect db: {}".format(err))

        else:
            print("Every thing is fine")
            self.cnx = cnx
            self.cursor = cnx.cursor()

    def close_spider(self, spider):
        if self.cursor is not None:
            self.cursor.close()
        if self.cnx is not None:
            self.cnx.close()

    def process_item(self, item, spider):
        if self.cursor is None:
            return item

        if isinstance(item, DailyStockPriceItem):
            try:
                self.handle_daily_stock_price_item(item)
            except Exception as err:
                logging.log(logging.FATAL, "Error in handle: {}".format(err))

        return item

    def handle_daily_stock_price_item(self, item):
        add = (
            "INSERT INTO stock_prices "
            "(stock_code, date, trade_volume, trade_value, opening_price, highest_price, lowest_price, closing_price, price_change, transaction, created_at, updated_at) "
            "VALUES (%(co_id)s, %(date)s, %(trade_volume)s, %(trade_value)s, %(opening_price)s, %(highest_price)s, %(lowest_price)s, %(closing_price)s, %(price_change)s, %(transaction)s, %(created_at)s, %(updated_at)s) "
            
            # "(stock_code, date, trade_volume, trade_value, opening_price, highest_price, lowest_price, closing_price, change, created_at) "
            # "VALUES (%(co_id)s, %(date)s, %(trade_volume)s, %(trade_value)s, %(opening_price)s, %(highest_price)s, %(lowest_price)s, %(closing_price)s, %(change)s, %(created_at)s)"

            #"(change) "
            #"VALUES (%(change)s)"

        )
        d = dict(item)
        now = datetime.datetime.now()

        d['date'] = parse_time(d['date']) # TODO

        d['trade_volume'] = parse_int(d['trade_volume'])
        d['trade_value'] = parse_int(d['trade_value'])

        d['opening_price'] = parse_float(d['opening_price'])
        d['highest_price'] = parse_float(d['highest_price'])
        d['lowest_price'] = parse_float(d['lowest_price'])
        d['closing_price'] = parse_float(d['closing_price'])
        d['price_change'] = parse_float(d['price_change'])

        d['transaction'] = parse_int(d['transaction'])

        d['created_at'] = now
        d['updated_at'] = now

        try:
            self.cursor.execute(add, d)
            self.cnx.commit()
        except mysql.connector.Error as err:
            self.cnx.rollback()
            print("Fail to commit: {}".format(err))