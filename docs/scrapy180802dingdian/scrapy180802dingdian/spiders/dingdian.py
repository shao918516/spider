#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scrapy180802dingdian.items import Scrapy180802DingdianItem

__author__ = 'Terry'

import scrapy

class DingdianSpider(scrapy.Spider):

    name = 'dingdian'

    start_urls = [
        'https://www.23us.so/list/1_1.html',
        'https://www.23us.so/list/2_1.html',
        'https://www.23us.so/list/3_1.html',
        'https://www.23us.so/list/4_1.html',
        'https://www.23us.so/list/5_1.html',
        'https://www.23us.so/list/6_1.html',
        'https://www.23us.so/list/7_1.html',
        'https://www.23us.so/list/8_1.html',
        'https://www.23us.so/list/9_1.html',
    ]

    def parse(self, response):
        # 通过 lxml 的 xpath 获取最大页码数
        # text = response.text
        # from lxml import etree
        # tree = etree.HTML(text)
        # page_max = tree.xpath('//a[@class="last"]/text()')[0]

        # scrapy 框架在 response 对象上 提供了 xpath 方法
        # extract 提取所有
        # extract_first 提取第一个值
        page_max = response.xpath('//a[@class="last"]/text()').extract_first()

        page_max = int(page_max)

        # 第一页的 url
        url_first = response.url

        for i in range(1, page_max+1):
            url = url_first.replace('_1', f'_{i}')

            # 必须添加 dont_filter=True， 否则会丢失每一个种类的 第一页的 数据！！
            yield scrapy.Request(url, callback=self.parse_list, dont_filter=True)

    def parse_list(self, response):
        # 正则表达式提取这样的数据是非常乏力的。
        # import re
        # text = response.text
        # urls = re.findall(r'href="(https://www.23us.so/xiaoshuo/[0-9]+.html)"', text, re.RegexFlag.S)

        # xpath 提取
        urls = response.xpath('//tr[@bgcolor="#FFFFFF"]/td[1]/a/@href').extract()

        for url in urls:
            yield scrapy.Request(url, callback=self.parse_detail)

    def parse_detail(self, response):
        name = response.xpath('//meta[@name="keywords"]/@content').extract_first()
        book_type = response.xpath('//table[@id="at"]//a[1]/text()').extract_first()
        author = response.xpath('//table[@id="at"]/tr[1]/td[2]/text()').extract_first()
        status = response.xpath('//table[@id="at"]/tr[1]/td[3]/text()').extract_first()
        words = response.xpath('//table[@id="at"]/tr[2]/td[2]/text()').extract_first()
        last_update = response.xpath('//table[@id="at"]/tr[2]/td[3]/text()').extract_first()
        clicks = response.xpath('//table[@id="at"]/tr[3]/td[1]/text()').extract_first()

        item = Scrapy180802DingdianItem()
        item['name'] = name
        item['book_type'] = book_type
        item['author'] = author
        item['status'] = status
        item['words'] = words
        item['last_update'] = last_update
        item['clicks'] = clicks

        yield item


