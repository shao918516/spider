# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class Scrapy180805LiepinPipeline(object):
    def open_spider(self, spider):
        import pymongo
        self.client = pymongo.MongoClient(**spider.settings['MONGODB_CONFIG'])
        self.db = self.client[spider.settings['MONGODB_DB']]
        self.coll = self.db[spider.settings['MONGODB_COLL']]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.coll.insert(dict(item))

        return item
