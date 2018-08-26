# -*- coding: utf-8 -*-
import telnetlib

import scrapy

from ..items import IpItem


class XiciipSpider(scrapy.Spider):
    name = 'xiciip'
    allowed_domains = ['xicidaili.com']
    start_urls = [f'http://www.xicidaili.com/nn/{i}' for i in range(1, 2)]

    def parse(self, response):
        infos = response.css('table#ip_list tr')[1:]
        for info in infos:
            ip = info.css('td:nth-child(2)::text').extract_first()
            port = info.css('td:nth-child(3)::text').extract_first()
            htp = info.css('td:nth-child(6)::text').extract_first().lower()
            # test_url=f'{htp}://httpbin.org/ip'
            proxy = f'{htp}://{ip}:{port}'

            try:
                telnetlib.Telnet(ip, port=port, timeout=4)
            except:
                continue
            else:
                item = IpItem()
                item['htp'] = htp
                item['proxy'] = proxy
                yield item
            # meta={'proxy':proxy,'dont_retry':True,'download_timeout':10,'tested_htp':htp,'tested_ip':ip}
            # yield scrapy.Request(test_url,callback=self.check_available,meta=meta,dont_filter=True)
            # time.sleep(2)

    # def check_available(self,response):
    #     print(response.text)
    #     item=IpItem()
    #     tested_ip=response.meta['tested_ip']
    #     if tested_ip==json.loads(response.text)['origin']:
    #         item['htp']=response.meta['tested_htp']
    #         item['proxy']=response.meta['proxy']
    #         print(tested_ip)
