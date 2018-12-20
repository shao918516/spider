#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from urllib.parse import quote

from common.requests_helper import make_session
from docs.s1112.db.mysql_handle import MysqlHandler

__author__ = 'Terry'


"""
    需求：
    1、登录拉勾网
        登录url：https://passport.lagou.com/login/login.html
    2、搜索 python爬虫
    3、获取3页的岗位数据：
        岗位名
        薪水
        公司名
        地点
    4、将数据保存到 mysql
    
    实现：
    1、多个功能很多时候是可以分开抓包的
        譬如这里的 登录功能 和 搜索功能 就是可以分开抓包
    2、抓 登录 数据包
    3、由于现在的拉勾网登录，需要极验验证码配合， 目前没有处理这个验证码的方式
        这里就仅仅分析 拉勾网 的登录部分
    4、实现前期准备代码
    5、访问 登录首页    
    6、查找 登录提交
        类似这种登录的提交，最直接的就是 搜索用户名
        在 request body 范围内，搜索 13007421682
        找到 ： https://passport.lagou.com/login/login.json
        
        headers 部分：
        X-Anit-Forge-Code	88841914
        X-Requested-With	XMLHttpRequest
        X-Anit-Forge-Token   	fb0253e2-ff3e-4cad-af5b-ba19fd038104
        Referer	https://passport.lagou.com/login/login.html
        
        在 response范围 搜索 ba19fd038104
        在  https://passport.lagou.com/login/login.html  response中找到： 
        window.X_Anti_Forge_Token = 'fb0253e2-ff3e-4cad-af5b-ba19fd038104';
        window.X_Anti_Forge_Code = '88841914';
        
        form表单部分：
        isValidate	true     # 固定值
        username	13007421682   # 账号
        password	f65c4696fa08c439bdbf458dfad3e4e6
        request_form_verifyCode	
        submit	
        challenge	d0797d18cb55cc023eae4fb45d56e53c
        
        需要查找 password 和 challenge
        
        先搜索： challenge	d0797d18cb55cc023eae4fb45d56e53c
        在 response 中 搜索 d0797d18cb55cc023eae4fb45d56e53c
        找到： https://api.geetest.com/gt_judgement?pt=0&gt=66442f2f720bfc86799932d8ad2eb6c7
        这个请求是 极验验证码 的效验， 暂时不管！
        
        继续搜索：password	 f65c4696fa08c439bdbf458dfad3e4e6
        类似密码的加密数据的搜索：
        1、搜索 f65c4696fa08c439bdbf458dfad3e4e6 是永远搜不到的
        2、一般搜索 前面的 key： password
        3、一般在 js 加密文件中， 会有类似这样的赋值：  password='某个值'
        4、在 response范围 中搜索 password， 因为 加密算法 都是在js文件中实现的，
            而js文件都是服务器返回的
            会搜索到非常多的结果，不容易分析
        5、应该搜索  "password="  这个字符串， 
            而有部分网站， =号前面是有 空格 的 "password ="  
        6、搜索 password= 这个字符串
            得到2个结果，简单分析后，判断查看
            https://www.lgstatic.com/passport/static/pkg/pc/page/login/main.html_aio_384c4e0.js
        7、由于 js 文件都是经过压缩的，不好查看
            需要进行格式化后查看，
             可以选择 文本工具，
             也可以选择浏览器中查看：在chrome浏览器中 sources 》》 network  可以找到该文件
             
             格式化后， 需要 搜索: password =    ，因为格式化会自动加 空格
             
             代码块如下：
             var c, g = y.collectData(), v = "veenike";
             g.password = md5(g.password),
             g.password = md5(v + g.password + v),
             
             通过python代码实现同样的加密：
             def lagou_encrypt_password(password):
                import hashlib
            
                # 第一次 md5 加密
                password = hashlib.md5(password.encode()).hexdigest()
            
                # 加 盐
                v = "veenike"
                password = v + password + v
            
                # 第二次 md5 加密
                password = hashlib.md5(password.encode()).hexdigest()
                return password
                
    7、抓 搜索岗位的 数据库
    8、直接访问 首页：https://www.lagou.com/
    9、搜索：
        1、在 request范围 搜索 python， 结果太多，没法分析
        2、在 response范围 搜索 页面上查看到的数据中不易重复的 数字+字母 字符串
            找到：
            https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false
        3、新建一个 charles 的session
            随便重构一个不易重复的 字符串，在 request范围 进行搜索， 找到 url 
            在这里也不好使，结果太多 
    
        https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false
        
        headers:
        Referer	https://www.lagou.com/jobs/list_python%E7%88%AC%E8%99%AB?labelWords=&fromSearch=true&suginput=
        
        form表单：
        first	true    # 第一页是 true
        pn	1  # 页码
        kd	python爬虫  # 搜索的 关键字 
        
    9、数据持久化
"""

def lagou_encrypt_password(password):
    """ 实现 拉勾网 的密码加密

    :param password:  加密后的密码
    :return:
    """
    import hashlib

    # 第一次 md5 加密
    password = hashlib.md5(password.encode()).hexdigest()

    # 加 盐
    v = "veenike"
    password = v + password + v

    # 第二次 md5 加密
    password = hashlib.md5(password.encode()).hexdigest()
    return password

class LagouSpider:

    def __init__(self, username, password, mysql_config):
        self.session = make_session(True)

        self.username = username
        self.password = password
        self.mysql_config = mysql_config

    def visit_login_html(self):
        url = 'https://passport.lagou.com/login/login.html'
        response = self.session.get(url)
        text = response.text

        self.X_Anti_Forge_Token = re.search(r"window.X_Anti_Forge_Token = '(.*?)';", text).group(1)
        self.X_Anti_Forge_Code = re.search(r"window.X_Anti_Forge_Code = '(.*?)';", text).group(1)

        print('获取到 token:', self.X_Anti_Forge_Token, self.X_Anti_Forge_Code)

    def visit_login_json(self):
        """
            目前有 极验验证码 暂时不处理
        :return:
        """
        url = 'https://passport.lagou.com/login/login.json'
        headers = {
            'X-Anit-Forge-Code': self.X_Anti_Forge_Code,
            'X-Requested-With': 'XMLHttpRequest',
            'X-Anit-Forge-Token': self.X_Anti_Forge_Token,
            'Referer': 'https://passport.lagou.com/login/login.html'
        }
        data = {
            'isValidate': 'false',
            'username': self.username,
            'password': lagou_encrypt_password(self.password),
            'request_form_verifyCode': '',
            'submit': '',
            # 'challenge': 'd0797d18cb55cc023eae4fb45d56e53c'
        }
        response = self.session.post(url, headers=headers, data=data)

        json_data = response.json()

        submitCode = json_data['submitCode']

        if submitCode == 75692247:
            print('登录成功')
        else:
            print('登录失败：', json_data['message'])

    def visit_index(self):
        url = 'https://www.lagou.com/'
        self.session.get(url)

    def visit_positionAjax(self, keyword, pn=1):
        """ 爬取指定 关键字 和 指定 页码的 岗位数据

        :param keyword:  搜索 关键字
        :param pn:  页码
        :return:  岗位信息的json列表
        """

        # 这里就一个 params 参数，并且是固定值，直接附加在 url 后面提交就行
        url = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'
        headers = {
            'Referer': f'https://www.lagou.com/jobs/list_{quote(keyword)}?labelWords=&fromSearch=true&suginput='
        }
        data = {
            'first': 'true',
            'pn': pn,
            'kd': keyword
        }
        response = self.session.post(url, headers=headers, data=data)

        json_data = response.json()

        if json_data['success']:
            print('获取岗位信息成功')
            result = json_data['content']['positionResult']['result']

            return result
        else:
            print('获取岗位信息失败')

    def visit_positionAjax_many(self, keyword, page_count):
        """ 访问多页岗位数据

        :param keyword:  搜索 岗位关键字
        :param page_count:  总的页数
        :return:
        """
        mysql_handle = MysqlHandler(self.mysql_config)
        sql = 'insert into lagou(position_name, salary, company_name, work_loc) values(%s,%s,%s,%s)'
        try:
            for i in range(1, page_count+1):
                result = self.visit_positionAjax(keyword, i)
                sql_params = [[position['positionName'],
                               position['salary'],
                               position['companyFullName'],
                               position['city']] for position in result]
                mysql_handle.insertMany(sql, sql_params)
        finally:
            mysql_handle.dispose()



if __name__ == '__main__':
    username = '13007421682'
    password = 'mumu2018'
    mysql_config = {
        'host': '127.0.0.1',
        'port': 3306,
        'db': 's1808',
        'user': 'root',
        'password': '123456',
        'charset': 'utf8'  # 不能是  utf-8
    }
    lagou_spider = LagouSpider(username, password, mysql_config)

    # lagou_spider.visit_login_html()
    # lagou_spider.visit_login_json()

    keyword = 'python爬虫'
    lagou_spider.visit_positionAjax_many(keyword, 3)


