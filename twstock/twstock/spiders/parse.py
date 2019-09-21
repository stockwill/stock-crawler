import re


# https://docs.python.org/zh-cn/3/library/re.html
def parse_quarter(s):
    pattern = re.compile(r"(\d+)年第(\d+)季")
    match = pattern.match(s)
    if match:
        #print(match.groups())
        #print(match.group(0))
        #print(match.group(1))
        #print(match.group(2))
        return True, match.group(1), match.group(2)
    return False, None, None


def parse_year(s):
    pattern = re.compile(r"(\d+)年年度")
    match = pattern.match(s)
    if match:
        #print(match.groups())
        #print(match.group(0))
        #print(match.group(1))
        return True, match.group(1)
    return False, None


def format_time_at(s):
    ok, year, quarter = parse_quarter(s)
    if ok:
        return "%d Q%s" % (int(year)+1911, quarter)

    ok, year = parse_year(s)
    if ok:
        return "%d" % (int(year)+1911)

    return s


def main():
    parse_quarter('108年第2季')
    parse_year('107年年度')


if __name__ == '__main__':
    main()
