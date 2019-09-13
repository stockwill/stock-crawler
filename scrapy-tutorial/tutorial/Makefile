.PHONY: all

JSON=quotes.json

all:
	rm $(JSON)
	scrapy crawl quotes -o $(JSON)

shell:
	scrapy shell 'http://quotes.toscrape.com/page/1/'

clean:
	rm quotes-1.html quotes-2.html


JL=quotes.jl
jl:
	rm $(JL)
	scrapy crawl quotes -o $(JL)

