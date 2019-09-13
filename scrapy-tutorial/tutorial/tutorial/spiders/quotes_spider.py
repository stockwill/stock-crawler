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

        #next_page = response.css('li.next a::attr(href)').get()
        #if next_page is not None:
        #    yield response.follow(next_page, callback=self.parse)
        #for href in response.css('li.next a::attr(href)'):
        #    yield response.follow(href, callback=self.parse)
        for a in response.css('li.next a'):
            yield response.follow(a, callback=self.parse)