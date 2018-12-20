#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Terry'


import urllib3

# 指定了 顶级域名
http_pool = urllib3.HTTPConnectionPool('httpbin.org')
# 只能指定 path
r = http_pool.urlopen('GET', 'http://www.baidu.com/robots.txt')
print(r.status)
print(r.data)
#不允许访问host之外的url