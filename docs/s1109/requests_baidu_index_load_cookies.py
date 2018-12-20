#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from urllib.parse import unquote, quote

from requests.cookies import RequestsCookieJar

from common.requests_helper import make_session

__author__ = 'Terry'

"""
    需求：
    使用 requests 加载 登录过百度的cookies，
    访问 百度指数
    index.baidu.com
    搜索 黄金
    
    实现：
    1、抓包
    2、构建基本类
    3、首先访问百度指数的首页， http://index.baidu.com/
    4、分析包
        1、我们搜索的内容是 黄金
            直接搜索 黄金，是搜索不到内容的，
            通过分析 浏览器的 url， 可以看到 %E9%BB%84%E9%87%91 这样的字符串
            可以猜测 可能是 黄金 的url编码， 使用 unquote('%E9%BB%84%E9%87%91') 确认
            在 request body 中搜索 
                %E9%BB%84%E9%87%91,  没有参数
                
            可以确定请求不是通过 post 发送的
            大概率是 get 请求
            可以使用 浏览器 地址栏中的：
            http://index.baidu.com/v2/main/index.html#/trend/%E9%BB%84%E9%87%91?words=%E9%BB%84%E9%87%91
            
            url 中的 #  是 锚 的作用
            
            这个请求是一个 302 跳转过来的，
            那么我们需要访问的url是：
            http://index.baidu.com/api/Route?fromu=http%3A%2F%2Findex.baidu.com%2Fv2%2Fmain%2Findex.html%23%2Ftrend%2F%E9%BB%84%E9%87%91%3Fwords%3D%25E9%25BB%2584%25E9%2587%2591
            
            
            
"""

class BaiduIndexSpider:

    def __init__(self):
        self.session = make_session(True)

    def load_cookies(self, file_path):
        """ 从指定文件中加载cookie内容

        :param file_path:   文件
        :return:
        """

        # 从文件 反序列化 一个对象
        with open(file_path) as f:
            cookies = json.load(f)

        # RequestsCookieJar 是 requests 的 cookies 的对象
        cookies_jar = RequestsCookieJar()
        # 遍历 cookies 列表
        for cookie in cookies:
            """
                为什么只需要使用 name 和 value
                
                如果只使用 name和value ，监听后，查看效果
                提交的请求中，包含如下 cookie：
                BAIDUID	B600CEDE6C63A3C1B98BB8ECAB18F551:FG=1
                BDUSS	zAtS1ZlS2NuMmM5MUVYaEg0dFl3bjY3RVg4YlBucTV1VlZid1dXN21-amRmZ3hjQVFBQUFBJCQAAAAAAAAAAAEAAAB4TynObXVtdWxvdmVzaGluZQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAN3x5Fvd8eRba
                BD_HOME	1
                BD_LAST_QID	9531883699549834121
                BD_UPN	13314752
                BIDUPSID	B600CEDE6C63A3C1B98BB8ECAB18F551
                H_PS_PSSID	27499_1439_21109_18560_20880_27401_22159
                PSTM	1541730744
                delPer	0
                
                可以查看文件，可以得知文件中，有 9 个cookie
                
                也就是我们只设置 name 和value， 那么在 请求 应用了所有的cookie
                
                但是 cookie 是区分 domain 和 path
                 从cookie的应用上讲， 
                 如果我们要访问的是  index.baidu.com
                 那么我们只应该 设置 所属的 domain为 
                 index.baidu.com和.baidu.com  的cookie，其他的cookie 不应该设置
                 
                 这里存在几个问题：
                 1、你需要增加额外的判断， domain的判断， 别忘记还有一个 path
                 类似：
                 if cookie['domain']=='.baidu.com':
                    cookies_jar.set(cookie['name'], cookie['value'])
                 elif cookie['domain'] == 'index.baidu.com' and (cookie['path']=='/' or cookie['path']=='/api/Route'):
                 
                 增加了很多额外的工作，并且随时可能出错
                 
                 2、你后续访问的url， 是有可能不是同一个 域 的
                    譬如： 
                    你第一个 url 请求是  index.baidu.com ， 
                        这里设置了所有的属于 顶级域名和 index.baidu.com 的cookie
                    第二个 url 请求是 baike.baidu.com
                        那么执行这一步操作，你又的重新加载cookie，把属于 baike.baidu.com 的 cookie 进行设置
                    第三个？第四个？
                    
                 所以，终极解决方案：
                 我不管我们取到的cookie 是属于 什么domain和 path 的，
                 全部设置了 顶级域名和 根path
                 这样的弊端： 
                 你提交一些url时，会提交一些多余的 cookie 值, 多用一点网络资源，
                 但是不会对业务功能造成任何影响
            """
            cookies_jar.set(cookie['name'], cookie['value'])

        self.session.cookies = cookies_jar

    def visit_index(self):
        url = 'http://index.baidu.com/'
        self.session.get(url)

    def visit_api_route(self, keyword):
        url = 'http://index.baidu.com/api/Route'
        headers = {
            'Referer': 'http://index.baidu.com/'
        }
        # charles 中查看到的 参数，就是以下构造方式
        fromu = f'http://index.baidu.com/v2/main/index.html#/trend/{keyword}?words={quote(keyword)}'
        params = {
            'fromu': fromu
        }
        self.session.get(url, headers=headers, params=params)

if __name__ == '__main__':
    baidu_index_spider = BaiduIndexSpider()
    baidu_index_spider.load_cookies('baidu_cookies.txt')
    baidu_index_spider.visit_index()
    keyword = '黄金'
    baidu_index_spider.visit_api_route(keyword)

