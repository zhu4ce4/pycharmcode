# -*- coding: utf-8 -*-
import scrapy

from ..items import ZhutuoItem


class WeixinSpider(scrapy.Spider):
    name = 'weixin'
    allowed_domains = ['weixin.sogou.com']
    start_urls = [
        f'http://weixin.sogou.com/weixin?usip=&query={x}&ft=&tsn=1&et=&interation=&type=2&wxid=&page=1&ie=utf8' for x in
        ['朱沱', '松溉', '何埂', '永川港桥', '云龙机场']]
    # ['朱沱', '松溉', '何埂', '永川港桥', '云龙机场']]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        'Referer': 'http://weixin.sogou.com/weixin?usip=&query=%E6%9D%BE%E6%BA%89&ft=&tsn=1&et=&interation=&type=2&wxid=&page=2&ie=utf8'}

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, headers=self.headers, callback=self.parse)  # 必须用yield，用return报错！

    def parse(self, response):
        # for info in response.css('ul.news-list li'):
        #     biaoti=info.xpath('string(.//h3/a)').extract()
        #     link=info.css('h3 a::attr(href)').extract()
        #     yield {'标题':biaoti,'链接':link}
        linklist = response.css('ul.news-list h3 a::attr(href)').extract()
        # biaotilist=response.css('ul.news-list h3 a::text').extract()  #可行，但不能解决搜索的关键字提取不到的问题,需要使用xpath里的string
        # biaotilist=response.xpath('string(//ul[@class="news-list"]//li/div[2]/h3/a)').extract()   #为什么只能得到第一条结果呢？
        biaotilist = response.css('ul.news-list li').xpath('string(.//h3/a)').extract()  # 为什么一定要在多个li这里停留一下？？？？
        # biaotilist = response.xpath('//ul[@class="news-list"]//li').xpath('string(./div[2]/h3/a)').extract()    #效果一致
        # authorlist = response.css('ul.news-list li').xpath('string(.//a[@class="account"])').extract()
        # timeago=response.css('ul.news-list li').css('div.s-p span::text').extract()   #发布时间是javascript 数据，获取不到
        # timeago=response.css('ul.news-list li span.s2::text').extract()
        item = ZhutuoItem()
        for m, n in zip(biaotilist, linklist):
            item['biaoti'] = m
            item['link'] = n
            yield item

        next_url = response.css('div.p-fy a.np::attr(href)').extract_first()
        if next_url:
            next_url = 'http://weixin.sogou.com/weixin' + next_url
            yield scrapy.Request(next_url, callback=self.parse, headers=self.headers)

# todo:待增加爬虫;遇到ip被临时封禁的问题，需要ip代理池
