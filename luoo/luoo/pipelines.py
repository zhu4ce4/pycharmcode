# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.http import Request
from scrapy.pipelines.files import FilesPipeline


class MusicPipeline(FilesPipeline):  # 继承该类
    def get_media_requests(self, item, info):
        for url in item['file_urls']:
            yield Request(url, meta={'item': item})

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        qi_shu = item['qi_shu']
        music_name = item['music_name']
        file_urls = item['file_urls']
        path = f'{qi_shu}/{music_name}.{file_urls[0][-3:]}'
        return path

# todo：1、在每张专辑里面添加当前图片的缩略图，2、多线程；
