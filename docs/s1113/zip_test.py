#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Terry'

li1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
li2 = ['a', 'b', 'c', 'd', 'e']
li3 = ['a1', 'b2', 'c3', 'd4', 'e5']

li_new = zip(li1, li2, li3)

print(list(li_new))

# for i,j,k in zip(li1, li2, li3):
#     print(i)
#     print(j)
#     print(k)
