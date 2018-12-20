#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scrapy.spiders import Rule

from scrapy180804.items import Scrapy180804Item

__author__ = 'Terry'

import scrapy
from scrapy.linkextractors import LinkExtractor

class DingdianSpider(scrapy.spiders.CrawlSpider):

    name = 'dingdian'

    # 一般 crawlspider 都配置 start_urls  启动
    start_urls = ['https://www.23us.so/']

    rules = (
        # 建立 follow 明确写在参数中
        Rule(LinkExtractor(allow=['/list/[0-9]+_[0-9]+.html',
                                  '/full.html',
                                  '/article/articlelist.php?fullflag=[0-9]+&page=[0-9]+']), follow=True),
        Rule(LinkExtractor(allow='/xiaoshuo/[0-9]+.html'),
             callback='parse_detail'),
    )

    def parse_detail(self, response):
        name = response.xpath('//meta[@name="keywords"]/@content').extract_first()
        book_type = response.xpath('//table[@id="at"]//a[1]/text()').extract_first()
        author = response.xpath('//table[@id="at"]/tr[1]/td[2]/text()').extract_first()
        status = response.xpath('//table[@id="at"]/tr[1]/td[3]/text()').extract_first()
        words = response.xpath('//table[@id="at"]/tr[2]/td[2]/text()').extract_first()
        last_update = response.xpath('//table[@id="at"]/tr[2]/td[3]/text()').extract_first()
        clicks = response.xpath('//table[@id="at"]/tr[3]/td[1]/text()').extract_first()

        item = Scrapy180804Item()
        item['name'] = name
        item['book_type'] = book_type
        item['author'] = author
        item['status'] = status
        item['words'] = words
        item['last_update'] = last_update
        item['clicks'] = clicks

        yield item

