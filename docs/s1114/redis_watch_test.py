#!/usr/bin/env python
# -*- coding: utf-8 -*-
from redis import WatchError

__author__ = 'Terry'

import redis

r = redis.Redis(host='192.168.1.121', port=6379, decode_responses=True)

with r.pipeline() as pipe:
    while True:
        try:
            # 监控 OUR-SEQUENCE-KEY  密钥
            pipe.watch('OUR-SEQUENCE-KEY')
            # 监听后，管道会进行 立刻执行命令 模式，除非我们设置为缓存模式
            # 这样允许我们获得序列的值
            current_value = pipe.get('OUR-SEQUENCE-KEY')
            next_value = int(current_value) + 1
            # 使用 multi 恢复到缓存模式
            pipe.multi()
            pipe.set('OUR-SEQUENCE-KEY', next_value)

            # 执行许多行动
            pipe.set('name', 'terry')
            pipe.incr('age')

            # 最后执行 命令
            pipe.execute()
            # 一直执行到这里，所以命令全部实现
            # 退出
            break
        except WatchError as e:
            # 另一个客户端修改了 OUR-SEQUENCE-KEY 的值，
            # 在我们监听之后，到最后 执行之前 这个时间段内
            # 回滚，重新执行
            continue
