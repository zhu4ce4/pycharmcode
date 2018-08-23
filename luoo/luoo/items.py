# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LuooItem(scrapy.Item):
    file_urls = scrapy.Field()
    files = scrapy.Field()
    qi_shu = scrapy.Field()
    music_name = scrapy.Field()
