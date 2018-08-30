# -*- coding: utf-8 -*-
'''
@datetime: 2018/8/30 13:01
@author: Jack Luo
@job:
//todo:
'''
import datetime
import json

import scrapy
from scrapy.http import FormRequest
from scrapy.selector import Selector

from ..items import GongKaiItem


class ZtSpider(scrapy.Spider):
    name = 'zt'
    today = datetime.date.today()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
    url = 'http://www.yczyjy.cn/WebSite/CommonHandler.ashx?form=infoList&action=getSearchList&cid=undefined'

    def start_requests(self):
        # yield scrapy.Request(url,method='POST',body=str(data),headers=headers,callback=self.parse,dont_filter=True)
        for j in ['港桥', '朱沱', '松溉']:
            data = {'pageindex': '1', 'pagesize': '10', 'Key': f'{j}'}  # 此处pageindex必须为字符串，不能是整型
            yield FormRequest(self.url, method='POST', formdata=data, headers=self.headers, callback=self.parse)
            # 返回的是xmlresponse，不像requests.post 那样能否直接.json()得到，而是只能.text

    def parse(self, response):

        # resp=json.loads(response.text)  #得到text数据后用json将text给load出来变成dict
        resp = json.loads(response.body)  # 得到text数据后用json将text给load出来变成dict
        lili = resp['showinfo']  # 然后把dict里的数据取出得到text
        lili = Selector(text=lili)
        infos = lili.css('li')
        for info in infos:
            item = GongKaiItem()
            riqi = (info.css('span::text').extract_first())
            riqi = datetime.datetime.strptime(riqi, '%Y-%m-%d').date()
            if (self.today - riqi) < datetime.timedelta(6):
                title = info.css('a::text').extract_first()
                link = info.css('a::attr("href")').extract_first()

                item['biaoti'] = title
                item['link'] = link
                item['time'] = riqi
                yield item
            else:
                break
