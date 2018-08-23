# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.http import Request
from scrapy.pipelines.files import FilesPipeline


class MusicPipeline(FilesPipeline):  # 继承该类

    def get_media_requests(self, item, info):  # 在此下载
        cixu = -1
        for url in item['file_urls']:
            cixu += 1
            yield Request(url, meta={'item': item, 'cixu': cixu})

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        qi_shu = item['qi_shu']
        music_name = item['music_name']
        file_urls = item['file_urls']
        cixu = request.meta['cixu']
        path = f'{qi_shu}/{music_name[cixu]}.{file_urls[cixu][-3:]}'
        return path
