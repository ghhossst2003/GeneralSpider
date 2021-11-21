import random
import re
import scrapy
from scrapy import selector
from scrapy.item import Item
from w3lib import url
import re

from stockspider.items import StockspiderItem


class YahooSpider(scrapy.Spider):
    name = 'yahoo'
    allowed_domains = ['yahoo.com']
    start_urls = ['https://finance.yahoo.com/']

    def parse(self, response):
        print(response.request.headers['User-Agent'])
        item = StockspiderItem()
        item["url"] = response.url.encode('utf-8')
        item["content"] = response.body
        url_selector_list = response.xpath("//a")
        for selector in url_selector_list:
            url = selector.xpath("@href").extract()
            if len(url) > 0:
                url = url[0]
            else:
                continue
            if self.is_url(url) == True:
                print(url)
                yield scrapy.http.Request(url, callback=self.parse, dont_filter=False)
        # yield item

    def is_url(self, url):
        if len(url) <= 0 :
            return False
        match_object = re.match("(https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]", url)
        if match_object == None:
            return False
        match_object = match_object.span()
        if match_object[0] == 0 and match_object[1] == len(url):
            return True
        else:
            return False

if __name__ == "__main__":
    import sys
    # print(sys.argv[0])
    # from scrapy import cmdline
    # cmdline.execute("scrapy crawl yahoo".split())