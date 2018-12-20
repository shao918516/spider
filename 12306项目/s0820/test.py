#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Terry'


import requests

url = 'https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand&0.5175450838314624'
r = requests.get(url)

im = r.content