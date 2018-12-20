#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Terry'

import http.client


def http_get(url):
    # 打开一个HTTPS连接
    conn = http.client.HTTPSConnection(url)
    # 发送一个 GET 请求 ，path是 /
    conn.request("GET", "/")
    # 得到服务器的 响应对象
    r = conn.getresponse()
    # 得到 response 的 响应体
    data = r.read()

    return data.decode()

if __name__ == '__main__':
    text = http_get('www.baidu.com')
    print(text)