import unittest

import time
import datetime
import parse

def parse_int(val_str):
    return int(val_str.replace(',', ''))


def parse_float(val_str):
    return float(val_str.replace(',', ''))


# https://stackoverflow.com/questions/1697815/how-do-you-convert-a-time-struct-time-object-into-a-datetime-object
# https://pypi.org/project/parse/
def parse_time(time_str):
    #tm = time.strptime(time_str, "%Y/%m/%d")
    r = parse.parse('{}/{}/{}', time_str)
    year = int(r[0])
    month = int(r[1])
    day = int(r[2])
    if year < 200:
        year = year + 1911
    # return datetime.datetime(*tm[:6])
    return datetime.datetime(year=year,month=month,day=day)


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(datetime.datetime(2020 , 1 , 2), parse_time("2020/01/02"))
        self.assertEqual(datetime.datetime(2020, 1, 2), parse_time("109/01/02"))
        self.assertEqual(33282120, parse_int("33,282,120"))
        self.assertEqual(5090.5	, parse_float("5,090.5"))
        self.assertEqual(30	, parse_float("+30.0"))
        self.assertEqual(-150.5	, parse_float("-150.5"))


if __name__ == '__main__':
    unittest.main()
