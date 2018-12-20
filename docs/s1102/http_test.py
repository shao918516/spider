#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Terry'

import http.client

# 打开一个HTTPS连接
conn = http.client.HTTPSConnection("www.python.org")
# 发送一个 GET 请求 ，path是 /
conn.request("GET", "/")
# 得到服务器的 响应对象
r1 = conn.getresponse()
# 输出response的 状态码和描述
print(r1.status, r1.reason)
# 得到 response 的 响应体
data1 = r1.read()  # This will return entire content.
# The following example demonstrates reading data in chunks.
# conn.request("GET", "/")
# r1 = conn.getresponse()
# while not r1.isclosed():
#     print(r1.read(200))  # 200 bytes

# Example of an invalid request
conn.request("GET", "/parrot.spam")
r2 = conn.getresponse()
print(r2.status, r2.reason)

data2 = r2.read()
conn.close()
