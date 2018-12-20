#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Terry'

import redis

r = redis.Redis(host='192.168.1.121', port=6379, decode_responses=True)

# 普通的写法
# pipe = r.pipeline(transaction=True)
# pipe.set('name', 'python')
# pipe.set('age', 22)
# pipe.execute()

# 单行编写
pipe = r.pipeline(transaction=True)
pipe.set('name', 'mary').set('age', 55).execute()
