#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Terry'


from urllib import parse

"""
    urllib 的parse 模块， 3个方法，是我们使用频率最高的
    
    quote
    unquote
    urlencode
"""
# quote
# 将 中文和特殊字符 转化为  %E7 这样的编码格式， url编码
# s = '中文abc!@#$%^&*() _+\\'
# print('quote:', parse.quote(s))

# unquote
# 将 类似 %E7 这样的编码， 转为普通的 str
# url = 'https://s.taobao.com/search?q=%E7%9A%AE%E9%9E%8B+%E9%BB%91+%E7%94%B7&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.1000386.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306&bcoffset=-24&ntoffset=-24&p4ppushleft=1%2C48&s=440'
# print('unquote:', parse.unquote(url))

# urlencode
# 将一个 dict 转为  key=value&key1=value1  这样的格式，同时进行 url编码
params = {
    'key1': '测试参数1',
    'key2': '@#$%^&*(',
    'key3': 100
}
print('urlencode:', parse.urlencode(params))


