# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Scrapy180804Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    book_type = scrapy.Field()
    author = scrapy.Field()
    status = scrapy.Field()
    words = scrapy.Field()
    last_update = scrapy.Field()
    clicks = scrapy.Field()
