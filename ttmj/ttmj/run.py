# -*- coding: utf-8 -*-
'''
@time: 2018/8/24 13:11
@author: Jack Luo
//todo:1、按tv名称，并分季将提取码、链接数据写入excel，并下载封面cover到总文件夹；2、让结果按照剧集顺序排序；3、引入代理ip，存入数据库
'''
from scrapy.cmdline import execute

execute(('scrapy crawl tt').split())

