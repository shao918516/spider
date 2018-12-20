#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from selenium.webdriver.common.by import By

from common.selenium_helper import wait_ele, input_clear_and_send_keys

__author__ = 'Terry'


"""
    需求：
    使用 selenium 登录百度，保存 cookies 到文件
"""

from selenium import webdriver

def get_driver():
    driver = webdriver.Firefox()

    return driver

def baidu_login(driver, username, password):
    # 访问首页 ,  一定要加 http或者https
    driver.get('http://www.baidu.com')

    # 这里，html页面中有2个 tj_login 的 a标签， 第二个才是有效的！
    # tj_login_ele = driver.find_elements_by_name('tj_login')[1]
    tj_login_ele = driver.find_element_by_xpath('//*[@id="u1"]/a[@name="tj_login"]')
    tj_login_ele.click()

    # 等待 登录弹出框 的出现, 以下2种方式都可以
    # 显性等待+延时1秒
    # wait_ele(driver, By.ID, 'TANGRAM__PSP_10__footerULoginBtn')
    # 直接固定等待1秒
    time.sleep(1)

    # 直接获取元素并且调用 点击方法
    driver.find_element_by_id('TANGRAM__PSP_10__footerULoginBtn').click()

    # 等待 用户名和密码 输入框的出现
    time.sleep(1)

    # 输入用户名
    input_clear_and_send_keys(driver, By.ID, 'TANGRAM__PSP_10__userName', username)

    # 输入密码
    input_clear_and_send_keys(driver, By.ID, 'TANGRAM__PSP_10__password', password)

    #  点击登录
    driver.find_element_by_id('TANGRAM__PSP_10__submit').click()

def save_driver_cookies(driver, file_path):
    """ 将 selenium 驱动中的cookies保存到指定文件

    :param driver:  selenium驱动
    :param file_path:   文件
    :return:
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        import json
        json.dump(driver.get_cookies(), f)

if __name__ == '__main__':
    driver = get_driver()
    baidu_login(driver, 'mumuloveshine', 'mumu2018')
    time.sleep(1)
    save_driver_cookies(driver, 'baidu_cookies.txt')
    # 退出 浏览器
    driver.quit()
