#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from urllib.parse import quote

from scrapy180803.items import Scrapy180803Item

__author__ = 'Terry'


import scrapy

class LianjiaSpider(scrapy.Spider):

    name = 'lianjia'

    start_urls = ['https://bj.lianjia.com/']

    def parse(self, response):
        keywords = self.settings['KEYWORDS']

        for keyword in keywords:
            url = f'https://bj.lianjia.com/ershoufang/rs{quote(keyword)}/'

            # 使用 meta 传参
            yield scrapy.Request(url, callback=self.parse_list, meta={'keyword': keyword})

    def parse_list(self, response):
        # 想要知道 response 是 检索 的哪个关键字？？？
        meta = response.meta
        keyword = meta['keyword']

        text = response.text
        try:
            totalPage = re.search(r'"totalPage":([0-9]+),', text).group(1)
        except:
            totalPage = 0
            print('取不到')
        totalPage = int(totalPage)

        for i in range(1, totalPage+1):
            url = f'https://bj.lianjia.com/ershoufang/pg{i}rs{quote(keyword)}/'

            # 继续传递 meta
            yield scrapy.Request(url, callback=self.parse_ershoufang, meta=meta)

    def parse_ershoufang(self, response):
        titles = response.xpath('//div[@class="info clear"]/div[1]/a/text()').extract()
        locs = response.xpath('//div[@class="info clear"]/div[2]/div[1]/a/text()').extract()
        # houseInfo 每 5个信息 是一个 房子的 信息
        houseInfo = response.xpath('//div[@class="info clear"]/div[2]/div[1]/text()').extract()
        house_types = houseInfo[::5]
        areas = houseInfo[1::5]

        prices = response.xpath('//div[@class="info clear"]/div[4]/div[2]/div[1]/span/text()').extract()

        # 最后一页 不足30个！前面每页显示30个
        for title, loc, house_type, area, price in zip(titles, locs, house_types, areas, prices):
            item = Scrapy180803Item()
            item['title'] = title
            item['loc'] = loc
            item['house_type'] = house_type
            item['area'] = area
            item['price'] = price

            yield item

