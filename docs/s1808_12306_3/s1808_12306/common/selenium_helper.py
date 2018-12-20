#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Terry'

import time

def wait_ele(driver, by, value):
    """ 用于 selenium 使用中，等待某个指定元素的出现

    :param driver:  selenium驱动
    :param by:     查找的方式
    :param value:   查找的值
    :return:
    """
    from selenium.webdriver.support.wait import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    # 20  最长等待时间        0.5   轮询时间
    # 最长等待20秒，诶=每0.5秒查询一次， 对象出现了，继续执行，没出现 ，继续等待
    WebDriverWait(driver, 20, 0.5).until(EC.presence_of_element_located((by, value)))
    time.sleep(1)

def input_clear_and_send_keys(driver, by_type, by_value, keys):
    """ 往一个特定的input元素写入内容，写入之前先清空

    :param driver:  selenium驱动
    :param by_type:   by的类型
    :param by_value:   by的值
    :param keys:      写入的内容
    :return:
    """
    ele = driver.find_element(by_type, by_value)
    ele.clear()
    ele.send_keys(keys)
