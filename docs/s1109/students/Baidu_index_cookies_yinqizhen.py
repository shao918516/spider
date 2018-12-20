#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from requests.cookies import RequestsCookieJar
from common.requests_helper import make_session

__author__ = 'YuChen'


# 2、使用 requests 加载 第一步 获取的cookies，
#     访问 百度指数
#     index.baidu.com
#     搜索 黄金
# 注意事项：
# 在最后点击 登录按钮 之前，设置 断点， 如果登录需要验证码，
# 手动在浏览器中输入验证码

class BaiDuIndexSpider:

    def __init__(self):
        self.session = make_session(True)

    def load_cookies(self, file_path):
        with open(file_path) as f:
            cookies = json.load(f)
        cookie_jar = RequestsCookieJar()
        for cookie in cookies:
            cookie_jar.set(cookie['name'], cookie['value'])
        self.session.cookies = cookie_jar

    def visit_baidu_index(self):
        url = 'http://index.baidu.com/v2/main/index.html#/trend/%E9%BB%84%E9%87%91?'
        headers = {
            'Referer': 'http://index.baidu.com/?from=pinzhuan#/?'
        }
        # 'http://index.baidu.com/v2/main/index.html#/trend/%E9%BB%84%E9%87%91?'
        params = {
            'prod': 'prod',
            'wd': '黄金',
            '17301': '',
            'callback': '_jsonpzvhvkao3wm'
        }
        response = self.session.get(url, params=params, headers=headers)
        response.encoding = 'utf-8'
        resp_text = response.text

        # json_data = response.json()
        # statuses = json_data['data']['result']#

        return resp_text


if __name__ == '__main__':
    baidu_index = BaiDuIndexSpider()
    baidu_index.load_cookies('baidu_cookies.txt')
    baidu_index.visit_baidu_index()
    print(baidu_index.visit_baidu_index())
