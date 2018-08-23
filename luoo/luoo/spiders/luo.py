# -*- coding: utf-8 -*-
import re

import scrapy

from ..items import LuooItem


class LuoSpider(scrapy.Spider):
    qi_shu_start = input('***********请输入想要开始的期数：（将从该期倒计数下载）***********')
    total_qi = int(input('***********请输入想要下载的期总数：***********'))
    print('***********歌曲存储文件夹为："downluoo"***********')
    name = 'luo'
    allowed_domains = ['luoo.org']
    start_urls = [f'http://www.luoo.org/music/{qi_shu_start}.html']
    counts = 0
    ge_counts = 0

    def del_illegal(self, tet):
        pattern = re.compile('[\\\/:"<>|\*\?]')  # 去掉歌名中的非法符号
        result = re.findall(pattern, tet)
        if result:
            for i in result:
                tet = tet.replace(i, '')
            return tet
        else:
            return tet

    def parse(self, response):
        qi_shu = response.css('span.vol-number.rounded::text').extract_first()
        pic_url = response.css('img.vol-cover::attr(src)').extract_first()[:-14]
        pic_name = response.css('img.vol-cover::attr(alt)').extract_first()

        ge = LuooItem()
        ge['qi_shu'] = qi_shu
        down_links = [pic_url]
        music_name = [pic_name]

        for each in response.css('div.musiclist li'):
            musicn = each.css('a.play::text').extract_first()[4:]
            musicn = self.del_illegal(musicn)
            downlink = each.css('a.download::attr(href)').extract_first()[5:]
            down_links.append(downlink)
            music_name.append(musicn)
            self.ge_counts += 1
        # 图片也是文件，在此加上图片链接，一并下载下来
        ge['file_urls'] = down_links  # 可以是列表
        ge['music_name'] = music_name  # 可以是列表，进行一一对应，以便后面调取
        yield ge  # 可以在循环之外

        self.counts += 1
        if self.counts < self.total_qi:
            next_url = response.urljoin(response.xpath('//a[text()="「往期」"]/@href').extract_first())
            yield scrapy.Request(next_url, callback=self.parse)
        else:
            print(f'***********预计将下载{self.counts}期共{self.ge_counts}首歌曲{self.counts}张封面图片***********')
