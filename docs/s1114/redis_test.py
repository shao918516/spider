#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Terry'

import redis

# decode_responses 设置为 True , 不设置为 true 的话，会操作 bytes
r = redis.Redis(host='192.168.1.121', port=6379, decode_responses=True)

# r.set('name', 'mary')

# print(r.get('name'))

print(r.getset('name', 'terry'))


