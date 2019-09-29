all: quotes

gen:
	scrapy genspider quotes quotes.toscrape.com


QUOTES_JSON=quotes.json
quotes:
	$(RM) $(QUOTES_JSON)
	scrapy crawl quotes -o $(QUOTES_JSON)


clean:
	rm -f authors/*.json
