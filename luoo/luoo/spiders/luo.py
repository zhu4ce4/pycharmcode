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
        for each in response.css('div.musiclist li'):
            music_name = each.css('a.play::text').extract_first()[4:]
            music_name = self.del_illegal(music_name)
            singer = each.xpath('./text()').extract_first()
            down_link = each.css('a.download::attr(href)').extract_first()[5:]

            ge = LuooItem()
            ge['file_urls'] = [down_link]
            ge['qi_shu'] = qi_shu
            ge['music_name'] = music_name
            ge['singer'] = singer
            yield ge
            self.ge_counts += 1

        self.counts += 1
        if self.counts < self.total_qi:
            next_url = response.urljoin(response.xpath('//a[text()="「往期」"]/@href').extract_first())
            yield scrapy.Request(next_url, callback=self.parse)
        print(f'***********预计将下载{self.counts}期共{self.ge_counts}首歌曲***********')
