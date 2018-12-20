#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

__author__ = 'Terry'

import redis
import pymongo

def redis_2_mongo():
    """ 将 item 数据从 redis 转移到 mongodb

    :return:
    """

    # 构造 mongodb 的 连接
    client = pymongo.MongoClient(host='127.0.0.1', port=27017)
    db = client['s1808']
    coll = db['dingdian_redis']

    # 构造 redis的连接
    redis_conn = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)

    while 1:
        # 从 item 的 list 中 弹出一个元素
        item = redis_conn.lpop('dingdian:items')

        # 如果 item 为 空， 即表示已经取完， 那么退出当前 while 循环
        if not item:
            break

        # 将 item 从 json字符串 转换为  dict 对象
        item = json.loads(item)

        # 将 item 字典对象 写入到 mongodb 中
        coll.insert(item)

    # 关闭 mongodb 的连接
    client.close()

if __name__ == '__main__':
    redis_2_mongo()