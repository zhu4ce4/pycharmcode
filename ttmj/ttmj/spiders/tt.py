# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest


class TtSpider(scrapy.Spider):
    name = 'tt'
    allowed_domains = ['ttmeiju.vip']
    start_urls = ['http://www.ttmeiju.vip/meiju/THE.Walking.Dead.html']

    def parse(self, response):
        # print(response.text)
        infos = response.css('tbody#seedlist tr')
        for info in infos:
            name = info.xpath('string(.//td[@align="left"]/a)').extract()[0].strip()
            init_url = info.css('[title=百度云盘下载]::attr(href)').extract()
            code = info.css('td:nth-child(5)::text').extract()
            zimu = info.css('td:nth-child(8)').xpath('string(.)').extract_first()
            if '无' in zimu: continue
            if not init_url:
                print(f'{name}没有百度云盘链接，请到{self.start_urls}自行查找链接')
                continue
            yield scrapy.Request(init_url[0], callback=self.parse_tv, dont_filter=True,
                                 meta={'初链': init_url, '提取码': code, '名字': name})

    def parse_tv(self, response):
        url = response.url
        name = response.meta['名字']
        code = response.meta['提取码']
        if '无法访问' in response.text:
            print(f'可能已被删除：{url}')
        elif '失效时间' in response.text:
            print(f'恭喜你可以直接观看{name},地址:{url}')
        elif '提取密码' in response.text:
            print(f'请输入提取码{code}观看{name}，地址：{url}')

    login_url = 'http://www.ttmeiju.vip/index.php/user/login.html'

    def start_requests(self):  # 重写该方法
        log = {'username': '天天往事',
               'password': 'tian1tian1wang3shi4',
               'loginsubmit': '登录'}
        unicornHeader = {
            'Host': 'www.ttmeiju.vip',
            'Referer': 'http://www.ttmeiju.vip/',
        }
        yield FormRequest(self.login_url, headers=unicornHeader, method='POST', callback=self.login_or_not,
                          formdata=log)

    def login_or_not(self, response):

        yield from super().start_requests()

# fetch('http://www.ttmeiju.vip/meiju/Better.Call.Saul.html')
