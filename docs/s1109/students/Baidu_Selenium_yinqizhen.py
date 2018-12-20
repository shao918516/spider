#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json,time
from selenium import webdriver
from selenium.webdriver.common.by import By

# 1、使用 selenium 登录百度，保存 cookies到文件


def wait_ele(by, value):
    from selenium.webdriver.support.wait import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    WebDriverWait(driver, 50, 0.5).until(EC.presence_of_element_located((by, value)))
    time.sleep(0.5)

driver = webdriver.Firefox()
driver.set_page_load_timeout(5)
driver.set_script_timeout(5)
#要访问的url:
url = 'https://www.baidu.com'
driver.get(url)
time.sleep(0.5)
wait_ele(By.XPATH, '//*[@id="u1"]/a[7]')
login_action_tj_login = driver.find_element_by_xpath('//*[@id="u1"]/a[7]')
login_action_tj_login.click()
time.sleep(0.5)
wait_ele(By.ID, 'TANGRAM__PSP_10__footerULoginBtn')
login_action_ULoginBtn = driver.find_element_by_id('TANGRAM__PSP_10__footerULoginBtn')
login_action_ULoginBtn.click()
time.sleep(0.5)
wait_ele(By.ID,'TANGRAM__PSP_10__userName')
#输入用户名：
login_name_input = driver.find_element_by_id('TANGRAM__PSP_10__userName')
login_name_input.clear()
login_name_input.send_keys('mumuloveshine')
#输入密码：
login_password_input = driver.find_element_by_id('TANGRAM__PSP_10__password')
login_password_input.clear()
login_password_input.send_keys('mumu2018')
# 点击登录按钮
login_action_submit_button = driver.find_element_by_id('TANGRAM__PSP_10__submit')
login_action_submit_button.click()
#获取cookies
cookies = driver.get_cookies()
print(cookies)
with open('baidu_cookies.txt', 'w') as f:
    json.dump(cookies, f)
# 最后，一定记得 quit
driver.quit()







