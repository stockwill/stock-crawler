.PHONY: all genspider stock 

RM=rm -f

all: daily_stock_price 

genspider:
	# scrapy genspider stock mops.twse.com.tw/mops/web/t146sb05
	# scrapy genspider financial_report mops.twse.com.tw/server-java/t164sb01
	# scrapy genspider dividend mops.twse.com.tw/mops/web/t05st09_2
	scrapy genspider daily_stock_price www.twse.com.tw 

STOCK_JSON=stock.json
stock:
	$(RM) $(STOCK_JSON)
	scrapy crawl stock -o $(STOCK_JSON)



.PHONY: eps
EPS_JSON=eps.json
eps:
	$(RM) $(EPS_JSON)
	scrapy crawl financial_report -o $(EPS_JSON)


.PHONY: dividend
DIVIDEND_JSON=dividend.json
dividend:
	$(RM) $(DIVIDEND_JSON)
	scrapy crawl dividend -o $(DIVIDEND_JSON)

.PHONY: dividend_date
DIVIDEND_DATE_JSON=dividend_date.json
dividend_date:
	$(RM) $(DIVIDEND_DATE_JSON)
	scrapy crawl dividend_date -o $(DIVIDEND_DATE_JSON)

.PHONY: daily_stock_price 
DAILY_STOCK_RPICE_JSON=daily_stock_price.json
daily_stock_price:
	$(RM) $(DIVIDEND_DATE_JSON)
	scrapy crawl daily_stock_price -o $(DAILY_STOCK_RPICE_JSON)

clean:
	rm -f data/* eps/* dividend/*
