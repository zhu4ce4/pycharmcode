# -*- coding: utf-8 -*-
'''
@datetime: 2018/8/29 16:25
@author: Jack Luo
@job:
//todo:
'''
import datetime

# -*- coding: utf-8 -*-
import scrapy

from ..items import GongKaiItem


class YcSpider(scrapy.Spider):
    name = 'yc'
    allowed_domains = ['bbs.cqyc.net/']
    start_urls = [
        'http://bbs.cqyc.net/search.php?mod=forum&formhash=2cd084c1&srchtxt=%CB%C9%B8%C8&searchsubmit=yes',
        'http://bbs.cqyc.net/search.php?mod=forum&formhash=2cd084c1&srchtxt=%D6%EC%E3%FB&searchsubmit=yes',
        'http://bbs.cqyc.net/search.php?mod=forum&formhash=2cd084c1&srchtxt=%B8%DB%C7%C5&searchsubmit=yes',
        'http://bbs.cqyc.net/search.php?mod=forum&formhash=2cd084c1&srchtxt=%BA%CE%B9%A1&searchsubmit=yes']
    # 'http://bbs.cqyc.net/search.php?mod=forum&searchid=924&orderby=lastpost&ascdesc=desc&searchsubmit=yes&page=1']
    today = datetime.date.today()

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, meta={'cookiejar': 'chrome'}, callback=self.parse)

    def parse(self, response):
        infos = response.css('div#threadlist li.pbw')
        item = GongKaiItem()
        for info in infos:
            riqistr = info.css('p:nth-child(4) span:nth-child(1)::text').extract_first()
            riqi = riqistr[:-6]
            riqi = datetime.datetime.strptime(riqi, '%Y-%m-%d').date()
            if (self.today - riqi) < datetime.timedelta(6):
                title = info.xpath('string(.//a)').extract_first()
                link = info.css('a::attr(href)').extract_first()
                item['biaoti'] = title
                item['link'] = link
                item['time'] = riqistr
                return item
            else:
                break
