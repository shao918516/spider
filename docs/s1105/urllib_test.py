#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time

__author__ = 'Terry'

from urllib import request
# start = time.time()

# GET方式请求一个url
# response = request.urlopen(r'http://www.baidu.com/')
# html = response.read()
# text = html.decode('utf-8')
# print(text)
# print('共用： %s 秒' % (time.time() - start))


# 经常会连起来使用
# text = request.urlopen(r'http://www.baidu.com').read().decode()
# print(text)


"""
    Request 对象
"""
start = time.time()
url = r'http://www.baidu.com/'
headers = {
    'User-Agent': r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
    'Referer': r'http://www.baidu.com/',
    'Connection': 'keep-alive'
}
# 指定 请求头
req = request.Request(url, headers=headers)
page = request.urlopen(req).read().decode('utf-8')
print(page)
print('共用： %s 秒' % (time.time() - start))


