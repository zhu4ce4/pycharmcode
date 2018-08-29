# -*- coding: utf-8 -*-

import pymongo
import redis
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
from scrapy.item import Item


class ZhutuoPipeline(object):
    i = 30
    def process_item(self, item, spider):
        if len(item['biaoti']) > self.i:
            item['biaoti'] = item['biaoti'][:self.i]
        return item


class YcltPipeline(object):
    def open_spider(self, spider):
        db_host = spider.settings.get('REDIS_HOST', 'localhost')
        db_port = spider.settings.get('REDIS_PORT', 6379)
        db_index = spider.settings.get('REDIS_DB_INDEX', 0)
        self.db_conn = redis.StrictRedis(host=db_host, port=db_port, db=db_index)
        self.item_i = 0

    def close_spider(self, spider):
        self.db_conn.connection_pool.disconnect()

    def process_item(self, item, spider):
        self.insert_db(item)

        return item

    def insert_db(self, item):
        if isinstance(item, Item):
            item = dict(item)

        self.item_i += 1
        self.db_conn.hmset(f'luntan:{self.item_i}', item)


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
