#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Terry'

# ASCII 码的部分
# print(b'\x21'.decode('utf-8'))
# print(b'\x21'.decode('gbk'))
# print(b'\x21'.decode('gb2312'))
# print(b'\x21'.decode('iso-8859-1'))

# 超出 ASCII 码的部分
print(b'\xab'.decode('iso-8859-1'))
print(b'\xab'.decode('iso-8859-2'))
print(b'\xab'.decode('iso-8859-3'))
print(b'\xab'.decode('iso-8859-4'))