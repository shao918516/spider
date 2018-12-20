#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import re

headers = {
    'connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 7.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
    'Accept': 'text/html, application/xhtml+xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9'
}
params = {
    'fr': 'aladdin'
}
url = 'https://baike.baidu.com/item/人工智能/9180'
response = requests.get(url, params=params, headers = headers)
response.encoding = 'utf-8'
connect = response.text

# 获取人工智能的定义
r = 'content="(.*?)"'
definition = re.findall(r, connect, re.RegexFlag.MULTILINE|re.RegexFlag.DOTALL)
print(definition[2])
# print(connect)

# 获取目录
r2 = '<span.*?><a href="#([1-9]|[1][0-9])">(.*?)</a>'
word = re.findall(r2, connect, re.RegexFlag.MULTILINE|re.RegexFlag.DOTALL)
for i in word:
    print(i[1])


