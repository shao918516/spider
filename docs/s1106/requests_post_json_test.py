#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Terry'

import requests

headers = {
    'User-Agent': r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  r'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
    'Referer': r'http://httpbin.org',
    'Connection': 'keep-alive'
}
json_data = {
    'key1': 'value1',
    'key2': 'value2'
}
url = 'http://httpbin.org/post'
r = requests.post(url, json=json_data, headers=headers, proxies={'http': '127.0.0.1:8888'})
print(r.text)

