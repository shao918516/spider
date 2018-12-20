#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Terry'

# 1、安装 urllib3 和 requests
# 2、使用 requests 的 get 方法
#     访问 10 个 任意网站的 url， 需要自己填写 headers 和 params
# 3、尝试使用 re 正则表达式， 获取 网页中的指定内容

import requests
#
# headers = {
#     'Host': "www.dianping.com",
#     'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
# }
# url = "https://www.dianping.com"
# r = requests.get(url, headers=headers)
# print(r.text)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
}

# 命名错误， 应该是  params
prarms = {
    "wd": "中"
}
url = "https://www.baidu.com"
# response 、r、resp
# 这里的命名，绝对错误啊，  取了 反义词
request = requests.get(url, params=prarms, headers=headers)
request.encoding = "utf-8"
print(request.text)
