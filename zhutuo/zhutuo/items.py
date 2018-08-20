# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhutuoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    biaoti = scrapy.Field()
    # biaoti=scrapy.Field(serializer=lambda x:'|'.join(x))
    link = scrapy.Field()


class GongKaiItem(ZhutuoItem):  # 继承了zhutuoitem
    # 拓展item子类
    time = scrapy.Field()
