# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PybookItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    ma = scrapy.Field()  # 条形码
    name = scrapy.Field()
    author = scrapy.Field()  # 有译者的，需要用field元数据将2者合并到author中列到一起
    youhuo = scrapy.Field()  # bool值
    base_price = scrapy.Field()
    sale_price = scrapy.Field()
    star45_prob = scrapy.Field()  # 评级4-5星的比例
    pub_date = scrapy.Field()
    comments_num = scrapy.Field()
    star = scrapy.Field()  # 总的平均star
    arrival_date = scrapy.Field()
    yun_fee = scrapy.Field()
    previews = scrapy.Field()  # 仅限简介的第一句话，以逗号或句号分辨
    ziying = scrapy.Field()  # bool值
    sender = scrapy.Field()
    dianzi_version = scrapy.Field()  # bool值
    pub_comp = scrapy.Field()  # 第几版也要有
    hotbuyer_said = scrapy.Field()
    newbuyer_said = scrapy.Field()
    newbuyer_date = scrapy.Field()

    # todo:筛选只要中文，而且不能是电子书 的图书，必须按照出版日期排序，同一本书不能重复(get 条形码去重？？)
