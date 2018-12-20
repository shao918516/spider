#!/usr/bin/env python
# -*- coding: utf-8 -*-
from common.requests_helper import make_session

__author__ = 'Terry'

import urllib3
urllib3.disable_warnings()


session = make_session()

response = session.get('http://www.baidu.com')

print('编码：', response.encoding)
# 手动指定一下编码
response.encoding = 'UTF-8'
print(response.text)


#  gbk  : 鐧惧害鎼滅储
#  UTF-8: 百度搜索

# s = '百度搜索'
# print(s.encode().decode('gbk'))  # 输出 鐧惧害鎼滅储
