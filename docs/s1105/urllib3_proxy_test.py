#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Terry'


import urllib3

# 指定代理IP
proxy = urllib3.ProxyManager('http://127.0.0.1:8888', headers={'connection': 'keep-alive'})
r = proxy.request('GET', 'http://httpbin.org/robots.txt')
print(r.status)
print(r.data)