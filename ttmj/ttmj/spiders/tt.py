# -*- coding: utf-8 -*-
import re

import requests
import scrapy
from scrapy import Selector
from scrapy.http import FormRequest

from .waigua import MiMa

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/68.0.3440.106 Safari/537.36'}



def find_name():
    '''
    在登录之前，先看看用户输入的tv名称是否能够找到，找不到重新输入
    '''
    while True:
        tvname = input('请输入你想看的tv名:   （模糊匹配）')
        pages_num = int(input('你希望最多搜寻多少页数:'))

        for i in range(1, pages_num + 1):
            url = f'http://www.ttmeiju.vip/index.php/summary/index/p/{i}.html'
            response = requests.get(url, headers=headers)
            response = response.text
            if tvname not in response:
                print(f'*************搜寻了第{i}页，无果！*************')
                continue
            else:
                sel = Selector(text=response)
                tv_url = sel.xpath(f'//a[contains(text(),"{tvname}")]/@href').extract()  # todo:若有多个匹配
                print(f'找到了{len(tv_url)}个疑似匹配结果：')
                for m, n in enumerate(tv_url):
                    pattern = re.compile(r'meiju/(.*?).html')
                    n = re.findall(pattern, n)[0]
                    print(f'{m}:{n}')
                    print('999：全部都要')
                tv_num = int(input('请输入你想要的对应的数字：'))
                if tv_num == 999:
                    return tv_url
                return [tv_url[tv_num]]
        print(f'*************查询了{pages_num}页都没找到,尝试输入精准名字，并扩大搜索页数吧！*************')


url_list = find_name()


class TtSpider(scrapy.Spider):
    name = 'tt'
    allowed_domains = ['ttmeiju.vip']

    start_urls = [f'http://www.ttmeiju.vip/{url}' for url in url_list]

    login_url = 'http://www.ttmeiju.vip/index.php/user/login.html'

    def start_requests(self):  # 重写该方法
        '''
        准备登录
        '''
        log = {'username': MiMa.username,
               'password': MiMa.password,
               'loginsubmit': '登录'}
        unicornHeader = {'Host': 'www.ttmeiju.vip', 'Referer': 'http://www.ttmeiju.vip/', }
        yield FormRequest(self.login_url, headers=unicornHeader, method='POST', callback=self.login_or_not,
                          formdata=log)

    def login_or_not(self, response):
        '''登陆成功，调用原start_requests方法执行parse'''
        yield from super().start_requests()

    def parse(self, response):
        '''
        登陆之后执行的内容
        '''
        # print(response.text)
        infos = response.css('tbody#seedlist tr')
        for info in infos:
            name = info.xpath('string(.//td[@align="left"]/a)').extract()[0].strip()
            init_url = info.css('[title=百度云盘下载]::attr(href)').extract()
            code = info.css('td:nth-child(5)::text').extract()
            zimu = info.css('td:nth-child(8)').xpath('string(.)').extract_first()
            if '无' in zimu: continue
            if not init_url:
                print(f'{name}没有百度云盘链接，请到{self.start_urls}自行查找其他链接')
                continue
            yield scrapy.Request(init_url[0], callback=self.parse_tv, dont_filter=True,
                                 meta={'初链': init_url, '提取码': code, '名字': name})

    def parse_tv(self, response):
        url = response.url
        name = response.meta['名字']
        code = response.meta['提取码']
        if '无法访问' in response.text:
            print(f'目测已被删除：{url}')
        elif '失效时间' in response.text:
            print(f'恭喜！{name}直接观看地址:{url}')
        elif '提取密码' in response.text:
            print(f'提取码{code}输入观看{name}，地址：{url}')
        else:
            print('发现了UFO!你已被外星人ET劫持！')
