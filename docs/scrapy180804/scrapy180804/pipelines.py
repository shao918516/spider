# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

class DataFilterDingdianPipeline(object):

    def process_item(self, item, spider):
        """
            执行数据 清洗
        :param item:
        :param spider:
        :return:
        """
        item['author'] = item['author'].strip()
        item['status'] = item['status'].strip()
        try:
            item['words'] = int(item['words'].strip().replace('字', ''))
        except:
            item['words'] = 0
        item['last_update'] = item['last_update'].strip()
        item['clicks'] = item['clicks'].strip()
        # 将 清洗后的 item 传递给下一个 pipeline
        return item

class Scrapy180804Pipeline(object):
    def open_spider(self, spider):
        import pymongo
        self.client = pymongo.MongoClient(**spider.settings['MONGODB_CONFIG'])
        self.db = self.client['s1808']
        self.coll = self.db['dingdian1']

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.coll.insert(dict(item))

        # 如果当前 pipeline是最后一个 ，那么就是 在控制台打印输出！
        return item
