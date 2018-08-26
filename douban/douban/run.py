# -*- coding: utf-8 -*-
'''
@datetime: 2018/8/26 14:04
@author: Jack Luo
@任务:爬取豆瓣2017年度电影榜单，各榜单数据：以榜单标题为文件夹名字分类(内含对应的排名+名字+评分命名的图片)
//todo:待优化：ip代理池持续维护，ip提取使用前需再次测试可用性
'''
from scrapy.cmdline import execute

execute('scrapy crawl doubanmv'.split())
