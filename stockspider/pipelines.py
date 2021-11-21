# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import hashlib
from itemadapter import ItemAdapter


class StockspiderPipeline:
    
    def __init__(self):
        self.__url_to_file__ = open("url_to_html_file.txt", 'a')
        pass
    
    def __del__(self):
        self.__url_to_file__.close()

    def process_item(self, item, spider):
        url_string = item['url']
        hd5 = hashlib.md5()
        hd5.update(url_string)
        filename = "html/{0}.html".format(hd5.hexdigest())
        with open(filename, 'w') as f:
            f.write(item['content'].decode("utf-8"))
        self.__url_to_file__.write("%s -< : >- %s\r" %(url_string.decode('utf-8'), filename))
        self.__url_to_file__.flush()
        return item
