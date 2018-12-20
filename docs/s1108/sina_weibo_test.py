#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from common.requests_helper import make_session

__author__ = 'Terry'

import urllib3
urllib3.disable_warnings()

"""
    需求：
    登录sina微博手机版
    登录url：https://passport.weibo.cn/signin/login
    
    1、登录
    2、获取50个博文信息
        输出：
        博主名
        博文的前10个字符
        
        
    实现：
    1、抓包
    2、第一个入口的请求： https://passport.weibo.cn/signin/login
        直接访问
    3、查找第二个需要访问的 request
        我们的这里的功能是先登录、再获取博文
        第一个功能是 登录
        登录会使用到  用户名和密码
        但是密码一般会被转码，搜索 密码 不保险
        那么我们搜索 用户名， 如果用户名是邮箱，记住不要搜索@，
        那么在我这里就搜索 51508690@qq.com 用户名中的  51508690 字符串
        搜索的范围是： 
            这种登录提交，肯定是 post， 而且 用户名、密码，只会出现在 request 的请求体中
            
        搜索后，找到url： https://passport.weibo.cn/sso/login
        headers:
            Referer	https://passport.weibo.cn/signin/login
            
        params:  没有
        
        data or json:
            form表单数据：
            username	51508690@qq.com   # 用户名
            password	mumu2018   # 密码
            savestate	1
            r	
            ec	0
            pagerefer	
            entry	mweibo
            wentry	
            loginfrom	
            client_id	
            code	
            qq	
            mainpageflag	1
            hff	
            hfp	
        
        执行post 请求， 登录成功
        
    4、查找 获取博文 的请求
        不要搜索 中文、特殊字符
        而是去寻找 不易重复的 字母+数字+_ 组成的 字符串
        找到  Antares  这样一个字符串
        在 response 范围内查找
        找到： https://m.weibo.cn/feed/friends?
        PS: 如果找到多个， 记住， 请求时间最靠前的是正确的
        
        因为是GET请求，没有 data
        headers：
            Referer	https://m.weibo.cn/
        params：
            没有
            
        发送 get 请求， 得到第一页20条的博文信息的 json 内容
        
    5、要查找另外的 30 条 或者 更多 博文
        在 后续的（前20条博文以后的）博文中， 查找 可以用于 搜索的关键字
        iphone7
        在 response 范围内，搜索 iphone7
        查找到url： https://m.weibo.cn/feed/friends?max_id=4304071526186165
        
        比第一页的请求多了一个 max_id=4304071526186165
        4304071526186165：  这个 value 不可能是固定值， 确定是 动态值
            在 response 范围中 搜索 4304071526186165
            找到多个response包含， 确定一个请求：
            https://m.weibo.cn/feed/friends?max_id=4304079469074017
            
            同样的方式 搜索 4304079469074017
            找到： https://m.weibo.cn/feed/friends?
            
            获取第一页的时候， 得到一个 next_cursor， 指向下一页的 max_id
        
        
        
        
"""

class SinaWeiboMobileSpider:

    def __init__(self, username, password):
        self.session = make_session(True)

        self.username = username
        self.password = password

        self.index = 1

    def visit_signin_login(self):
        """ 访问登录的第一个请求

        :return:
        """
        url = 'https://passport.weibo.cn/signin/login'
        self.session.get(url)

        print('访问登录页面')

    def visit_sso_login(self):
        """ 发送登录请求

        :return:
        """
        url = 'https://passport.weibo.cn/sso/login'
        headers = {
            'Referer': 'https://passport.weibo.cn/signin/login'
        }
        data = {
            'username': self.username,
            'password': self.password,
            'savestate': '1',
            'r': '',
            'ec': '0',
            'pagerefer': '',
            'entry': 'mweibo',
            'wentry': '',
            'loginfrom': '',
            'client_id': '',
            'code': '',
            'qq': '',
            'mainpageflag': '1',
            'hff': '',
            'hfp': ''
        }

        response = self.session.post(url, data=data, headers=headers)

        # 使用 json库 转换 响应文本内容为 json格式
        # text = response.text
        # json_data = json.loads(text)

        # 使用 requests 的 response 的 json() 方法
        json_data = response.json()

        # 登录成功返回状态码是： 20000000
        if json_data['retcode'] == 20000000:
            print('登录成功')
        else:
            print('登录失败')

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
    username = '51508690@qq.com'
    password = 'mumu2018'
    sina_weibo_mobil_spider = SinaWeiboMobileSpider(username, password)

    sina_weibo_mobil_spider.visit_signin_login()
    sina_weibo_mobil_spider.visit_sso_login()

    sina_weibo_mobil_spider.visit_friends_by_page_num(10)
