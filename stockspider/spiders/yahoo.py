import random
import re
import scrapy
from scrapy import selector
from scrapy import settings
from scrapy.item import Item
from w3lib import url
import re
import hashlib
import redis
from stockspider.items import StockspiderItem
from scrapy.utils.project import get_project_settings

class YahooSpider(scrapy.Spider):
    name = 'yahoo'
    allowed_domains = ['yahoo.com']
    start_urls = ['https://finance.yahoo.com/']

    def __init__(self, name=None, **kwargs):
        super().__init__(name=name, **kwargs)
        settings = get_project_settings()
        redis_server = settings['FINISH_URL_REDIS_IP']
        redis_port = settings['FINISH_URL_REDIS_PORT']
        redis_password = settings['FINISH_URL_REDIS_REQUIREPASS']
        self.__pool__ = redis.ConnectionPool(
            host=redis_server, port = redis_port, decode_responses=True)
        self.__redis__ = redis.Redis(connection_pool = self.__pool__)
        print(settings)

    def __del__(self):
        self.__redis__.close()
        self.__pool__.disconnect()

    def parse(self, response):
        print(response.request.headers['User-Agent'])
        item = StockspiderItem()
        url = response.url.encode('utf-8')
        md5 = hashlib.md5()
        md5.update(url)
        url_hash = md5.hexdigest()
        item["url_hash"] = url_hash
        item["url"] = url
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
                if(self.__redis__.sismember('url', url_hash)):
                    continue
                yield scrapy.Request(url, callback=self.parse, dont_filter=True)
        yield item

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
    print(sys.argv[0])
    from scrapy import cmdline
    cmdline.execute("scrapy crawl yahoo".split())