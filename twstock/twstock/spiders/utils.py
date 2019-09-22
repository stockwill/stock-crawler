from time import gmtime, strftime

data_dir = "data/"


def get_data_dir():
    return data_dir


def write_page(response):
    page = response.url.split("/")[-1]
    filename = data_dir + '%s.html' % page
    with open(filename, 'wb') as f:
        f.write(response.body)
    print("Write to file %s" % filename)


def get_meta_data(info, co_id):
    return {
        "1. Information": info,
        "2. Symbol": "TW:" + co_id,
        "3. Last Refreshed": strftime("%Y-%m-%d %H:%M:%S", gmtime()),
        "4. Time Zone": 'UTC',
    }
