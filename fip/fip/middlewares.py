# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class SeleniumMiddleware():
    def __init__(self):
        self.options = Options()
        self.options.binary_location = r"C:\Chromium\chrome.exe"
        self.timeout = 8
        self.br = webdriver.Chrome(chrome_options=self.options)
        self.wait = WebDriverWait(self.br, self.timeout)

    def __del__(self):
        self.br.close()

    def process_request(self, request, spider):
        try:
            self.br.get(request.url)
            self.br.maximize_window()
            js = "var q=document.documentElement.scrollTop=300"
            self.br.execute_script(js)
            aclick = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.dataTables_length>label>select')))
            aclick.click()
            bclick = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.dataTables_length>label>select>option:nth-child(3)')))
            bclick.click()
            if request.meta.get('page') > 1:
                self.br.find_element_by_link_text('Next').click()
            return HtmlResponse(url=request.url, body=self.br.page_source, request=request, encoding='utf8', status=200)
            # next=self.br.find_element_by_css_selector('li.next.disabled')
            # print("*****")
            # print(next)
            # if next:
            #     break
            # else:
            #     self.br.find_element_by_link_text('next').click()
            #     yield HtmlResponse(url=request.url, body=self.br.page_source, request=request, encoding='utf8',//不能用yield！！
            #                        status=200)
        except TimeoutException:
            return HtmlResponse(url=request.url, status=500, request=request)


class FipSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class FipDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
