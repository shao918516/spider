#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import re

from common.requests_helper import make_session

import urllib3
urllib3.disable_warnings()

__author__ = 'Terry'

class TaobaoSpider:

    def __init__(self):
        # 初始化一个 session 对象
        self.session = make_session(True)
        # 每页显示的记录数
        self.page_num = 44
        # 总共多少页
        self.page_count = 100

        self.item_index = 1

    def visit_index(self):
        """ 访问首页

        :return:
        """
        url = 'http://www.taobao.com/'
        # 目前没有需要从response中获取数据，所以不赋值
        self.session.get(url)

    def _visit_search(self, q, s=0):
        """ 访问搜索页面

        :return:
        """
        url = 'https://s.taobao.com/search'
        params = {
            'q': q,  # 搜索关键字
            'ie': 'utf8',  # 编码
            's': s  #  起始记录数
        }
        headers = {
            'Referer': 'https://www.taobao.com/'
        }
        response = self.session.get(url, params=params, headers=headers)
        text = response.text

        g_page_config = re.search(r'g_page_config = (.*?}});', text).group(1)

        g_page_config = json.loads(g_page_config)

        auctions = g_page_config['mods']['itemlist']['data']['auctions']

        for auction in auctions:
            view_sales = auction.get('view_sales', '0人购买')
            print(f"商品：{self.item_index} 店铺：{auction['nick']}  价格：{auction['view_price']}  购买人数：{view_sales}")
            self.item_index += 1

    def visit_search_all(self, q):
        """ 访问 100 页 的搜索结果

        :param q:
        :return:
        """
        for i in range(self.page_count):
            s = self.page_num * i
            self._visit_search(q, s)

if __name__ == '__main__':
    taobao_spider = TaobaoSpider()
    taobao_spider.visit_index()
    keyword = '衬衣'
    taobao_spider.visit_search_all(keyword)