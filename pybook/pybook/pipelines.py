# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem


class PybookPipeline(object):
    def process_item(self, item, spider):
        item['作者'] = item['作者'].strip('更多').strip('&0').strip('&1').strip('&2').strip('&3').strip('&4')
        # return item
        print(item)


class DuplicatesPipeline(object):
    def __init__(self):
        self.book_set = set()

    def process_item(self, item, spider):
        ma = item['条形码']
        name = item['书名']
        if ma in self.book_set:
            raise DropItem(f'发现重复的条形码（疑似重复的书）：{name}')
        self.book_set.add(ma)
        return item

# class MongoDBPipeline(object):
#     @classmethod
#     def from_crawler(cls, crawler):
#         cls.DB_URI = crawler.settings.get('MONGO_DB_URI', 'mongodb://localhost:27017')
#         cls.DB_NAME = crawler.settings.get('MONGO_DB_NAME', 'book')
#         return cls()
#
#     def open_spider(self, spider):
#         self.client = pymongo.MongoClient(self.DB_URI)
#         self.db = self.client[self.DB_NAME]
#
#     def close_spider(self, spider):
#         self.client.close()
#
#     def process_item(self, item, spider):
#         collection = self.db[spider.name]
#         post = dict(item) if isinstance(item, Item) else item
#         collection.insert_one(post)
#         return item
