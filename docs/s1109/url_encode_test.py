#!/usr/bin/env python
# -*- coding: utf-8 -*-
from urllib.parse import urlencode

__author__ = 'Terry'

''''
    URL编码解码：
    用于url的参数提交
    中文、特殊字符 转换为 %B3%3B%53。。。。。。
'''
from urllib import parse

s = '#%&+='
# 默认编码为UTF-8
s1 = parse.quote(s) # 编码
print(s1)
s2 = parse.unquote('%2b') # 解码
print(s2)
d = {
    'k1': '中文',
    'k2': 'fab123'
}
# 将字典转换为 url 的get 参数串
print(urlencode(d))