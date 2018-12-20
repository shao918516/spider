#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import time

from common.s12306_helper import *
from common.manual_dm import Manual
from common.request_helper import make_session
from common.rk import RClient
from urllib import parse

from common.util import get_13_time

__author__ = 'Terry'

import urllib3
urllib3.disable_warnings()

"""
    需求：
    实现12306的购票
    
    实现：
    1、抓包
        登录链接是：https://kyfw.12306.cn/otn/login/init
    2、分析包
    3、核心请求：
        3种方式查找：
        1、查找post请求
        2、搜索 login 关键字
        3、搜索 登录的用户名
        
        https://kyfw.12306.cn/passport/web/login
    4、要想获得 json 格式的 response，必须将 headers中的 accept 修改为：
        application/json, text/javascript, */*; q=0.01
    5、需要提交验证码，url是：
        https://kyfw.12306.cn/passport/captcha/captcha-check
        form参数：
        answer	115,113,180,44   #  图片对应的坐标，2个图片的位置， 分别是 3和6
        login_site	E
        rand	sjrand
    5、实现 图片位置 字符串 转换成 坐标字符串 的方法
    6、获取图片的 url：https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand&0.13956760608019647
        注意：切记，所有这种登录的时候使用的验证码，一定要用相同的session去访问！！！
        
"""

import random
from settings import *

class Spider12306:


    def __init__(self, username, password):
        self.username = username
        self.password = password

        self.session = make_session(debug=True)
        self.dm_init()

        self.url_index = 'https://kyfw.12306.cn/otn/login/init'

    def dm_init(self):
        if USE_DM == 'ruokuai':
            self.dm = RClient(RUOKUAI_CONFIG['username'],
                              RUOKUAI_CONFIG['password'],
                              RUOKUAI_CONFIG['soft_id'],
                              RUOKUAI_CONFIG['soft_key'])
        else:
            self.dm = Manual()

    def visit_init(self):
        """
            访问登录首页
        :return:
        """
        self.session.get(self.url_index)
        print('访问首页结束')

    def _visit_captcha_image(self):
        url = 'https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand&' + str(random.random())
        r = self.session.get(url)

        # 返回图片的 bytes
        return r.content

    def _visit_captcha_check(self, postion_str):
        url = 'https://kyfw.12306.cn/passport/captcha/captcha-check'
        data = {
            'answer': postion_str,
            'login_site': 'E',
            'rand': 'sjrand'
        }
        headers = {
            'Refefer': self.url_index
        }
        r = self.session.post(url, data=data, headers=headers)
        json_data = r.json()

        result_code = json_data['result_code']

        b = False

        if result_code == '4':
            print('验证码效验成功')
            b = True
        else:
            print('验证码效验失败', json_data['result_message'])

        return b

    def validate_vcode(self):
        # 尝试 10 次 验证码提交
        for _ in range(10):
            json_data = self.dm.create(self._visit_captcha_image, 6113)
            result = json_data['Result']
            vcode_id = json_data['Id']

            position_str = get_loc_by_vcode(result)
            print(f'验证码串 {result} 转换为坐标串：{position_str}')
            b = self._visit_captcha_check(position_str)

            if not b:
                # 失败了， 继续尝试
                self.dm.report_error(vcode_id)
                time.sleep(.5)
            else:
                # 成功了，退出
                break
        else:
            print('尝试 5 次验证码，依旧失败！！')
            exit()

    def visit_login_submit(self):
        url = 'https://kyfw.12306.cn/passport/web/login'
        data = {
            'username': self.username,
            'password': self.password,
            'appid': 'otn'   # 不确定是否固定值的，可以多提交几次，如果每次都一样，那么就是固定值
        }
        headers = {
            'Refefer': self.url_index
        }
        r = self.session.post(url, data=data, headers=headers)
        json_data = r.json()

        result_code = json_data['result_code']
        if result_code == 0:
            print('登录成功')
        else:
            print('登录失败，', json_data['result_message'])

    def visit_userLogin(self):
        url = 'https://kyfw.12306.cn/otn/login/userLogin'
        data = {
            '_json_att': ''
        }
        self.session.post(url, data=data)

    # def visit_userLogin_no_redirect(self):
    #     url = 'https://kyfw.12306.cn/otn/login/userLogin'
    #     data = {
    #         '_json_att': ''
    #     }
    #     r = self.session.post(url, data=data, allow_redirects=False)
    #     location = r.headers['Location']
    #     X_via = r.headers['X-Via']
    #     self.session.get(location)

    def visit_auth_uamtk(self):
        url = 'https://kyfw.12306.cn/passport/web/auth/uamtk'
        data = {
            'appid': 'otn'
        }
        r = self.session.post(url, data=data)
        json_data = r.json()

        result_code = json_data['result_code']

        if result_code == 0:
            print('uamtk 成功')
            self.newapptk = json_data['newapptk']
        else:
            print('uamtk 失败')
            print(r.text)

    def visit_uamauthclient(self):
        url = 'https://kyfw.12306.cn/otn/uamauthclient'
        data = {
            'tk': self.newapptk
        }
        r = self.session.post(url, data=data)
        json_data = r.json()

        result_code = json_data['result_code']
        if result_code == 0 :
            print('uamauthclient 成功，用户名是：', json_data['username'])
        else:
            print('uamauthclient 失败')
            print(r.text)

    def visit_leftTicket_init(self):
        url = 'https://kyfw.12306.cn/otn/leftTicket/init'
        self.session.get(url)

    def visit_leftTicket_queryA(self, train_data, from_station, to_station, seat_type='硬卧'):
        self.train_data = train_data
        self.from_station = from_station
        self.to_station = to_station
        self.seat_type = seat_type

        url = 'https://kyfw.12306.cn/otn/leftTicket/query'
        params = {
            'leftTicketDTO.train_date': train_data,
            'leftTicketDTO.from_station': STATION_DICT[from_station],
            'leftTicketDTO.to_station': STATION_DICT[to_station],
            'purpose_codes': 'ADULT'
        }
        r = self.session.get(url, params=params)
        json_data = r.json()

        b = False

        status = json_data['status']

        if status:
            print('获取车次列表成功')
            """
                得到 查询的 所有车次信息，列表，列表中的元素类似：
                "NzlCBspFZDWRgcehQHnbbwT9JySLkRdBEeQAqKU3PG0EDQgpIpjNPXbSXufUr%2BetHqz9bba739Xn%0AUvp%2BueXri2w9nH0VpIl2J8sg29oaSJfk5rEmEQ8QQ2UQgX0GgtmX1Q611Ei2Lkx5nQ8FNhrtKxNF%0AEOiJmfuOwjpwbDhSh1xMmYrzZ2ASIaMkcDr07Pwj4SYzGL39VgvyeJajyCQP34NgLBuZRNcCY080%0AJJ4tisbidiAWtsTNqxCgRXe38fjzS4eDDRD7bhc%3D|预订|240000Z14908|Z149|BXP|GIW|BXP|CSQ|08:36|23:18|14:42|Y|74oDJih6BMAX2MALt%2F3JIf9IG3CNQmreImD0SZS%2FyX8MM%2BFyhYUVVdlx5e0%3D|20181016|3|P4|01|09|0|0||||2|||有||3|有|||||10401030|1413|0"
                使用 | 进行分隔：
                下标  作用
                0     submitOrderRequest 请求中的 secretStr 参数
                3     车次，譬如：z149
                4     始发站
                5     终点站
                6     出发地
                7     目的地
                8     发车时间
                9     到达时间
                10    历时多久
                13    出发日期
                23    软卧
                28    硬卧
                31    一等座
                32    商务座
            """
            self.train_li = json_data['data']['result']

            for train in self.train_li:
                train_split = train.split('|')
                # 5种情况：   ''、有、大于0的整数、无、0
                seat_status = train_split[SEAT_TYPE_INDEX_DICT[seat_type]]

                if seat_status != '' and seat_status != '无' and seat_status!= '0':
                    print(f'选中车次：{ train_split[3] }， 座席是：{seat_type}, 票数：{seat_status}')
                    self.current_train = train_split
                    b = True
                    break
            else:
                print('没有合适的车次！！')
        else:
            print('获取车次列表失败')
            print(r.text)

        return b

    def visit_leftTicket_submitOrderRequest(self):
        url = 'https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest'
        data = {
            'secretStr': parse.unquote(self.current_train[0]),
            'train_date': self.train_data,
            'back_train_date': self.train_data,
            'tour_flag': 'dc',  # 单程
            'purpose_codes': 'ADULT', # 普通乘客
            'query_from_station_name': self.from_station,
            'query_to_station_name': self.to_station,
            'undefined': ''
        }
        headers = {
            'Referer': 'https://kyfw.12306.cn/otn/leftTicket/init'
        }
        r = self.session.post(url, data=data, headers=headers)
        json_data = r.json()

        status = json_data['status']
        if status:
            print('submitOrderRequest 确认成功')
            return True
        else:
            print('submitOrderRequest 确认失败，')
            print(r.text)
            return False

    def visit_initDc(self):
        url = 'https://kyfw.12306.cn/otn/confirmPassenger/initDc'
        data = {
            '_json_att': ''
        }
        r = self.session.post(url, data=data)
        text = r.text

        self.globalRepeatSubmitToken = re.search(r"globalRepeatSubmitToken = '(.*?)';", text).group(1)
        self.key_check_isChange = re.search(r"'key_check_isChange':'(.*?)'", text).group(1)

    def visit_getPassengerDTOs(self):
        url = 'https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs'
        data = {
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': self.globalRepeatSubmitToken
        }
        r = self.session.post(url, data=data)
        json_data = r.json()

        self.normal_passengers = json_data['data']['normal_passengers']

    def _get_passengerTicketStr_oldPassengerStr(self, ticket_passenger_no_id):
        # 普通实现
        # passenger_info = None
        # for passenger in self.normal_passengers:
        #     if passenger['passenger_id_no'] == ticket_passenger:
        #         passenger_info = passenger
        #         break

        # filter实现
        passenger_info = list(filter(lambda x: x['passenger_id_no']==ticket_passenger_no_id, self.normal_passengers))[0]

        """
                {
                    "code": "1",
                    "passenger_name": "颜金娥",
                    "sex_code": "F",
                    "sex_name": "女",
                    "born_date": "1958-03-17 00:00:00",
                    "country_code": "CN",
                    "passenger_id_type_code": "1",
                    "passenger_id_type_name": "中国居民身份证",
                    "passenger_id_no": "432524195803170023",
                    "passenger_type": "1",
                    "passenger_flag": "0",
                    "passenger_type_name": "成人",
                    "mobile_no": "13263281381",
                    "phone_no": "",
                    "email": "",
                    "address": "",
                    "postalcode": "",
                    "first_letter": "YJE",
                    "recordCount": "2",
                    "total_times": "95",
                    "index_id": "0",
                    "gat_born_date": "",
                    "gat_valid_date_start": "",
                    "gat_valid_date_end": "",
                    "gat_version": ""
                }
        """
        #  '3,0,1,颜金娥,1,432524195803170023,13263281381,N'
        passengerTicketStr = f'{SEAT_TYPE_CHECK_INFO_DICT[self.seat_type]},{passenger_info["passenger_flag"]},' \
                             f'{passenger_info["passenger_type"]},{passenger_info["passenger_name"]},{passenger_info["passenger_id_type_code"]},' \
                             f'{passenger_info["passenger_id_no"]},{passenger_info["mobile_no"]},N'
        #  '颜金娥,1,432524195803170023,1_'
        oldPassengerStr = f'{passenger_info["passenger_name"]},{passenger_info["passenger_id_type_code"]},' \
                          f'{passenger_info["passenger_id_no"]},{passenger_info["passenger_type"]}_'

        return passengerTicketStr, oldPassengerStr

    def visit_checkOrderInfo(self, ticket_passenger_no_id):
        self.ticket_passenger_no_id = ticket_passenger_no_id

        url = 'https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo'
        passengerTicketStr, oldPassengerStr = self._get_passengerTicketStr_oldPassengerStr(ticket_passenger_no_id)
        data = {
            'cancel_flag': '2',
            'bed_level_order_num': '000000000000000000000000000000',
            'passengerTicketStr': passengerTicketStr,
            'oldPassengerStr': oldPassengerStr,
            'tour_flag': 'dc',
            'randCode': '',
            'whatsSelect': '1',
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': self.globalRepeatSubmitToken
        }

        r = self.session.post(url, data=data)
        json_data = r.json()

        submitStatus = json_data['data']['submitStatus']

        if submitStatus:
            print('checkOrderInfo  成功')
        else:
            print('checkOrderInfo 失败')
            print(r.text)

    def visit_getQueueCount(self):
        url = 'https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount'

        data = {
            'train_date': date_format_12306_getQueueCount(self.train_data),
            'train_no': self.current_train[2],
            'stationTrainCode': self.current_train[3],
            'seatType': '3',
            'fromStationTelecode': self.current_train[6],
            'toStationTelecode': self.current_train[7],
            'leftTicket': self.current_train[12],
            'purpose_codes': '00',
            'train_location': self.current_train[15],
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': self.globalRepeatSubmitToken
        }

        r = self.session.post(url, data=data)
        json_data = r.json()

        messages = json_data['messages']

        def validate_ticket(ticket, num=1):
            if int(ticket.split(',')[0]) >= num:
                return True
            else:
                print('没有对应的座席的票了')
                return False

        b = False
        if messages:
            print('getQueueCount 失败')
            print(r.text)
        else:
            print('getQueueCount 成功')
            ticket = json_data['data']['ticket']

            b = validate_ticket(ticket)

        return b

    def visit_confirmSingleForQueue(self):
        url = 'https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue'
        passengerTicketStr, oldPassengerStr = self._get_passengerTicketStr_oldPassengerStr(self.ticket_passenger_no_id)
        data = {
            'passengerTicketStr': passengerTicketStr,
            'oldPassengerStr': oldPassengerStr,
            'randCode': '',
            'purpose_codes': '00',
            'key_check_isChange': self.key_check_isChange,
            'leftTicketStr': self.current_train[12],
            'train_location': self.current_train[15],
            'choose_seats': '',
            'seatDetailType': '000',
            'whatsSelect': '1',
            'roomType': '00',
            'dwAll': 'N',
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': self.globalRepeatSubmitToken
        }
        r = self.session.post(url, data=data)
        json_data = r.json()

        submitStatus = json_data['data']['submitStatus']

        if submitStatus:
            print('confirmSingleForQueue 成功')
        else:
            print('confirmSingleForQueue 失败')
            print(r.text)

    def _visit_queryOrderWaitTime(self):
        url = 'https://kyfw.12306.cn/otn/confirmPassenger/queryOrderWaitTime'
        params = {
            'random': get_13_time(),
            'tourFlag': 'dc',
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': self.globalRepeatSubmitToken
        }
        r = self.session.get(url, params=params)
        json_data = r.json()

        orderId = json_data['data']['orderId']

        if orderId:
            print('queryOrderWaitTime 出票成功， id：', orderId)
            return True
        else:
            print('queryOrderWaitTime 还没有出票, 预计等待时间：', json_data['data']['waitTime'])
            return False

    def validate_queryOrderWaitTime(self):
        for _ in range(100):
            b = self._visit_queryOrderWaitTime()

            if b:
                break
            else:
                t = 3
                print(f'等待 {t} 秒，继续查询')
                time.sleep(t)
        else:
            print('queryOrderWaitTime 查询超时，退出！')

if __name__ == '__main__':
    username = 'mumuloveshine'
    password = 'mumu2018'
    spider12306 = Spider12306(username, password)
    spider12306.visit_init()
    spider12306.validate_vcode()
    spider12306.visit_login_submit()

    spider12306.visit_userLogin()

    spider12306.visit_auth_uamtk()
    spider12306.visit_uamauthclient()
    spider12306.visit_leftTicket_init()

    train_data = '2018-12-16'
    from_station = '北京'
    to_station = '长沙'
    seat_type = '硬卧'
    # 颜金娥的 身份证号码
    ticket_passenger = '432524195803170023'

    b = spider12306.visit_leftTicket_queryA(train_data, from_station, to_station, seat_type)
    if b:
        b = spider12306.visit_leftTicket_submitOrderRequest()
        if b:
            spider12306.visit_initDc()
            spider12306.visit_getPassengerDTOs()
            spider12306.visit_checkOrderInfo(ticket_passenger)
            b = spider12306.visit_getQueueCount()
            if b:
                spider12306.visit_confirmSingleForQueue()
                spider12306.validate_queryOrderWaitTime()


