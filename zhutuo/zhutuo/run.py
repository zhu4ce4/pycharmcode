# -*- coding: utf-8 -*-
'''
@time: 2018/8/19 13:33
@author: Jack Luo
@file: run.py
'''
from scrapy.cmdline import execute

# execute('scrapy crawl zt -o zt.xml'.split())
execute('scrapy crawl weixin'.split())
# execute('scrapy crawlall'.split())
