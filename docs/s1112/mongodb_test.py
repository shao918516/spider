#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Terry'

import pymongo

if __name__ == '__main__':
    # 往 s1808数据库的  lagou 集合  写入一条任意记录
    client = pymongo.MongoClient('localhost', port=27017)

    # 得到 数据库
    # db = client['s1808']
    db = client.s1808

    # 得到集合
    # coll = db['lagou']
    coll = db.lagou

    # 写入数据  name=terry, age=18
    coll.insert({'name': 'terry', 'age': 18})
