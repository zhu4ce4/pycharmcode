# -*- coding: utf-8 -*-
import scrapy

from ..items import LuooItem


class LuoSpider(scrapy.Spider):
    name = 'luo'
    allowed_domains = ['luoo.org']
    start_urls = ['http://www.luoo.org/music/993.html']
    counts = 0

    def parse(self, response):
        qi_shu = response.css('span.vol-number.rounded::text').extract_first()
        for each in response.css('div.musiclist li'):
            music_name = each.css('a.play::text').extract_first()[4:]
            singer = each.xpath('./text()').extract_first()
            down_link = each.css('a.download::attr(href)').extract_first()[5:]

            ge = LuooItem()
            ge['file_urls'] = [down_link]
            ge['qi_shu'] = qi_shu
            ge['music_name'] = music_name
            ge['singer'] = singer
            yield ge

        self.counts += 1
        if self.counts < 2:
            next_url = response.urljoin(response.xpath('//a[text()="「往期」"]/@href').extract_first())
            yield scrapy.Request(next_url, callback=self.parse)

# todo:按期数分文件夹下载歌曲，总共下载不超过5期
