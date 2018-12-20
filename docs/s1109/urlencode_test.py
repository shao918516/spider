#!/usr/bin/env python
# -*- coding: utf-8 -*-
from urllib.parse import quote, unquote

__author__ = 'Terry'


if __name__ == '__main__':
    s = '黄金'
    # print('原始数据：', s)
    #
    # s1 = quote(s)
    # print('一次quote：', s1)
    # print('一次quote转回原始字符串：', unquote(s1))
    #
    # s2 = quote(s1)
    # print('二次quote:', s2)
    #
    # print('二次转换的字符串，同样需要2次反编码:', unquote(unquote(s2)))

    # s_n = quote(quote(quote(quote(quote(s)))))
    # print(s_n)
    # print(unquote(unquote(unquote(unquote(unquote(s_n))))))

    su = '%3D%25E9%25BB%2584%25E9%2587%2591'
    print(unquote(unquote(su)))