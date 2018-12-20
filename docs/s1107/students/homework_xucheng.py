#!/user/bin/env python
# -*- coding: utf-8 -*-

import requests

conn = requests.Session()
url = 'https://github.com/login'

# 这个 参数 是哪得来的？？？
postdata = {
    'username':'zhegemingzi',
    'password':'mysunshine941028'
}
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'
}
response = conn.post(url, data=postdata, headers=headers)
print(response.text)
