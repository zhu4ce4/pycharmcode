# -*- coding: utf-8 -*-
'''
@datetime: 2018/8/26 14:04
@author: Jack Luo
//todo:爬取豆瓣2017年度电影榜单，各榜单数据：标题、图片(以对应的名字命名该图片)
'''
from scrapy.cmdline import execute

execute('scrapy crawl doubanmv'.split())
