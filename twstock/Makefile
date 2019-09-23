.PHONY: all genspider stock dividend

RM=rm -f

all: dividend 

genspider:
	# scrapy genspider stock mops.twse.com.tw/mops/web/t146sb05
	# scrapy genspider financial_report mops.twse.com.tw/server-java/t164sb01
	scrapy genspider dividend mops.twse.com.tw/mops/web/t05st09_2

STOCK_JSON=stock.json
stock:
	$(RM) $(STOCK_JSON)
	scrapy crawl stock -o $(STOCK_JSON)


FINANCIAL_JSON=financial.json
financial:
	$(RM) $(FINANCIAL_JSON)
	scrapy crawl financial_report -o $(FINANCIAL_JSON)

DIVIDEND_JSON=dividend.json
dividend:
	$(RM) $(DIVIDEND_JSON)
	scrapy crawl dividend -o $(DIVIDEND_JSON)

clean:
	rm -f data/* eps/* dividend/*
