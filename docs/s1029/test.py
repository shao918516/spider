#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Terry'

x = 1

def func_a():
    x = 2
    def func_b():
        x = 3
        print(x)

    func_b()

func_a()