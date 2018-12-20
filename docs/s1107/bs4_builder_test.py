#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Terry'


from bs4 import BeautifulSoup

# text = '<a><b /></a>'
# soup_test1 = BeautifulSoup(text, 'xml') # 会补全 html，body和p
# soup_test2 = BeautifulSoup(text, 'lxml') # 会补全 html，body和p
# soup_test3 = BeautifulSoup(text, 'html5') # 会补全 html，body和p
# soup_test4 = BeautifulSoup(text, 'strict') # 会补全 html，body和p

# print(soup_test1.builder)
# print(soup_test2.builder)
# print(soup_test3.builder)
# print(soup_test4.builder)

# soup_test5 = BeautifulSoup(text, ['html', 'html5lib'])
# print(soup_test5.builder)
# print('over')


from bs4 import BeautifulSoup
text = '<a><b />测试内容<c>test</c></a>'
soup_test = BeautifulSoup(text, 'lxml') # 会补全 html，body和p
print('lxml:')
print(soup_test)
soup_test = BeautifulSoup(text, 'html.parser') # 会补全 p
print('html.parser:')
print(soup_test)
soup_test = BeautifulSoup(text, 'html5')  # 会补全 html，head，body和p
print('html5:')
print(soup_test)
soup_test = BeautifulSoup(text, 'xml')  # 会加xml头，忽略错误的标签
print('xml:')
print(soup_test)