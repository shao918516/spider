#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Terry'

import requests

# 一般不会使用 request 方法
# response = requests.request('GET', 'http://www.baidu.com')
# print(response.text)

# 一般使用 GET 方法替代
response = requests.get('http://www.baidu.com')

# content 得到 响应的bytes
print(response.content)

# text  得到  响应的文本字符串
print(response.encoding)  # 这里是 ISO-8859-1
print(response.text)

# 指定 text 属性的转码字符集
response.encoding = 'utf-8'
print(response.text)