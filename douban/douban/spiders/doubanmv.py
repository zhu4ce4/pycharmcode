# -*- coding: utf-8 -*-
import json

import scrapy

from ..items import DoubanItem


class DoubanmvSpider(scrapy.Spider):
    name = 'doubanmv'
    allowed_domains = ['movie.douban.com']
    start_urls = [f'https://movie.douban.com/ithil_j/activity/movie_annual2017/widget/{i}' for i in range(1, 2)]

    # start_urls = ['https://movie.douban.com/annual/2017?source=navigation#{i}' for i in range(1,88)]

    def parse(self, response):
        item = DoubanItem()
        resp = json.loads(response.text)
        title = resp['res']['payload']['title']
        item['title'] = title
        infos = resp['res']['subjects']
        for rk, info in enumerate(infos):
            name = info['title']
            rating = info['rating']
            pic = info['cover']
            link = info['url']
            rank = rk + 1

            item['name'] = name
            item['rating'] = rating
            item['pic'] = pic
            item['link'] = link
            item['rank'] = rank
            yield item
