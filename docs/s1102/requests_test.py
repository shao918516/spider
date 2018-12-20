#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Terry'

import requests

r = requests.get('http://www.baidu.com')

print(r.text)


r.encoding = 'UTF-8'

print(r.text)