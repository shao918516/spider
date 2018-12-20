#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Terry'


# s = '中文测试中文测试中文测试中文测试'
#
# print(s.encode('utf-8'))
# print('gbk:', s.encode('utf-8').decode('gbk', 'ignore'))
# print('gbk:', s.encode('utf-8').decode('gbk', 'ignore').encode('gbk').decode('utf-8', 'ignore'))


# s = '喟班鞍'
#
# print(s.encode('gbk'))
# print('gbk:', s)
# print('utf-8:', s.encode('gbk').decode('utf-8'))

s = '中文测试中文测试中文测试中文测试'

# print(s.encode('utf-8'))
# 不加参数，出现 UnicodeDecodeError
# print('gbk:', s.encode('utf-8').decode('gbk'))
# 忽略错误的字节6
print('gbk:', s.encode('utf-8').decode('gbk', 'ignore'))
# 用 一个 � 字符替换掉错误的字节
print('gbk:', s.encode('utf-8').decode('gbk', 'replace'))
# 用 xml 的字符替换错误的字节  &#a5fx;
# print('gbk:', s.encode('utf-8').decode('gbk', 'xmlcharrefreplace'))
