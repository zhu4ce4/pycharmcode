# -*- coding: utf-8 -*-
import re

import scrapy

from ..items import PybookItem


class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    allowed_domains = ['www.amazon.cn']
    start_urls = [
        'https://www.amazon.cn/s/ref=sr_pg_2?rh=n%3A658390051%2Ck%3Apython&page=1&keywords=python&ie=UTF8&qid=1534832397']  # 默认
    # 'https://www.amazon.cn/s/ref=sr_pg_2?rh=n%3A658390051%2Ck%3Apython&page=2&keywords=python&ie=UTF8&qid=1534832397']  #默认
    # 'https://www.amazon.cn/s/ref=sr_pg_3?rh=n%3A658390051%2Ck%3Apython&page=1&sort=date-desc-rank&keywords=python&ie=UTF8&qid=1534816867']    #出版时间优先
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}

    def replacesth(self, sth):
        return sth.replace(' ', '').replace('\n', '').replace('\t', '').replace('–', '')

    def parse(self, response):
        infos = response.css('li.s-result-item.celwidget  ')  # 必须首先每本书每本书地进行判断
        pattern = re.compile('[\u4e00-\u9fa5]')  # 视图匹配中文
        for info in infos:
            name = info.css('h2::text').extract_first()
            if re.search(pattern, name):
                dianzishu_pass = info.css('div.a-row.a-spacing-none a h3::text').extract()
                if '电子书' not in dianzishu_pass[0]:
                    book_link = info.xpath('.//h2/../@href').extract_first()
                    if len(dianzishu_pass) > 1:
                        if '电子书' in dianzishu_pass[1]:
                            yield scrapy.Request(book_link, callback=self.parse_book, headers=self.headers,
                                                 meta={'name': name, 'dianzi_version': True, 'link': book_link})
                    else:
                        yield scrapy.Request(book_link, callback=self.parse_book, headers=self.headers,
                                             meta={'name': name, 'dianzi_version': False, 'link': book_link})
                else:
                    print(f'{name:50s} 是电子书')
                    continue
            else:
                print(f'发现一本外文书{name:50s}')
                continue

        # if response.css('a#pagnNextLink::attr(href)').extract_first():
        #     next_url = 'https://www.amazon.cn' + response.css('a#pagnNextLink::attr(href)').extract_first()
        #     yield scrapy.Request(next_url, callback=self.parse, headers=self.headers)

    def parse_book(self, response):
        # name=response.meta['name']  #也可使用name=title[0]获取书名
        title = response.xpath('string(.//h1[@id="title"])').extract_first()
        title = self.replacesth(title).split('Tapablanda')  # 可以这样调用函数
        name = title[0]
        # name=response.xpath('string(.//h1[@id="title"])').extract_first().replace(' ','').replace('\n','').replace('–','').split('Tapablanda')[0]
        ma = response.xpath('//b[text()="条形码:"]/../text()').extract_first().strip()
        pub_comp = response.xpath('//b[text()="出版社:"]/../text()').extract_first().strip()
        # pub_date=response.xpath('string(.//h1[@id="title"])').extract_first().replace(' ','').replace('\n','').replace('–','').split('Tapablanda')[1]
        pub_date = title[1]
        author = response.xpath('string(.//div[@id="bylineInfo"])').extract_first()
        author = self.replacesth(author)  # todo：怎样用一行代码写完本行及上一行代码
        dianzi_version = response.meta['dianzi_version']
        star_find = response.css(
            'div#averageCustomerReviews_feature_div i.a-icon.a-icon-star span::text').extract_first()
        avg_star = star_find[2:] if star_find else '没有star'
        base_price = response.css('div#buyBoxInner span.a-color-secondary::text').extract()
        base_price = base_price[1] if base_price else '暂无定价'
        sale_price = response.css('div#buyNewSection span:nth-child(2)::text').extract_first()
        sale_price = sale_price if sale_price else '暂无售价'
        comments_num = response.css(
            'div#averageCustomerReviews_feature_div span#acrCustomerReviewText::text').extract_first()
        comments_num = comments_num if comments_num else '暂无评论'
        ziying = response.css('i.detail_badge_sba::text').extract_first()
        ziying = True if ziying == '自营' else False
        star4 = int(response.xpath('//*[text()="4 星"]/../following-sibling::td[2]//text()').extract_first()[:-1])
        star5 = int(response.xpath('//*[text()="5 星"]/../following-sibling::td[2]//text()').extract_first()[:-1])
        star45_prob = str(star4 + star5) + '%'
        link = response.meta['link']

        book = PybookItem()
        book['书名'] = name
        book['出版日期'] = pub_date
        book['出版社'] = pub_comp
        book['条形码'] = ma
        book['作者'] = author
        book['有电子书'] = dianzi_version
        book['平均分'] = avg_star
        book['定价'] = base_price
        book['售价'] = sale_price
        book['评论数'] = comments_num
        book['是自营'] = ziying
        book['四五星'] = star45_prob
        book['链接'] = link
        yield book
