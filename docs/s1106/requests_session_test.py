#!/usr/bin/env python
# -*- coding: utf-8 -*-
from common.requests_helper import make_session

__author__ = 'Terry'


session = make_session()
response = session.get('http://www.baidu.com')

print(response.text)