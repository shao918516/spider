#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Terry'

import urllib3
# http = urllib3.PoolManager()
# r = http.request('GET', 'http://www.baidu.com')
# print(r.data.decode())


http = urllib3.PoolManager()
headers = {
    'Cookie': 'PSTM=1541125821; BIDUPSID=CCA7745D7BD4CC91206D206D93F89FDB; BAIDUID=2E2253980F41BD6CD62E2840D3ACE383:FG=1; BD_UPN=12314753; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; pgv_pvi=9669870592; locale=zh; BDUSS=d1WTRFWGg0UUZ2cjVmY2NyQzdWR0M1VVZCdWU1bW14dzdxM2VMSzdPSThqZ2RjQVFBQUFBJCQAAAAAAAAAAAEAAAB4TynObXVtdWxvdmVzaGluZQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADwB4Fs8AeBbQU; H_PS_645EC=f06bpWTU2P%2BeOM%2FJTHtE%2Bt4ZAqVB%2B%2BAm4G0aeGr45TLTylJ%2FdHrKqXdRTTk; BD_HOME=1; H_PS_PSSID=1451_21096_20880_27400_27508'
}
r = http.request('GET', 'http://www.baidu.com', headers=headers)
print(r.data.decode())


