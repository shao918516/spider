#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

def make_session(is_proxy=False):
    """构造一个通用的requests的session对象
    :return:  requests的session对象
    """
    session = requests.session()

    # 不检验 https 证书
    session.verify = False
    # 设置不信任系统代理，并且不启用
    session.trust_env = False
    # 设置默认的headers
    session.headers = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }
    if is_proxy:
        session.proxies = {
            'http': '127.0.0.1:8888',
            'https': '127.0.0.1:8888',
        }

    return session

# 这种命名也是不应该出现的， spider 是 爬虫
# 正确的应该 SinaSpider  WeiboSpider  MoblieWeiboSpider
class Spider():


    def __init__(self,username,password):
        self.session = make_session(True)
        self.username = username
        self.password = password

    def visit_sina(self):
        # 这个 url 哪来的啊 ？？
        self.session.get('https://passport.weibo.cn/')
        # print 作为日志信息，尽量明确一点
        # print('1')
        print('visit_sina')

    def login(self):
        data = {
            'username':self.username,
            'password':self.password,
            'savestate':1,
            'entry':'mweibo',
            'mainpageflag':1,
            'ec':0
        }
        headers = {
            'Referer':'https://passport.weibo.cn/signin/login'
        }
        url = 'https://passport.weibo.cn/sso/login'
        response = self.session.post(url, data=data, headers=headers)
        print(response.text)


if __name__ == "__main__":
    username = '13106543660'
    password = 'cong452452'
    sina_login = Spider(username,password)
    sina_login.visit_sina()
    sina_login.login()




