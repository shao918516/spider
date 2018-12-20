#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Terry'


def identity(x):
    return x

def func_a(a, b, c=None, process_request=identity, process_response=lambda x: x):
    if c:
        a = c(a)

    a = process_request(a)
    a = process_response(a)
    print('b:', b)
    print('处理后的a：', a)

if __name__ == '__main__':
    # 这样调用，没错
    # func_a(3, 'aa', c=lambda x: x*2, process_request=lambda x: x**2)

    # 这样调用，抛出异常：TypeError: 'NoneType' object is not callable
    # func_a(3, 'aa', process_request=lambda x: x**2)

    # 这样调用， 正常吗？
    func_a(3, 'aa', c=lambda x: x * 2)