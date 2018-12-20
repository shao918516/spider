#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Terry'


def func_test(a, b, *args, k=None, j=0, **kwargs):
    """
    :param a:   第一个位置参数！
    :param b:   第二个位置参数！
    :param args:   可变位置参数， 元组类型
    :param k:   第一个 默认参数， 关键字参数
    :param j:   第二个 默认参数， 关键字参数
    :param kwargs:   可变关键字参数，  字典类型
    :return:
    """
    print(a)
    print(b)
    print(args)
    print(k)
    print(j)
    print(kwargs)

def func_b(a, b, k=None, j=0):
    print(a)
    print(b)
    print(k)
    print(j)

def func_c(a, b, *, k=None, j=0):
    print(a)
    print(b)
    print(k)
    print(j)

if __name__ == '__main__':
    # func_test(1, 2, 3, 4, 5, k='k参数', m='m参数', n='n参数')

    # func_b(1, 2, k='k参数', j=12)
    # func_b(1, 2, j=12, k='k参数')
    # func_b(1, 2, 'k参数', 10)

    # func_c(1, 2, 'k参数', 10) # 是错误的
    func_c(1, 2, k='k参数', j=10)