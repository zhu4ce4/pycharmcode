# -*- coding: utf-8 -*-
import datetime

import scrapy

from ..items import GongKaiItem


class GongkaiSpider(scrapy.Spider):
    name = 'gongkai'
    allowed_domains = ['yc.cq.gov.cn']
    start_urls = ['http://yc.cq.gov.cn/zfgk/zfxxgkpt/zfxxgkml/list.html?']
    today = datetime.date.today()
    page = 0

    # headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}

    def parse(self, response):
        infos = response.css('div.boxcon div.xxgk_wrap')
        for i in infos:
            riqistr = i.css('ul li.w100 span::text').extract_first()
            riqi = datetime.datetime.strptime(riqistr, '%Y-%m-%d').date()
            # biaoti=i.css('li.w353 a::text').extract()[0]
            biaoti = i.css('div.hover_box>p:nth-child(2) span::text').extract_first()
            if (self.today - riqi) < datetime.timedelta(2):
                for j in ['朱沱', '松溉', '何埂', '港桥']:
                    if (biaoti.find(j) >= 0):
                        link = 'http://yc.cq.gov.cn/zfgk/zfxxgkpt/zfxxgkml/' + i.css(
                            'ul li.w353 a::attr(href)').extract_first()[2:]
                        item = GongKaiItem()
                        item['biaoti'] = biaoti
                        item['link'] = link
                        item['time'] = riqistr
                        yield item
            else:
                break

        zuihouderiqi = infos[-1].css('li.w100 span::text').extract_first()
        zuihouderiqi = datetime.datetime.strptime(zuihouderiqi, '%Y-%m-%d').date()
        if (self.today - zuihouderiqi) < datetime.timedelta(2):
            self.page += 1
            next_url = f'http://yc.cq.gov.cn/zfgk/zfxxgkpt/zfxxgkml/list_{self.page}.html'  # 此处的self.count调用的是上一行自增后的值，而非count=0
            yield scrapy.Request(next_url, callback=self.parse)
