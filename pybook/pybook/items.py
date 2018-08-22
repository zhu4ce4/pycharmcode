# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


# def ser(tet):
#     return '|'.join(tet.split(','))

class PybookItem(scrapy.Item):

    条形码 = scrapy.Field()  # 条形码
    书名 = scrapy.Field()
    # 作者 = scrapy.Field()  # 有译者的，需要用field元数据将2者合并到author中列到一起
    作者 = scrapy.Field(serializer=lambda x: '|'.join(x.split(',')))  # serializer只能是在输出为csv的时候，才能起作用????
    定价 = scrapy.Field()
    售价 = scrapy.Field()
    四五星 = scrapy.Field()  # 评级4-5星的比例
    出版日期 = scrapy.Field()
    评论数 = scrapy.Field()
    平均分 = scrapy.Field()  # 总的平均star
    是自营 = scrapy.Field()  # bool值
    有电子书 = scrapy.Field()  # bool值
    出版社 = scrapy.Field(serializer=lambda x: '|'.join(x.split(';')))
    链接 = scrapy.Field()
    # !!!!previews = scrapy.Field()  # 仅限简介的第一句话，以逗号或句号分辨
    # !!hotbuyer_said = scrapy.Field()
    # !!!newbuyer_date = scrapy.Field()
    # todo:筛选只要中文，而且不能是电子书 的图书，必须按照出版日期排序，同一本书不能重复(get 条形码去重？？)
