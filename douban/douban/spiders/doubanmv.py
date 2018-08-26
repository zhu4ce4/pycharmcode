# -*- coding: utf-8 -*-
import json

import scrapy

from ..items import DoubanItem


class DoubanmvSpider(scrapy.Spider):
    name = 'doubanmv'
    # allowed_domains = ['movie.douban.com']
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
            pic_url = info['cover']
            rank = rk + 1

            item['name'] = name
            item['rating'] = rating
            item['image_urls'] = [pic_url]
            item['rank'] = rank
            yield item


'''    def parse(self, response):
        item = DoubanItem()
        resp = json.loads(response.text)
        title = resp['res']['payload']['title']
        item['title'] = title
        infos = resp['res']['subjects']
        names=[]
        ratings=[]
        image_urls=[]
        ranks=[]
        for rk, info in enumerate(infos):

            name = info['title']
            rating = info['rating']
            pic_url = info['cover']
            rank = rk + 1

            names.append(name)
            ratings.append(str(rating))
            image_urls.append(pic_url)
            ranks.append(str(rank))

            item['name'] = names
            item['rating'] = ratings
            item['image_urls'] = image_urls
            item['rank'] = ranks
        yield item
        '''
