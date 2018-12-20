#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Terry'


from selenium import webdriver
import time

# 启动驱动，不同的浏览器启用不同的类
# driver = webdriver.PhantomJS(phantomjs_driver_path)
fireFoxOptions = webdriver.FirefoxOptions()
fireFoxOptions.set_headless()
driver = webdriver.Firefox(firefox_options=fireFoxOptions)
# 设置窗口大小
driver.set_window_size(1366, 768)
# 页面的加载超时时间
driver.set_page_load_timeout(10)
# script脚本的超时时间
driver.set_script_timeout(10)

# 访问目标页面
driver.get('https://www.baidu.com')

# 下面有3种延时方式的展示，一般实际项目中不会同一个地方用3个延时，选择一个或多个使用

# 绝对延时，等待规定时间后，直接执行后面的代码
time.sleep(1)

# 隐性延时，最长是30秒，如果30秒内，资源全部加载完成，那么执行后续的代码，
# 30秒内没有加载完成，也会继续执行后续代码
driver.implicitly_wait(30)

# 显性等待，等待时长20秒，间隔0.5秒去查询一次，目标元素是否加载完成
# 20秒内加载完成后，执行后续的代码，最长等待20秒，没有加载也会继续执行
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# driver.get('https://huilansame.github.io')
# locator = (By.LINK_TEXT, 'CSDN')
# # 20 秒是最长等待时间，  0.5 秒是间隔轮询时间
# WebDriverWait(driver, 20, 0.5).until(EC.presence_of_element_located(locator))

# 通过xpath的方式查找
su = driver.find_element_by_xpath('//*[@id="su"]')

# print(su.get_attribute('type'))
# print(su.get_attribute('id'))
# print(su.get_attribute('value'))
# print(su.get_attribute('class'))

# # 通过标签的id查找
# su = driver.find_element_by_id('su')
# # 通过标签的css选择器查找
# su = driver.find_element_by_css_selector('#su')
# # 通过class进行查找
# driver.find_element_by_class_name('bg s_btn')

# 也是通过标签的xpath，等同于 driver.find_element_by_xpath('//*[@id="su"]')
# driver.find_element(By.XPATH, '//*[@id="su"]')

# print(driver.title)
# print(su.get_attribute('value'))

# 保存屏幕
driver.get_screenshot_as_file('screenshot.jpg')

# 需要手动退出driver
# 切记切记一定退出
driver.quit()

# sina移动端 ，火狐
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

#打开浏览器
driver = webdriver.Firefox()
# 设置10秒页面超时返回，类似于requests.get()的timeout选项，driver.get()没有timeout选项
# 以前遇到过driver.get(url)一直不返回，但也不报错的问题，这时程序会卡住，设置超时选项能解决这个问题。
driver.set_page_load_timeout(10)
# 设置10秒脚本超时时间
driver.set_script_timeout(10)
driver.set_window_size(1366, 768)

# 访问新浪移动端，没有验证码
driver.get('https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=http%3A%2F%2Fm.weibo.cn%2F')

WebDriverWait(driver, 30, 1).until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginName"]')))

print(driver.title)

time.sleep(1)

user = driver.find_element_by_xpath('//*[@id="loginName"]')
# 清除当前input元素中的值，需要清除
user.clear()
# 在input元素中输入内容
user.send_keys('51508690@qq.com')

pwd = driver.find_element_by_xpath('//*[@id="loginPassword"]')
pwd.clear()
pwd.send_keys('mumu2018')

login = driver.find_element_by_xpath('//*[@id="loginAction"]')
# 出发这个login元素的click事件
login.click()

WebDriverWait(driver, 30, 1).until(EC.presence_of_element_located((By.XPATH, '//p[@data-node="title"]')))

msg = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[1]/div[2]/a[2]')
msg.click()

# 需要手动退出driver
driver.quit()

print('over')