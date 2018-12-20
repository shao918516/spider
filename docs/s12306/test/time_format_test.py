#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Terry'

import time
from datetime import datetime

def date_format_12306_getQueueCount1(date_str):
    """
        转化日期函数
    :param date_str:   类似：2018-10-16
    :return:  类似：Tue Oct 16 2018 00:00:00 GMT+0800 (中国标准时间)
    """
    # 'Tue Oct 16 2018 00:00:00 GMT+0800 (中国标准时间)'
    time_li = time.asctime(time.strptime(date_str, "%Y-%m-%d")).split(" ")
    time_li[3], time_li[4] = time_li[4], time_li[3]
    str_time = ' '.join(time_li)

    return str_time + ' GMT+0800 (中国标准时间)'

def date_format_12306_getQueueCount3(date_str):
    return f'{ time.asctime(time.strptime(date_str,"%Y-%m-%d"))} GMT+0800 (中国标准时间)'

def date_format_12306_getQueueCount2(date_str):
    a = date_str.split('-')
    d = datetime(int(a[0]), int(a[1]), int(a[2]))
    str1 = str(d.ctime())
    s = str1.split(' ')
    s.insert(3, s.pop())
    train = ' '.join(s)

    return train + ' GMT+0800 (中国标准时间)'

def date_format_12306_getQueueCount(date_str):
    return time.strftime('%a %b %d %Y', time.strptime(date_str, '%Y-%m-%d')) + ' 00:00:00 GMT+0800 (中国标准时间)'


print(date_format_12306_getQueueCount1('2018-10-16'))
print(date_format_12306_getQueueCount3('2018-10-16'))
print(date_format_12306_getQueueCount2('2018-10-16'))

print(date_format_12306_getQueueCount('2018-10-16'))