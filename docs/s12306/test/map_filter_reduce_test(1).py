#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Terry'


# filter

li = [1, 2, 3, 4, 5]

li_new = filter(lambda x: x%2 == 0, li)
print(list(li_new))



# li_new = []
# for i in li:
#     if i % 2 ==0 :
#         li_new.append(i)
#
# print(li_new)