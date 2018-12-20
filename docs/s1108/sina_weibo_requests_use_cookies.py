#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from requests.cookies import RequestsCookieJar

from common.requests_helper import make_session

__author__ = 'Terry'

import urllib3

urllib3.disable_warnings()

class SinaWeiboMobileSpider:

    def __init__(self):
        self.session = make_session(True)

        self.index = 1

    def load_cookies(self, file_path):
        # 从文件中加载 cookies
        with open(file_path) as f:
            cookies = json.load(f)

        # session对象使用 RequestsCookieJar  操作 cookies
        cookie_jar = RequestsCookieJar()
        for cookie in cookies:
            # 往 RequestsCookieJar 对象中写入 cookie 值
            cookie_jar.set(cookie['name'], cookie['value'])

        # 设置当前类使用的 session 对象的 cookies
        self.session.cookies = cookie_jar

    def _visit_friends(self, max_id=None):
        """ 根据 max_id 获取指定页面的 博文数据

            2种不同的访问方式：
            1、访问第一页时，没有 max_id
                url直接是: https://m.weibo.cn/feed/friends?
                get 请求
                headers 中 有一个 Referer
            2、访问 第二页到第N页 时， 需要根据 一个参数 max_id 来确定页码
                而这个 max_id 是上一页的 博文数据 中的 json内容中的 json_data['data']['next_cursor']

                url 是：https://m.weibo.cn/feed/friends?max_id=4304099472257457

            即你访问第一页数据时，可以根据返回的 next_cursor
            拼接处 访问第二页的 url: https://m.weibo.cn/feed/friends?max_id=上一页获取的next_cursor
            访问第二页时，可以根据返回的next_cursor得到第三页的 url
            以此类推
            除了第一页，后续的数据都是根据上一页的 next_cursor 来进行访问的

        :param max_id:  url参数
        :return:
        """
        # 有 max_id 代表不是第一页博文
        if max_id:
            # 进行url的拼接
            url = 'https://m.weibo.cn/feed/friends?max_id=' + str(max_id)
        # max_id 为 None时， 访问获取第一页的博文数据
        else:
            url = 'https://m.weibo.cn/feed/friends?'

        headers = {
            'Referer': 'https://m.weibo.cn/'
        }
        response = self.session.get(url, headers=headers)

        json_data = response.json()

        # 得到 博文数据 列表
        statuses = json_data['data']['statuses']
        # 得到 获取 下一页博文数据 的  max_id
        next_cursor = json_data['data']['next_cursor']

        # 遍历 博文数据 列表
        for statuse in statuses:
            print(f"第{self.index}条 博主：{statuse['user']['screen_name']}, 博文：{statuse['text'][:10]}")
            self.index += 1

        return next_cursor

    def visit_friends_by_page_num(self, page_num=1):
        """ 获取指定页码数的博文信息

        :param page_num:  多少页
        :return:
        """
        next_cursor = None

        # 根据次数循环控制
        # 当循环的 数值没有作用时， 使用  _ 来代表
        for _ in range(page_num):
            next_cursor = self._visit_friends(next_cursor)


if __name__ == '__main__':
    sina_weibo_mobil_spider = SinaWeiboMobileSpider()
    sina_weibo_mobil_spider.load_cookies('sina_cookies.txt')
    sina_weibo_mobil_spider.visit_friends_by_page_num(5)
