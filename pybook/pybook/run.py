# -*- coding: utf-8 -*-
'''
@time: 2018/8/21 14:25
@author: Jack Luo
@file: run.py
'''
from scrapy.cmdline import execute

execute('scrapy crawl amazon -o amazonpython.csv --nolog'.split())
