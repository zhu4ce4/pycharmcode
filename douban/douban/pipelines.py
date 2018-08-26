# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


from scrapy.http import Request
from scrapy.pipelines.images import ImagesPipeline


class PicPipeline(ImagesPipeline):  # 继承该类

    # def get_media_requests(self, item, info):
    #     for url in item['image_urls']:
    #         print(url)
    #         print(1)
    #         return Request(url, meta={'item': item})
    #
    # def file_path(self, request, response=None, info=None):
    #     item = request.meta['item']
    #     # rank = item['rank']
    #     name = item['name']
    #     # rating = item['rating']
    #     # title = item['title']
    #     # image_url=request.url
    #     image_url = item['image_urls'][0]
    #     print(2)
    #     print(name)
    #     print(3)
    #     exit()
    #     # name=str(rank)+name+str(rating)
    #     # path = f'{title}/{name}.{image_url[-3:]}'
    #     # return path

    def get_media_requests(self, item, info):
        for cixu,url in enumerate(item['image_urls']):
            yield Request(url,meta={'item':item,'cixu':cixu})

    def file_path(self, request, response=None, info=None):
        item=request.meta['item']
        cixu=request.meta['cixu']
        rank = item['rank'][cixu]
        name = item['name'][cixu]
        rating = item['rating'][cixu]
        title=item['title']
        image_url=item['image_urls'][cixu]
        name=rank+name+rating
        path = f'{title}/{name}.{image_url[-3:]}'
        return path
