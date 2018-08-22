# -*- coding: utf-8 -*-

from os.path import basename, dirname, join

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.files import FilesPipeline

from .items import LuooItem


# class LuooPipeline(object):
#     def process_item(self, item, spider):
#         return item

class MusicPipeline(FilesPipeline):  # 继承该类
    def file_path(self, request, response=None, info=None):
        print(LuooItem.qi_shu)
        print(type(LuooItem.qi_sh))
        path = r'E:\pycharmcode\luoo\luoo\downluoo\full' + LuooItem.qi_shu + LuooItem.music_name + LuooItem.singer
        return join(basename(dirname(path)), basename(path))
        # return path
