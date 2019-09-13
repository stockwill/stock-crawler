import scrapy

class AuthorSpider(scrapy.Spider):
    name = "author"

    start_urls = ['https://quotes.toscrape.com/']

    def parse(self, response):
        for href in response.css('.author + a::attr(href)'):
            yield response.follow(href, self.parse_author)

        for href in response.css('li.next a::attr(href)'):
            yield response.follow(href, self.parse)

    # Another interesting thing this spider demonstrates is that, even if there are many quotes from the same author, we don’t need to worry about visiting the same author page multiple times. By default, Scrapy filters out duplicated requests to URLs already visited, avoiding the problem of hitting servers too much because of a programming mistake.
    def parse_author(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        yield {
            'name': extract_with_css('h3.author-title::text'),
            'birthdate': extract_with_css('.author-born-date::text'),
            'bio': extract_with_css('.author-description::text'),
        }