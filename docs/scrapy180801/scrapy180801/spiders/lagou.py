#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from urllib.parse import quote

from scrapy180801.items import LagouItem

__author__ = 'Terry'

import scrapy

class LagouSpider(scrapy.Spider):
    """
        一定要继承 scrapy.Spider
    """

    # 必须设置 name 属性， 这个属性在整个项目的不同爬虫类中，必须唯一！！！
    name = 'lagou'

    # 本 爬虫类 的自定义配置
    # 和通用的 settings 中的配置 不一样的配置项，在这里单独设置
    # 所有能够在 setting 中配置的项，在这里都可以自定义配置！
    # 一般情况下，不会使用这个配置项
    # custom_settings = {
    #     'CONCURRENT_REQUESTS': 1
    # }


    """
        2中启动方式：
        1、 start_urls 属性 
        2、 start_requests 函数
    """

    # 第一种情况方式
    # 必须是 列表 ，里面值 是 第一个访问的url地址
    # 必须配置 parse 函数作为回调函数！！！
    start_urls = ['https://www.lagou.com/']

    # 第二种启动方式
    # def start_requests(self):
    #     url = 'https://www.lagou.com/'
    #     # dont_filter 不进行 重复检测， 默认会 去重
    #     # callback ：设置回调函数，一般第一个请求设置的回调函数是  parse
    #     yield scrapy.Request(url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        """ 处理第一个请求的 函数

        这个parse 函数不能用做其他用途！！！
        只能作为解析第一个请求的 回调处理 函数

        :param response:
        :return:
        """

        url = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'
        # 获取 settings 中的值
        keyword = self.settings['KEYWORD']

        headers = {
            'Referer': f'https://www.lagou.com/jobs/list_{quote(keyword)}?labelWords=&fromSearch=true&suginput='
        }
        # 获取爬取总页码数
        page_count = self.settings['PAGE_COUNT']
        for pn in range(1, page_count+1):
            data = {
                'first': 'true',
                'pn': str(pn),   # 必须转换为 str
                'kd': keyword
            }

            # 构造一个 post请求 request 对象
            # 这里不要使用 dont_filter 参数， 需要去重的功能
            yield scrapy.FormRequest(url, callback=self.parse_position, headers=headers, formdata=data)

    def parse_position(self, response):
        # scrapy中的 response 没有 resposne.json() 方法！！！！！！！！
        # 只能使用原始的 json 进行转换
        text = response.text
        json_data = json.loads(text)

        if json_data['success']:
            print('获取岗位信息成功')
            result = json_data['content']['positionResult']['result']

            # 对获取到的 15个 岗位列表 遍历
            for position in result:
                # 结构化数据
                item = LagouItem()
                item['position_name'] = position['positionName']
                item['salary'] = position['salary']
                item['company_name'] = position['companyFullName']
                item['city'] = position['city']

                # 将 item 对象 传递给 pipeline
                yield item
        else:
            print('获取岗位信息失败')