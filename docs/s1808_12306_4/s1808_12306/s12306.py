#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import re

import time
from urllib.parse import unquote

from common.manual import Manual
from common.requests_helper import make_session
from common.ruokuai import Ruokuai
from common.util import get_13_time
from s12306_helper import get_loc_by_vcode

__author__ = 'Terry'

import urllib3
urllib3.disable_warnings()

def format_date(date):
    struct_time = time.strptime(date, '%Y-%m-%d')
    return time.strftime('%a %b %d %Y', struct_time) + ' 00:00:00 GMT+0800 (中国标准时间)'

class S12306Spider:

    SEAT_TYPE_INDEX_DICT = {
        '高级软卧': 21,
        '软卧': 23,
        '无座': 26,
        '二等座': 30,
        '一等座': 31,
        '商务座': 32,
        '特等座': 32
    }

    def __init__(self, username, password):
        self.session = make_session(True)

        self.username = username
        self.password = password

        # 手动打码
        # self.dm = Manual()
        # 若快打码
        self.dm = Ruokuai(self.session, 'mumuloveshine', 'mumu2017', image_type='6113')

    def visit_resources_login(self):
        url = 'https://kyfw.12306.cn/otn/resources/login.html'
        self.session.get(url)

    def _visit_captcha_image(self):
        url = 'https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand&' + str(random.random())
        # 一定要用 self.session
        r = self.session.get(url)

        # 返回图片的 bytes
        return r.content

    def _visit_captcha_image64(self):
        url = 'https://kyfw.12306.cn/passport/captcha/captcha-image64'
        t = get_13_time()
        params = {
            'login_site': 'E',
            'module': 'login',
            'rand': 'sjrand',
            t: '',
            # 'callback': 'jQuery1910292836177545567_1542355491387',
            '_': str(int(t) - random.randint(1800, 2500)),
        }
        # 一定要用 self.session
        r = self.session.get(url, params=params)

        json_data = r.json()

        image = json_data['image']

        import base64
        content = base64.b64decode(image)
        # 返回图片的 bytes
        return content

    def _get_vcode(self):
        self.vcode, self.vcode_id = self.dm.create(self._visit_captcha_image64)
        return get_loc_by_vcode(self.vcode)

    def _visit_captcha_check(self):
        url = 'https://kyfw.12306.cn/passport/captcha/captcha-check'
        answer = self._get_vcode()
        params = {
            # 'callback': 'jQuery1910292836177545567_1542355491387',
            'answer': answer,
            'rand': 'sjrand',
            'login_site': 'E',
            '_': get_13_time(),
        }
        response = self.session.get(url, params=params)

        # 会抛出 json 错误
        json_data = response.json()

        if json_data['result_code'] == '4':
            print('验证码成功')
            self.vcode_answer = answer
            return True
        else:
            print('验证码失败:', self.vcode)
            return False

    def visit_captcha_check_until_success(self, max_time=10):
        """ 循环进行验证码验证，直到成功或者达到最大尝试次数

        :param max_time:  最大尝试次数
        :return:  成功或失败
        """
        for _ in range(max_time):
            b = self._visit_captcha_check()
            if not b:
                self.dm.report_error(self.vcode_id)
            else:
                return True
        else:
            print('10 次校验码都失败，异常！停止！')
            return False

    def visit_passport_web_login(self):
        url = 'https://kyfw.12306.cn/passport/web/login'
        data = {
            'username': self.username,
            'password': self.password,
            'appid': 'otn',
            'answer': self.vcode_answer
        }
        headers = {
            'Referer': 'https://kyfw.12306.cn/otn/resources/login.html'
        }

        response = self.session.post(url, headers=headers, data=data)

        json_data = response.json()

        if json_data['result_code'] == 0:
            print('登录成功')
        else:
            print('登录失败，', json_data['result_message'])

    def visit_uamtk(self):
        url = 'https://kyfw.12306.cn/passport/web/auth/uamtk'
        headers = {
            'Referer': 'https://kyfw.12306.cn/otn/passport?redirect=/otn/login/userLogin'
        }
        data ={
            'appid': 'otn'
        }
        response = self.session.post(url, headers=headers, data=data)

        json_data = response.json()

        if json_data['result_code'] == 0:
            self.newapptk = json_data['newapptk']
            print('visit_uamtk 成功，得到newapptk：', self.newapptk)
        else:
            print('visit_uamtk 失败：', json_data['result_message'])

    def visit_uamauthclient(self):
        url = 'https://kyfw.12306.cn/otn/uamauthclient'
        headers = {
            'Referer': 'https://kyfw.12306.cn/otn/passport?redirect=/otn/login/userLogin'
        }
        data = {
            'tk': self.newapptk
        }
        response = self.session.post(url, headers=headers, data=data)

        json_data = response.json()

        if json_data['result_code'] == 0:
            print('visit_uamauthclient 成功')
        else:
            print('visit_uamauthclient 失败：', json_data['result_message'])

    def _spilt_station_name(self, station_name):
        station_names = station_name.split('@')

        station_dict = {}
        for station_name in station_names:
            stations = station_name.split('|')
            if len(stations) > 2:
                station_dict[stations[1]] = stations[2]

        self.station_dict = station_dict
        print('站台信息分组完毕')

    def visit_station_name(self):
        url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js'
        headers = {
            'Referer': 'https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc'
        }
        r = self.session.get(url, headers=headers)
        text = r.text

        station_name_str = re.search(r"station_names ='(.*?)';", text).group(1)
        self._spilt_station_name(station_name_str)

    def _split_train_result(self, train_result):
        """ 将车次信息 根据 | 进行分割

            0:  类似一个key
            2:  train_no
            3： 车次：D311
            4： 始发站的 编号， VNP
            5： 终点站的 编号， SHH
            6:  出发地
            7： 目的地
            8： 出发时间
            9： 到达时间
            10： 历时时长
            12： 类似一个key
            13： 出发日期
            21： 高级软卧
            23： 软卧
            26： 无座
            30： 二等座
            31： 一等座
            32： 商务座/特等座

        :param train_result:
        :return:
        """
        self.train_li = [train.split('|') for train in train_result]

    def visit_leftTicket_query(self, train_date, from_station, to_station):
        self.train_date = train_date
        self.from_station = from_station
        self.to_station = to_station
        url = 'https://kyfw.12306.cn/otn/leftTicket/query'
        headers = {
            'Referer': 'https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc'
        }
        params = {
            'leftTicketDTO.train_date': train_date,
            'leftTicketDTO.from_station': self.station_dict[from_station],
            'leftTicketDTO.to_station': self.station_dict[to_station],
            'purpose_codes': 'ADULT',  # 普通 乘客
        }
        r = self.session.get(url, headers=headers, params=params)

        json_data = r.json()
        httpstatus = json_data['httpstatus']

        if httpstatus == 200:
            result = json_data['data']['result']
            print('获取车次信息成功:', result)
            self._split_train_result(result)
        else:
            print('获取车次信息失败:', json_data['messages'])

    def valid_seat(self, seat_type):
        """ 判断要购买的车次、座席是否有票

        :param seat_type:  座席类型
        :return:
        """

        for train in self.train_li:
            # seat 有几种情况
            # 有： 很多票， 无：没有票， 空： 没有票 ， 大于0的整数：有票
            seat = train[self.SEAT_TYPE_INDEX_DICT[seat_type]]

            if seat and seat != '无':
                # 只找第一个有座位的车次
                print('找到有效车次：', train[3], '车票剩余：', seat)
                # 将 匹配到的车次 设置为 当前车次
                self.current_train = train

                return True
            else:
                print('没有找到匹配车次')
                return False

    def visit_checkUser(self):
        url = 'https://kyfw.12306.cn/otn/login/checkUser'
        headers = {
            'Referer': 'https://kyfw.12306.cn/otn/leftTicket/init'
        }
        data = {
            '_json_att': ''  # 一定要写一个空值
        }
        r = self.session.post(url, headers=headers, data=data)

        json_data = r.json()

        if json_data['httpstatus'] == 200:
            print('visit_checkUser 成功')
        else:
            print('visit_checkUser 失败:', json_data['messages'])

    def visit_submitOrderRequest(self):
        url = 'https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest'
        headers = {
            'Referer': 'https://kyfw.12306.cn/otn/leftTicket/init',
            'Origin': 'https://kyfw.12306.cn'
        }
        data = {
            'secretStr': unquote(self.current_train[0]),  # 必须进行 unquote
            'train_date': self.train_date,
            'back_train_date': self.train_date,
            'tour_flag': 'dc',  # 单程     往返是： wc
            'purpose_codes': 'ADULT',
            'query_from_station_name': self.from_station,
            'query_to_station_name': self.to_station,
            'undefined': ''
        }

        r = self.session.post(url, headers=headers, data=data)

        json_data = r.json()

        if json_data['httpstatus'] == 200:
            print('visit_submitOrderRequest 成功')
        else:
            print('visit_submitOrderRequest 失败:', json_data['messages'])

    def visit_initDc(self):
        url = 'https://kyfw.12306.cn/otn/confirmPassenger/initDc'
        headers = {
            'Referer': 'https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc'
        }
        data = {
            '_json_att': ''
        }
        response = self.session.post(url, headers=headers, data=data)

        text = response.text

        self.globalRepeatSubmitToken = re.search(r"globalRepeatSubmitToken = '(.*?)';", text).group(1)

        print('visit_initDc成功，得到globalRepeatSubmitToke：', self.globalRepeatSubmitToken)

    def visit_getPassengerDTOs(self):
        url = 'https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs'
        headers = {
            'Referer': 'https://kyfw.12306.cn/otn/confirmPassenger/initDc'
        }
        data = {
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': self.globalRepeatSubmitToken
        }
        response = self.session.post(url, headers=headers, data=data)

        json_data = response.json()

        if json_data['httpstatus'] == 200:
            self.normal_passengers = json_data['data']['normal_passengers']
            print(f'visit_getPassengerDTOs 成功，得到 {len(self.normal_passengers)} 个联系人')
        else:
            print('visit_getPassengerDTOs 失败:', json_data['messages'])

    def visit_checkOrderInfo(self):
        url = 'https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo'
        headers = {
            'Referer': 'https://kyfw.12306.cn/otn/confirmPassenger/initDc'
        }
        data = {
            'cancel_flag': '2',
            'bed_level_order_num': '000000000000000000000000000000',
            'passengerTicketStr': '3,0,1,颜金娥,1,432524195803170023,13263281381,N',
            'oldPassengerStr': '颜金娥,1,432524195803170023,1_',
            'tour_flag': 'dc',
            'randCode': '',
            'whatsSelect': '1',
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': self.globalRepeatSubmitToken
        }

    def visit_getQueueCount(self):
        url = 'https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount'
        headers = {
            'Referer': 'https://kyfw.12306.cn/otn/confirmPassenger/initDc'
        }
        data = {
            'train_date': format_date(self.train_date),
            'train_no': self.current_train[2],
            'stationTrainCode': self.current_train[3],
            'seatType': '3',
            'fromStationTelecode': 'BJP',
            'toStationTelecode': 'SHH',
            'leftTicket': 'TIn%2Bxfz4wF7vFdPPGpJM3Ot2eq4jJkutTiGe%2BBG1H6tV8aOpy7oR3qsbrcI%3D',
            'purpose_codes': '00',
            'train_location': 'P2',
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': '36b5ea1a750cc30b048ffd1ea1866dc5'
        }

if __name__ == '__main__':
    username = 'mumuloveshine'
    password = 'mumu2018'
    train_date = '2018-12-17'
    from_station = '北京'
    to_station = '上海'
    seat_type = '一等座'

    spider_12306 = S12306Spider(username, password)

    spider_12306.visit_resources_login()
    spider_12306.visit_captcha_check_until_success()
    spider_12306.visit_passport_web_login()

    spider_12306.visit_uamtk()
    spider_12306.visit_uamauthclient()

    spider_12306.visit_station_name()
    spider_12306.visit_leftTicket_query(train_date, from_station, to_station)
    b = spider_12306.valid_seat(seat_type)

    if b:
        spider_12306.visit_checkUser()
        spider_12306.visit_submitOrderRequest()
        spider_12306.visit_initDc()
        spider_12306.visit_getPassengerDTOs()
