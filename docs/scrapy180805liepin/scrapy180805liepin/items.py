# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Scrapy180805LiepinItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    keyword = scrapy.Field()
    position = scrapy.Field()
    company = scrapy.Field()
    salary = scrapy.Field()
    city = scrapy.Field()
    edu = scrapy.Field()
    work_year = scrapy.Field()
    position_time = scrapy.Field()
    position_detail = scrapy.Field()
    url = scrapy.Field()
