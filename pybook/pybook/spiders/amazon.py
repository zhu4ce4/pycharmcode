# -*- coding: utf-8 -*-
import re

import scrapy


class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    allowed_domains = ['www.amazon.cn']
    start_urls = [
        'https://www.amazon.cn/s/ref=sr_pg_3?rh=n%3A658390051%2Ck%3Apython&page=1&sort=date-desc-rank&keywords=python&ie=UTF8&qid=1534816867']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}

    def parse(self, response):
        infos = response.css('li.s-result-item.celwidget  ')  # 必须首先每本书每本书地进行判断
        pattern = re.compile('[\u4e00-\u9fa5]')
        for info in infos:
            name = info.css('h2::text').extract_first()
            if re.search(pattern, name):
                dianzishu_ornot = info.css('h3::text').extract_first()
                if '电子书' not in dianzishu_ornot:
                    book_link = info.xpath('.//h2/../@href').extract_first()
                    yield book_link
                else:
                    continue
            else:
                continue

        if response.css('a#pagnNextLink::attr(href)').extract_first():
            next_url = 'https://www.amazon.cn' + response.css('a#pagnNextLink::attr(href)').extract_first()
            yield scrapy.Request(next_url, callback=self.parse, headers=self.headers)
