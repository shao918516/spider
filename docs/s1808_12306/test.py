#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Terry'

if __name__ == '__main__':

    s = '12345678'
    s1 = '49,35,117,42,190,39,255,33,38,107,116,113,189,111,266,118'

    s2 = '1357'
    s4 = '42,42,182,36,40,113,180,108'

    import time
    t = time.time()  # 单位秒， 小数点前是 10位，

    print(t)
    # 1542357921445
    print(str(int(t*1000)))