# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class Scrapy180801Pipeline(object):

    def open_spider(self, spider):
        """
            当爬虫类实例化时，执行的方法，
            用于 初始化 一些资源，譬如 数据库连接
        :param spider:
        :return:
        """
        import pymongo
        self.client = pymongo.MongoClient(**spider.settings['MONGODB_CONFIG'])
        self.db = self.client['s1808']
        self.coll = self.db['lagou']

    def close_spider(self, spider):
        """
            当爬虫类销毁时，执行的方法，
            用于 关闭一些资源， 譬如 数据库连接
        :param spider:
        :return:
        """

        # 关闭数据库连接
        self.client.close()

    def save_file(self, item, spider):
        with open('lagou.txt', 'a', encoding='utf-8') as f:
            f.write('----'.join([item['position_name'],
                                 item['salary'],
                                 item['company_name'],
                                 item['city']]))
            f.write('\n')

    def save_mongodb(self, item, spider):
        # item就是 dict 的子类
        self.coll.insert(dict(item))

    def process_item(self, item, spider):
        """ 将 item 数据进行持久化

        :param item:  item实例
        :param spider:  爬虫类的实例
        :return:
        """

        # 持久化到 文件
        # self.save_file(item, spider)

        # 持久化到 mongodb
        self.save_mongodb(item, spider)

        # 可以不写，但是不写的话，不会在控制台输出  item 对象
        return item
