.PHONY: all genspider stock

RM=rm -f

all: stock

genspider:
	scrapy genspider stockspider mops.twse.com.tw/mops/web/t146sb05 

STOCK_JSON=stock.json
stock:
	$(RM) $(STOCK_JSON)
	scrapy crawl stockspider -o $(STOCK_JSON)
