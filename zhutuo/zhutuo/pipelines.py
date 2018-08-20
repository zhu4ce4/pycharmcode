# -*- coding: utf-8 -*-

import pymongo
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
from scrapy.item import Item


class ZhutuoPipeline(object):
    i = 20

    def process_item(self, item, spider):
        if len(item['biaoti']) > 20:
            item['biaoti'] = item['biaoti'][:self.i]
        return item


class DuplicatesPipeline(object):
    def __init__(self):
        self.title_set = set()

    def process_item(self, item, spider):
        biaoti = item['biaoti']
        if biaoti in self.title_set:
            raise DropItem(f'duplicate title found:{biaoti}')
        self.title_set.add(biaoti)
        return item


class MongodbPipeline(object):
    @classmethod
    def from_crawler(cls, crawler):
        cls.DB_URI = crawler.settings.get('MONGO_DB_URI', 'mongodb://localhost:27017')
        cls.DB_NAME = crawler.settings.get('MONGO_DB_NAME', 'dailynews')
        return cls()

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.DB_URI)
        self.db = self.client[self.DB_NAME]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        collection = self.db[spider.name]
        post = dict(item) if isinstance(item, Item) else item
        collection.insert_one(post)
        return item
