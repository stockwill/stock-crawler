.PHONY: all install freeze twstock

all:

install:
	# pip install scrapy
	pip install -r requirements.txt

freeze:
	pip freeze > requirements.txt

twstock:
	scrapy startproject twstock
