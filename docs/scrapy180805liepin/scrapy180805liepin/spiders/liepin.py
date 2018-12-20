#!/usr/bin/env python
# -*- coding: utf-8 -*-
from urllib.parse import quote

from scrapy180805liepin.items import Scrapy180805LiepinItem

__author__ = 'Terry'

import scrapy

class LiepinSpdier(scrapy.Spider):

    name = 'liepin'

    start_urls = ['https://www.liepin.com/']

    def parse(self, response):
        keywords = self.settings['KEYWORDS']

        for keyword in keywords:
            url = f'https://www.liepin.com/zhaopin/?key={quote(keyword)}&d_pageSize=40&curPage=0'

            yield scrapy.Request(url, callback=self.parse_list, meta={'keyword':keyword})

    def parse_list(self, response):
        keyword = response.meta['keyword']

        # url = '/zhaopin/?init=-1&headckid=ed0317a3a26505fe&fromSearchBtn=2&ckid=ed0317a3a26505fe&degradeFlag=0&key=python%E7%88%AC%E8%99%AB&siTag=tF7woi2y6F2s2RnHW3wfUw%7EfA9rXquZc5IkJpXC-Ycixw&d_sfrom=search_unknown&d_ckId=801e0be349a377f373720911fc6fda33&d_curPage=0&d_pageSize=40&d_headId=801e0be349a377f373720911fc6fda33&curPage=4'
        text = response.text
        import re
        last_page = re.search(r'<a.*?class="last".*?href=".*?&curPage=(\d+)"', text).group(1)

        last_page = int(last_page)

        for i in range(last_page):
            url = f'https://www.liepin.com/zhaopin/?key={quote(keyword)}&d_pageSize=40&curPage={i}'

            yield scrapy.Request(url, callback=self.parse_position, dont_filter=True, meta=response.meta)

    def parse_position(self, response):

        position_urls = response.xpath('//div[@class="job-info"]/h3/a/@href').extract()
        positions = response.xpath('//div[@class="job-info"]/h3/a/text()').extract()
        companys = response.xpath('//*[@class="company-name"]/a/text()').extract()

        condition_clearfixs = response.xpath('//p[@class="condition clearfix"]/@title').extract()

        position_times = response.xpath('//time/@title').extract()

        for url, position, company, condition_clearfix, position_time in zip(position_urls, positions, companys, condition_clearfixs, position_times):
            next_meta = response.meta
            next_meta['position'] = position
            next_meta['company'] = company
            next_meta['condition_clearfix'] = condition_clearfix
            next_meta['position_time'] = position_time

            # response.follow  和  scrapy.Request 的区别就是会自动使用 response的 域名
            yield response.follow(url, callback=self.parse_detail, meta=next_meta, dont_filter=True)

    def parse_detail(self, response):

        meta = response.meta

        item = Scrapy180805LiepinItem()

        item['position'] = meta['position'].strip()
        item['company'] = meta['company'].strip()

        condition_clearfix = meta['condition_clearfix']
        condition_clearfix = condition_clearfix.split('_')
        item['salary'] = condition_clearfix[0]
        item['city'] = condition_clearfix[1]
        item['edu'] = condition_clearfix[2]
        item['work_year'] = condition_clearfix[3]

        def format_time(t):
            # 2018年09月06日  : 2018-09-06
            return t.replace('年', '-').replace('月', '-').replace('日', '')

        item['position_time'] = format_time(meta['position_time'])
        item['keyword'] = meta['keyword']

        content_word = response.xpath('//div[@class="content content-word"]/text()').extract()
        content_word = ''.join(content_word).replace(' ', '').replace('\t', '').replace('\n', '').replace('\r', '')
        item['position_detail'] = content_word

        item['url'] = response.url

        yield item

