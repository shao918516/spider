#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

import time
from selenium.webdriver.common.by import By

__author__ = 'Terry'

from selenium import webdriver


def wait_ele(by, value):
    from selenium.webdriver.support.wait import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    # 20  最长等待时间        0.5   轮询时间
    # 最长等待20秒，诶=每0.5秒查询一次， 对象出现了，继续执行，没出现 ，继续等待
    WebDriverWait(driver, 20, 0.5).until(EC.presence_of_element_located((by, value)))
    time.sleep(1)

# 无界面打开浏览器
# fireFoxOptions = webdriver.FirefoxOptions()
# 设置为 无界面
# fireFoxOptions.set_headless()
# driver = webdriver.Firefox(firefox_options=fireFoxOptions)

# 有界面打开浏览器
driver = webdriver.Firefox()
# 设置页面读取超时时间
driver.set_page_load_timeout(10)
# 设置10秒脚本超时时间
driver.set_script_timeout(10)
driver.set_window_size(1366, 768)  # 重置窗口大小

# 访问一个网址
url = 'https://passport.weibo.cn/signin/login'
driver.get(url)

wait_ele(By.ID, 'loginName')

# 根据id查找 input 对象
login_name_input = driver.find_element_by_id('loginName')
# 所有的 可输入的 元素，在进行写入之前，一定要 clear 清空
login_name_input.clear()
# 往 input 标签中写 数据
login_name_input.send_keys('51508690@qq.com')

# 输入密码
login_password_input = driver.find_element_by_id('loginPassword')
login_password_input.clear()
login_password_input.send_keys('mumu2018')

# 点击登录按钮
login_action_button = driver.find_element_by_id('loginAction')
login_action_button.click()

time.sleep(2)

# 获取 cookie 列表
cookies = driver.get_cookies()
# 持久化 cookie
with open('sina_cookies.txt', 'w') as f:
    # 一定不能这样写入文件 str(cookies)
    # f.write(str(cookies))
    #  这样写是可以的，但是绕了一圈
    # f.write(json.dumps(cookies))

    # 使用json的 dump
    json.dump(cookies, f)

# 最后，一定记得 quit
driver.quit()