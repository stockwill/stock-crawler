import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
            'https://quotes.toscrape.com/page/1',
            'https://quotes.toscrape.com/page/2',
        ]

    def parse(self, response):
        # self.log('Current url: %s' % response.url)
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

        for quote in response.css("div.quote"):
            text = quote.css("span.text::text").get()
            author = quote.css("small.author::text").get()
            tags = quote.css("div.tags a.tag::text").getall()
            print(dict(text=text, author=author, tags=tags))