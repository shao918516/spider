#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Bi Harword'

import requests
import re

# from urllib import parse
url = "https://www.zhihu.com/search"
params = {
    "q": "S8总决赛",
    "utm_content": "search_hot",
    "type": "content"

}
headers = {
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 7.0; Win64; x64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
    "Accept": "*/*;q=0.8",
    "Accept-Encoding": "",
    "Accept-Language": "zh-CN,zh;q=0.9",
}
rep = requests.get(url, params=params, headers=headers)
# print(req.content)
rep.encoding = "utf_8"
print(rep.status_code, rep.reason)
reason = rep.text
# print(type(reason))
# print(req.content)
reason=reason.replace("\\\\u","\\u")
# reason=reason.encode().decode()
# # reason=parse.urlencode(reason)
print(reason)


# title_list=re.findall("\"title\":.*?\"}",reason)
# print(title_list)
