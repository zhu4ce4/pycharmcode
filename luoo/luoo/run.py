# -*- coding: utf-8 -*-
'''
@time: 2018/8/22 20:22
@author: Jack Luo
@file: rum.py
'''
from scrapy.cmdline import execute

# execute('scrapy crawl luo'.split())
execute('scrapy crawl luo -o luowang.xml'.split())
