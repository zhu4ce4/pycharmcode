# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PybookItem(scrapy.Item):
    ma = scrapy.Field()  # 条形码
    name = scrapy.Field()
    author = scrapy.Field()  # 有译者的，需要用field元数据将2者合并到author中列到一起
    # !!!author = scrapy.Field(serializer=(lambda x:x.split(',')))  # 有译者的，需要用field元数据将2者合并到author中列到一起
    base_price = scrapy.Field()
    sale_price = scrapy.Field()
    star45_prob = scrapy.Field()  # 评级4-5星的比例
    pub_date = scrapy.Field()
    comments_num = scrapy.Field()
    avg_star = scrapy.Field()  # 总的平均star
    ziying = scrapy.Field()  # bool值
    dianzi_version = scrapy.Field()  # bool值
    pub_comp = scrapy.Field()  # 第几版也要有
    # !!!!previews = scrapy.Field()  # 仅限简介的第一句话，以逗号或句号分辨
    # !!hotbuyer_said = scrapy.Field()
    # !!!newbuyer_date = scrapy.Field()
    # todo:筛选只要中文，而且不能是电子书 的图书，必须按照出版日期排序，同一本书不能重复(get 条形码去重？？)
