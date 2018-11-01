# -*- coding: utf-8 -*-
import scrapy

from ..items import FipItem


class GetfipSpider(scrapy.Spider):
    name = 'getfip'
    allowed_domains = ['free-proxy-list.net']
    start_urls = ['https://free-proxy-list.net/anonymous-proxy.html']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}

    def start_requests(self):
        for iurl in self.start_urls:
            for page in range(1, 3):
                yield scrapy.Request(url=iurl, callback=self.parse, meta={'page': page}, dont_filter=True)

    def parse(self, response):
        item = FipItem()
        for each_row in response.css('tbody tr[class]'):
            if each_row.xpath('./td[7]/text()').extract_first() == 'yes':
                ipadd = each_row.xpath('./td[1]/text()').extract_first()
                port = each_row.xpath('./td[2]/text()').extract_first()
                ip = f'https://{ipadd}:{port}'
                item['httpors'] = 'https'
                item['ip'] = ip
                yield item

            else:
                ipadd = each_row.xpath('./td[1]/text()').extract_first()
                port = each_row.xpath('./td[2]/text()').extract_first()
                ip = f'http://{ipadd}:{port}'
                item['httpors'] = 'http'
                item['ip'] = ip
                yield item
