import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
            'https://quotes.toscrape.com/page/1',
            'https://quotes.toscrape.com/page/2',
        ]

    def parse(self, response):
        for quote in response.css("div.quote"):
            text = quote.css("span.text::text").get()
            author = quote.css("small.author::text").get()
            tags = quote.css("div.tags a.tag::text").getall()
            yield {
                'text': text, 'author': author, 'tags': tags
            }

        for a in response.css('li.next a'):
            yield response.follow(a, callback=self.parse)