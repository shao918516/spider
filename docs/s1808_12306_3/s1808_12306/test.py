#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
__author__ = 'Terry'

def format_train_date(train_date):
    """ 将 2018-12-17 格式转为 Mon Dec 17 2018 00:00:00 GMT+0800 (中国标准时间)

    :param train_date:
    :return:
    """
    date_tup = tuple([int(d) for d in train_date.split('-')] + [0,0,0,0,0,0])
    train_date = time.asctime(date_tup).replace('00:00:00 ', '') + ' 00:00:00 GMT+0800 (中国标准时间)'

    return train_date

def format_date(date):
    struct_time = time.strptime(date, '%Y-%m-%d')
    return time.strftime('%a %b %d %Y', struct_time) + ' 00:00:00 GMT+0800 (中国标准时间)'

    # date_li = train_date.split('-')
    # return time.asctime(date_li + [0,0,0,0,0,0])

if __name__ == '__main__':

    # s = '12345678'
    # s1 = '49,35,117,42,190,39,255,33,38,107,116,113,189,111,266,118'
    #
    # s2 = '1357'
    # s4 = '42,42,182,36,40,113,180,108'
    #
    # import time
    # t = time.time()  # 单位秒， 小数点前是 10位，
    #
    # print(t)
    # # 1542357921445
    # print(str(int(t*1000)))

    # 2018-12-17 转： 'Mon Dec 17 2018 00:00:00 GMT+0800 (中国标准时间)'
    print(format_train_date('2018-12-17'))