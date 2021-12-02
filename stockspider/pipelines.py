# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import hashlib
from itemadapter import ItemAdapter
import redis

class StockspiderPipeline:
    
    def __init__(self):
        self.__url_to_file__ = open("url_to_html_file.txt", 'a')
        pass
    
    def __del__(self):
        self.__url_to_file__.close()

    def process_item(self, item, spider):
        url_string = item['url']
        filename = "html/{0}.html".format(item['url_hash'])
        with open(filename, 'w') as f:
            f.write(item['content'].decode("utf-8"))
        self.__url_to_file__.write("%s -< : >- %s\r\n" %(url_string.decode('utf-8'), filename))
        self.__url_to_file__.flush()
        return item

class URLInsertPipline:
    
    @classmethod
    def from_crawler(cls,crawler):
        redis_server = crawler.settings.get("FINISH_URL_REDIS_IP")
        redis_port = crawler.settings.get("FINISH_URL_REDIS_PORT")
        redis_password = crawler.settings.get("FINISH_URL_REDIS_REQUIREPASS")
        return cls(redis_server, redis_port, redis_password)

    def __init__(self, redis_server, redis_port, redis_password):
        self.__pool__ = redis.ConnectionPool(
            host=redis_server, port = redis_port, decode_responses=True)
        self.__redis__ = redis.Redis(connection_pool = self.__pool__)

    def __del__(self):
        self.__redis__.close()
        self.__pool__.disconnect()

    def process_item(self, item, spider):
        print('url', item['url_hash'])
        self.__redis__.sadd('url', item['url_hash'])
        return item