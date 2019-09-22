.PHONY: all genspider stock

RM=rm -f

all: financial

genspider:
	# scrapy genspider stock mops.twse.com.tw/mops/web/t146sb05
	scrapy genspider financial_report mops.twse.com.tw/server-java/t164sb01

STOCK_JSON=stock.json
stock:
	$(RM) $(STOCK_JSON)
	scrapy crawl stock -o $(STOCK_JSON)


FINANCIAL_JSON=financial.json
financial:
	$(RM) $(FINANCIAL_JSON)
	scrapy crawl financial_report -o $(FINANCIAL_JSON)


clean:
	rm -f data/*
