# -*- coding: utf-8 -*-
'''
@datetime: 2018/8/29 15:59
@author: Jack Luo
@job:
//todo:运用splash结合lua_script提取javascript页面
'''
# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest

from ..items import ZhutuoItem

lua_script = """
function main(splash,args)
    splash:go(args.url)
    splash:wait(1)
    for i=2,7 do
        splash:select("li.nav_item:nth-child".."("..string.format("%d",i)..")").mouse_hover({x=-2, y=-2})
        splash:wait(0.5)
    end
    return splash:html()
end
"""


class MoneynewsSpider(scrapy.Spider):
    name = 'moneynews'
    allowed_domains = ['money.163.com/']
    start_urls = ['http://money.163.com/']

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, endpoint='execute', args={'lua_source': lua_script})

    def parse(self, response):
        item = ZhutuoItem()
        for sel in response.css('li.newsdata_item div.ndi_main')[:7]:
            title = sel.xpath('.//h3/a/text()').extract()[:5]
            # title=sel.xpath('string(.//h3/a)').extract_first()
            link = sel.xpath('.//h3/a/@href').extract()[:5]
            item['title'] = title
            item['link'] = link
            yield item
