#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

from common.requests_helper import make_session
import urllib3
urllib3.disable_warnings()

__author__ = 'Terry'

"""
    需求：
    实现github的登录
    
    登录url是：https://github.com/login
    
    实现：
    1、抓包
    2、写前期的准备代码
    3、分析包
    4、第一个访问的url， 永远都是get
        不管有用没用，直接访问
    5、通过快速搜索，可以定位到 url： https://github.com/session
        headers：
            只有一个referer
            
        params：没有
        
        data or json： 是form表单，即 data参数
            下列参数需要判断是固定值，还是动态获取的
            多抓几次包，进行比对，如果多次都一样，认为是固定值，每次不一样，肯定是动态值
            'commit': 'Sign in',   # 固定值
            'utf8': '✓',   # 固定值
            'authenticity_token': '4DVhovW0HbZsBmmpysHU2CI6vr9PVIIJQ/Zm4JtBrc7rX/tULAD0ckjmBUKW7GbeWyYnSqh6Lei3otKsUrBs4A==',   # 动态值
            'login': 'mumuloveshine',   # 用户名
            'password': 'mumu2018'   # 密码
            
            PS： key中有 token、id 等的，一般是动态之
                value 中是一些 16进制字符串 或者一些 其他的 比较长的字符串， 一般都是动态获取的
                
            可以猜测 authenticity_token  的 value 是动态，
            那么需要查找这个值在哪获取
            在 response 的范围内 搜索这个 值
            类似这种很长的字符串，我们不要全搜， 因为其中可能有一些字符被转码，那么就会搜索失败
            截取其中一截， 10到20个连续的  字母+数字 进行搜索
            经过搜索，得知 这个 
            authenticity_token  是在 https://github.com/login 返回的response 中得到的
            
"""

class GithubSpider:

    def __init__(self, username, password):
        self.session = make_session(True)

        self.username = username
        self.password = password

    def visit_login(self):
        """ 访问第一个url请求

        :return:
        """
        url = 'https://github.com/login'
        response = self.session.get(url)
        text = response.text
        # 后续的 session 请求所需要的 值
        self.authenticity_token = re.search(r'name="authenticity_token" value="(.*?)"', text).group(1)
        print('得到 authenticity_token:', self.authenticity_token)

    def visit_session(self):
        url = 'https://github.com/session'
        # headers ， 有一个 referer
        headers = {
            'Referer': 'https://github.com/login',
        }
        # params  , 这里没有 params
        # data 或 json
        data = {
            'commit': 'Sign in',
            'utf8': '✓',
            'authenticity_token': self.authenticity_token,
            'login': self.username,
            'password': self.password
        }
        response = self.session.post(url, headers=headers, data=data)
        text = response.text

        if 'Start a project' in text:
            print('登录成功')
        else:
            print('登录失败')

if __name__ == '__main__':
    username = 'mumuloveshine'
    password = 'mumu2018'
    github_spider = GithubSpider(username, password)
    github_spider.visit_login()
    github_spider.visit_session()
