data_dir = "data/"


def get_data_dir():
    return data_dir


def write_page(response):
    page = response.url.split("/")[-1]
    filename = data_dir + '%s.html' % page
    with open(filename, 'wb') as f:
        f.write(response.body)
    print("Write to file %s" % filename)
