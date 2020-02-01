.PHONY: all install freeze twstock

all:

# https://sourabhbajaj.com/mac-setup/Python/virtualenv.html
# https://gist.github.com/pandafulmanda/730a9355e088a9970b18275cb9eadef3
.PHONY: venv
venv: 
	virtualenv -p python3 venv

install:
	# pip install scrapy
	pip install -r requirements.txt

freeze:
	pip freeze > requirements.txt

twstock:
	scrapy startproject twstock
