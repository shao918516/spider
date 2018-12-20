#!/usr/bin/env python
# -*- coding utf-8 -*1
import re

from common.requests_helper import make_session
import urllib3
urllib3.disable_warnings()
class SinaSpider:
    def __init__(self, username, password):
        self.session = make_session(True)
        self.username = username
        self.password = password
    def visit_login(self):
        """ 访问第一个url请求

        :return:
        """
        url = 'https://passport.weibo.cn/sso/login'
        response = self.session.get(url)
        text = response.text

    def visit_session(self):
        url = 'https://m.weibo.cn/'
        # headers ， 有一个 referer
        headers = {
            'Referer': 'https://github.com/login',
        }

        data = {
            'username': self.username,
            'password': self.password,
            'savestate': "1",
            'ec': "0",
            'entry': "mweibo",
        }
        response = self.session.post(url, headers=headers, data=data)
        text = response.text
        print(text)

        if '随时随地发现新鲜事！微博带你欣赏世界上每一个精彩瞬间，了解每一个幕后故事。分享你想表达的，让全世界都能听到你的心声！' in text:
            print('登录成功')
        else:
            print('登录失败')

if __name__ == '__main__':
    username = '13763334011'
    password = 'zhaoxiachen2018!'
    github_spider = SinaSpider(username, password)
    github_spider.visit_login()
    github_spider.visit_session()