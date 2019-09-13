.PHONY: all quotes author


RM=rm -f

all: author

AUTHOR_JSON=author.json
author:
	$(RM) $(AUTHOR_JSON)
	scrapy crawl author -o $(AUTHOR_JSON)

QUOTES_JSON=quotes.json
quotes:
	$(RM) $(QUOTES_JSON)
	scrapy crawl quotes -o $(QUOTES_JSON)

shell:
	scrapy shell 'http://quotes.toscrape.com/page/1/'

clean:
	$(RM) quotes-1.html quotes-2.html


QUOTES_JL=quotes.jl
jl:
	$(RM) $(QUOTES_JL)
	scrapy crawl quotes -o $(QUOTES_JL)

