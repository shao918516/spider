#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Terry'



# 这是一个幂等函数， 也是一个 纯函数
def mul(a, b):
    return a*b

c = 10

# 这不是一个幂等函数
def mul_add_param(a, b):
    return a*b*c

# 这个函数是幂等函数
# 但是不是 纯函数
def mul_print(a, b):
    r = a*b
    # 改变了环境
    print('内部打印：', r)

    # 修改函数外部的变量
    global c
    c = 100

    return r

if __name__ == '__main__':
    print(mul_print(10, 2))
    c = 30
    print(mul_print(10, 2))
    print(mul_print(10, 2))
    print(mul_print(10, 2))