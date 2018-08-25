# -*- coding: utf-8 -*-
import scrapy

from ..items import YcltItem


class YcSpider(scrapy.Spider):
    name = 'yc'
    allowed_domains = ['bbs.cqyc.net/']
    start_urls = [
        'http://bbs.cqyc.net/search.php?mod=forum&searchid=509&orderby=lastpost&ascdesc=desc&searchsubmit=yes&page=1']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, meta={'cookiejar': 'chrome'}, callback=self.parse)

    def parse(self, response):
        infos = response.css('div#threadlist li.pbw')
        item = YcltItem()
        for info in infos:
            title = info.xpath('string(.//a)').extract_first()
            link = info.css('a::attr(href)').extract_first()
            item['title'] = title
            item['link'] = link
            yield item
