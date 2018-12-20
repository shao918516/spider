#!/usr/bin/env python
# -*- coding utf-8 -*1
from lxml import etree
from common.requests_helper import make_session
import re
import urllib3
urllib3.disable_warnings()

url = 'https://www.23us.so/xiaoshuo/14789.html'
session = make_session()
response = session.get(url)
response.encoding = 'UTF-8'
text = response.text

print(text)
novel_title = re.search(r'name="keywords" content="(.*?)"', text).group(1)
novel_category = re.search(r'href="/list/1_1.html">(.*?)</a></td>', text).group(1)
novel_author = re.search(r'<td>&nbsp;([^<].*?)</td>', text).group(1)
novel_status = re.search(r'<td>&nbsp;(.*?)</td></tr><tr>', text).group(1)
novel_length = re.search(r'<td>&nbsp;(.*?)字', text).group(1)
novel_clicks = re.search(r'<td>&nbsp;([\d]{6})</td>', text).group(1)
print("小说名为", novel_title)
print("小说类别为", novel_category)
print("小说作者为", novel_author)
print("小说状态为", novel_status)
print("小说全文长度为{}字".format(novel_length))
print("全文点击数为", novel_clicks)
# parser = etree.HTMLParser(encoding = "utf-8")
# htmlelement = etree.parse("https://www.23us.so/xiaoshuo/14789.html", parser=parser)
# print(etree.tostring(htmlelement, encoding="utf-8").decode("utf-8"))