.PHONY: all genspider stock

RM=rm -f

all: stock

genspider:
	scrapy genspider stock mops.twse.com.tw/mops/web/t146sb05

STOCK_JSON=stock.json
stock:
	$(RM) $(STOCK_JSON)
	scrapy crawl stock -o $(STOCK_JSON)

clean:
	rm -f *.csv *.html
