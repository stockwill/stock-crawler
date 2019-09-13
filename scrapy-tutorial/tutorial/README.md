[Tutorial](https://docs.scrapy.org/en/latest/intro/tutorial.html)

# View

[Using developer tools in the browser](https://docs.scrapy.org/en/latest/topics/developer-tools.html#topics-developer-tools)

[SelectGadget chrome extension](https://chrome.google.com/webstore/detail/selectorgadget/mhjhnkcfbdhnjickkkdbjoemdmbfginb)

# Further Reading

[Python 3 tutorial](https://docs.python.org/3/tutorial/)
[Automate the Boring Stuff With Python](https://automatetheboringstuff.com/)
[How To Think Like a Computer Scientist](http://openbookproject.net/thinkcs/python/english3e/)
[Learn Python 3 The Hard Way](https://learnpythonthehardway.org/python3/)
[CSS Selector](https://code.tutsplus.com/zh-hant/tutorials/the-30-css-selectors-you-must-memorize--net-16048)

[More on reddit wiki](https://www.reddit.com/r/learnpython/wiki/index#wiki_new_to_python.3F)

## XPath

[Learn XPath](https://docs.scrapy.org/en/latest/intro/tutorial.html#xpath-a-brief-intro)

## Extracting

```
response.css('.author::text')[0].get()
```

```
response.css('.tag::text')[0].get()
```

```
response.css('ul.pager a::attr(href)').get()
response.css('li.next a::attr(href)').get()
response.css('li.next a').attrib['href']
```

```
http://quotes.toscrape.com/author/Albert-Einstein
```
```
author = response.follow(response.css('.author + a::attr(href)').get())
fetch(author)
```