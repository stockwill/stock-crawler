.PHONY: all

all:
	rm quotes.json
	scrapy crawl quotes -o quotes.json

shell:
	scrapy shell 'http://quotes.toscrape.com/page/1/'

clean:
	rm quotes-1.html quotes-2.html


JL=quotes.jl
jl:
	rm $(JL)
	scrapy crawl quotes -o $(JL)

