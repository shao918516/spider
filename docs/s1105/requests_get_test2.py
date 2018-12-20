#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Terry'

import requests

# 使用headers
headers = {
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9'
}
# url 参数的使用
params = {
    'key1': 'test1',
    'key2': 'test2'
}
# url 不需要添加后续的 ? 和 url参数
url = 'http://httpbin.org/get'
response = requests.get(url, params=params, headers=headers)

print(response.text)