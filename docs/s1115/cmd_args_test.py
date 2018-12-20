#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Terry'

import sys

if __name__ == '__main__':
    print('测试cmd参数')
    print(sys.argv)
    name = input('请输入名字:')
    print(name)
    print('测试结束')