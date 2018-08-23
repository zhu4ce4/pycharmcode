# -*- coding: utf-8 -*-
'''
@time: 2018/8/22 20:22
@author: Jack Luo
@file: rum.py
'''
'''
图片与音乐同时下载，共用一个pipeline
'''
# todo：1、在每张专辑里面添加当前图片的缩略图，而非整张图片

from scrapy.cmdline import execute

execute('scrapy crawl luo'.split())
# execute('scrapy crawl luo -o luowang.xml'.split())
