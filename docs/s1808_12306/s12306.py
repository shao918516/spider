#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import re
import time
from urllib.parse import unquote

from docs.s1808_12306.common.manual import Manual
from common.requests_helper import make_session
from docs.s1808_12306.common.ruokuai import Ruokuai
from docs.s1808_12306.common.util import get_13_time
import urllib3
urllib3.disable_warnings()
__author__ = 'Terry'

class S12306Spider:

    def __init__(self, username, password):
        self.session = make_session(True)

        self.username = username
        self.password = password

        # 手动打码
        # self.dm = Manual()
        # 若快打码
        self.dm = Ruokuai(self.session, 'mumuloveshine', 'mumu2017', image_type='6113')

    def visit_resources_login(self):
        url_index = 'https://www.12306.cn/index/'
        self.session.get(url_index)

        url_login = 'https://kyfw.12306.cn/otn/resources/login.html'
        headers = {
            'Referer':'https://www.12306.cn/index/',
        }
        self.session.get(url_login,headers=headers)

    def _visit_captcha_image(self):
        url = 'https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand&' + str(random.random())
        # 一定要用 self.session
        r = self.session.get(url)

        # 返回图片的 bytes
        return r.content

    def _visit_captcha_image64(self):
        url = 'https://kyfw.12306.cn/passport/captcha/captcha-image64'
        t = get_13_time()
        headers = {
            'Accept': 'application/json'
        }
        params = {
            'login_site': 'E',
            'module': 'login',
            'rand': 'sjrand',
            t: '',
            # 'callback': 'jQuery1910292836177545567_1542355491387',
            '_': str(int(t) - random.randint(1800, 2500)),
        }
        # 一定要用 self.session
        r = self.session.get(url, headers=headers, params=params)

        json_data = r.json()

        image = json_data['image']

        import base64
        content = base64.b64decode(image)
        # 返回图片的 bytes
        return content

    def get_vcode(self):
        self.vcode, self.vcode_id = self.dm.create(self._visit_captcha_image64)
        answer = None
        for i in range(len(self.vcode)):
            x_start = 5
            y_start = 10
            x_end = 71
            y_end = 76
            gap = 72
            posi = int(self.vcode[i])
            if (posi >= 1 and posi <= 4):
                x_start = x_start + (posi-1) * gap
                x_end = x_end + (posi-1) * gap
            elif (posi >= 5 and posi <= 8):
                x_start = x_start + (posi - 5) * gap
                x_end = x_end + (posi - 5) * gap
                y_start += gap
                y_end += gap
            x=random.randint(x_start, x_end)
            y=random.randint(y_start, y_end)
            if not answer:
                answer=str(x)+','+str(y)
            else:
                answer=answer+','+str(x)+','+str(y)

        # 实现 '1357' 换还为  '42,42,182,36,40,113,180,108'   的函数
        return answer

    def _visit_captcha_check(self):
        url = 'https://kyfw.12306.cn/passport/captcha/captcha-check'
        answer = self.get_vcode()
        params = {
            # 'callback': 'jQuery1910292836177545567_1542355491387',
            'answer': answer,
            'rand': 'sjrand',
            'login_site': 'E',
            '_': get_13_time(),
        }
        response = self.session.get(url, params=params)
        print(response.text)
        text = response.text
        try:
            json_data = response.json()
            result_code = json_data['result_code']
        except:
            result_code = re.search(r'<result_code>([0-9]+)</result_code>',  text, re.RegexFlag.S).group(1)

        if result_code == "4":
            print('验证码成功')
            return True
        else:
            print('验证码失败')
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


    def visit_passport_web_login(self,answer):
        url = 'https://kyfw.12306.cn/passport/web/login'
        data = {
            'username': self.username,
            'password': self.password,
            'appid': 'otn',
            'answer': answer
        }
        headers = {
            'Referer': 'https://kyfw.12306.cn/otn/resources/login.html'
        }

        response = self.session.post(url, headers=headers, data=data)
        text = response.text
        print(text)
        try:
            json_data = response.json()
            result_code = json_data['result_code']
        except:
            result_code = re.search(r'<result_code>([0-9]+)</result_code>',  text, re.RegexFlag.S).group(1)

        if result_code == "0":
            print('登录成功')
        else:
            print('登录失败:', result_code)

    def redirect_user_login(self):
        url_redirect = 'https://kyfw.12306.cn/otn/passport'
        headers = {
            'Referer':'https://kyfw.12306.cn/otn/resources/login.html'
        }
        params = {
            'redirect':'/otn/login/userLogin'
        }

        response = self.session.get(url_redirect, headers=headers, params=params)
        print(response.cookies)

    def passport_web_auth_uamtk(self):
        url_auth_uamtk = 'https://kyfw.12306.cn/passport/web/auth/uamtk'
        headers = {
            'Referer': 'https://kyfw.12306.cn/otn/passport?redirect=/otn/login/userLogin',
        }
        form_data = {
            'appid': 'otn',
        }

        response = self.session.post(url_auth_uamtk, headers=headers, data=form_data)
        json_data = response.json()
        self.newapptk = json_data["newapptk"]

    def uamauthclient_tk_jsession(self):
        url_tk = 'https://kyfw.12306.cn/otn/uamauthclient'
        headers = {
            'Referer': 'https://kyfw.12306.cn/otn/passport?redirect=/otn/login/userLogin',
        }
        form_data = {
            'tk': self.newapptk,
        }
        response = self.session.post(url_tk, headers=headers, data=form_data)
        print(response.text)

    def visit_search_station_info(self,single_return_flag,from_station,to_station,ride_date,train_no):
        self.single_return_flag = single_return_flag
        self.from_station = from_station
        self.to_station = to_station
        self.ride_date = ride_date
        self.train_no = train_no

        url = f'https://kyfw.12306.cn/otn/leftTicket/init'
        headers = {
            'Referer':'https://www.12306.cn/index/index.html'
        }
        params = {
            'linktypeid': single_return_flag,
            'fs': from_station,
            'ts': to_station,
            'date': ride_date,
            'flag': 'N,N,Y'
        }

        response = self.session.get(url,headers=headers,params=params)
        text = response.text
        # scriptVersion = re.search(r'common_js.js\?scriptVersion=(.*?)"',text).group(1)
        self.station_version = re.search(r'station_name.js\?station_version=(.*?)"',text).group(1)
        referer_url = response.url
        flag_quote = re.search(r'flag=(.*?)$',referer_url).group(1)
        self.referer_url = response.url.replace(flag_quote,unquote(flag_quote))

    def get_station_code(self):
        url_station_code = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js'
        headers = {
            'Referer': self.referer_url,
        }
        params = {
            'station_version': self.station_version,
        }

        response = self.session.get(url_station_code, headers=headers, params=params)
        text = response.text
        station_name_str = re.search(r"station_names ='(.*?)';", text).group(1)
        self._spilt_station_name(station_name_str)
        # self.from_station_code = re.search(f'\|{self.from_station}\|(.*?)\|',text).group(1)
        # self.to_station_code = re.search(f'\|{self.to_station}\|(.*?)\|',text).group(1)
        # print(self.from_station_code,self.to_station_code)

    def _spilt_station_name(self, station_name):
        station_names = station_name.split('@')

        station_dict = {}
        for station_name in station_names:
            if len(station_name) > 2:
                stations = station_name.split('|')
                station_dict[stations[1]] = stations[2]
        self.station_dict = station_dict
        print('站台信息分组完毕')

    def get_trains_info(self):
        url_secret_str = 'https://kyfw.12306.cn/otn/leftTicket/query'
        headers = {
            'Referer': 'https://www.12306.cn/index/index.html',
        }
        params = {
            'leftTicketDTO.train_date': self.ride_date,
            'leftTicketDTO.from_station': self.station_dict[self.from_station],
            'leftTicketDTO.to_station': self.station_dict[self.to_station],
            'purpose_codes': 'ADULT'
        }

        response = self.session.get(url_secret_str, headers=headers, params=params)

        train_json = response.json()
        trains_info = train_json['data']['result']
        self._split_train_result(trains_info)

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

    SEAT_TYPE_INDEX_DICT = {
        '高级软卧': 21,
        '软卧': 23,
        '硬卧': 27,
        '无座': 26,
        '二等座': 30,
        '一等座': 31,
        '商务座': 32,
        '特等座': 32
    }

    def valid_train_seat(self, train_no, seat_type):
        seat_index = self.SEAT_TYPE_INDEX_DICT[seat_type]

        for train in self.train_li:
            if train_no == train[3]:
                sign = train[seat_index]
                if sign and sign != '无':
                    # 只找第一个有座位的车次
                    print(f'找到有效车次：{train[3]}，席别：{seat_type}，车票剩余：{sign}')
                    # 将 匹配到的车次 设置为 当前车次
                    self.current_train = train
                    return True
                else:
                    print('没有找到匹配车次')
                    return False

    def check_user_login(self):
        url_check_user_login = 'https://kyfw.12306.cn/otn/login/checkUser'
        headers = {
            'Referer': self.referer_url,
        }
        form_date = {
            '_json_att=': '',
        }

        response = self.session.post(url_check_user_login, headers=headers, data=form_date)
        login_flag = response.json()['data']['flag']
        return login_flag

    def submit_order_request(self):
        url_submit_order = 'https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest'
        headers = {
            'Referer': self.referer_url,
        }
        form_date = {
            'secretStr': unquote(self.current_train[0]),
            'train_date': self.ride_date,
            'back_train_date': time.strftime('%Y-%m-%d',time.localtime(time.time())),
            'tour_flag': self.single_return_flag,
            'purpose_codes': 'ADULT',
            'query_from_station_name': self.from_station,
            'query_to_station_name': self.to_station,
            'undefined': ''
        }

        response = self.session.post(url_submit_order, headers=headers, data=form_date)
        print(response.text)

    def confirm_passenger_init_dc(self):
        url = 'https://kyfw.12306.cn/otn/confirmPassenger/initDc'
        headers = {
            'Referer': self.referer_url,
        }
        form_date = {
            '_json_att': '',
        }

        response = self.session.post(url, headers=headers, data=form_date)
        text=response.text
        self.submit_token = re.search(r"var globalRepeatSubmitToken = '(.*?)';",text).group(1)
        self.key_check_isChange = re.search(r"'key_check_isChange':'(.*?)'", text).group(1)
        self.train_location = re.search(r"'train_location':'(.*?)'", text).group(1)

    def get_passenger_dtos(self):
        url = 'https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs'
        headers = {
            'Referer': 'https://kyfw.12306.cn/otn/confirmPassenger/initDc',
        }
        form_date = {
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': self.submit_token
        }

        response = self.session.post(url, headers=headers, data=form_date)
        self.json_user = response.json()["data"]["normal_passengers"]

    def check_order_info(self):
        url_js = 'https://kyfw.12306.cn/otn/resources/merged/queryLeftTicket_end_js.js'
        response = self.session.get(url_js)
        text = response.text
        cancel_flag = re.search('&cancel_flag=(.*?)&',text).group(1)
        bed_level_order_num = re.search('&bed_level_order_num=(.*?)&',text).group(1)

        url = 'https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo'
        headers = {
            'Referer': 'https://kyfw.12306.cn/otn/confirmPassenger/initDc',
        }
        form_date = {
            'cancel_flag': cancel_flag,
            'bed_level_order_num': bed_level_order_num,
            'passengerTicketStr': f'{self.current_train[14]},{self.json_user[0]["passenger_flag"]},{self.json_user[0]["passenger_type"]},{self.json_user[0]["passenger_name"]},{self.json_user[0]["passenger_id_type_code"]},{self.json_user[0]["passenger_id_no"]},{self.json_user[0]["mobile_no"]},N',
            'oldPassengerStr': f'{self.json_user[0]["passenger_name"]},{self.json_user[0]["passenger_id_type_code"]},{self.json_user[0]["passenger_id_no"]},1_',
            'tour_flag': self.single_return_flag,
            'randCode': '',
            'whatsSelect': '1',
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': self.submit_token
        }

        response = self.session.post(url, headers=headers, data=form_date)
        print(response.text)

    def get_queue_count(self):
        url = 'https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount'
        headers = {
            'Referer': 'https://kyfw.12306.cn/otn/confirmPassenger/initDc',
        }
        form_date = {
            'train_date': time.strftime("%a %b %d %Y", time.localtime()) + ' 00:00:00 GMT+0800 (中国标准时间)',
            'train_no': self.current_train[2],
            'stationTrainCode': self.current_train[3],
            'seatType': self.current_train[14],
            'fromStationTelecode': self.station_dict[from_station],
            'toStationTelecode': self.station_dict[to_station],
            'leftTicket': self.current_train[12],
            'purpose_codes': '00',
            'train_location': self.current_train[15],
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': self.submit_token
        }

        response = self.session.post(url, headers=headers, data=form_date)
        print(response.text)

    def confirm_single_for_queue(self):
        url = 'https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue'
        headers = {
            'Referer': 'https://kyfw.12306.cn/otn/confirmPassenger/initDc',
        }
        form_date = {
            'passengerTicketStr': f'{self.json_user[0]["code"]},{self.json_user[0]["passenger_flag"]},{self.json_user[0]["passenger_type"]},{self.json_user[0]["passenger_name"]},{self.json_user[0]["passenger_id_type_code"]},{self.json_user[0]["passenger_id_no"]},{self.json_user[0]["mobile_no"]},N',
            'oldPassengerStr': f'{self.json_user[0]["passenger_name"]},{self.json_user[0]["passenger_id_type_code"]},{self.json_user[0]["passenger_id_no"]},1_',
            'randCode': '',
            'purpose_codes': '00',
            'key_check_isChange': self.key_check_isChange,
            'leftTicketStr': self.current_train[12],
            'train_location': self.train_location,
            'choose_seats': '',
            'seatDetailType': '000',
            'whatsSelect': '1',
            'roomType': '00',
            'dwAll': 'N',
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': self.submit_token
        }

        response = self.session.post(url, headers=headers, data=form_date)
        print(response.text)

    def query_order_wait_time(self, random_int):
        url = 'https://kyfw.12306.cn/otn/confirmPassenger/queryOrderWaitTime'
        headers = {
            'Referer': 'https://kyfw.12306.cn/otn/confirmPassenger/initDc',
        }
        form_date = {
            'random': str(int(time.time()*1000 + random_int)),
            'tourFlag': self.single_return_flag,
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': self.submit_token,
        }

        response = self.session.post(url, headers=headers, data=form_date)
        print(response.text)

if __name__ == '__main__':
    username = 'shao918516'
    password = 'pengfei_1'

    # single_flag = 'dc', return_flag = 'wf'
    single_return_flag = 'dc'      # 单程/往返标志
    from_station = '北京'    # 起始站
    to_station = '廊坊'    # 到站
    ride_date = '2018-12-12'    # 乘车日期
    train_no = 'K215'    # 车次
    seat_type = '商务座'

    # 创建12306乘车订票类
    spider_12306 = S12306Spider(username, password)
    # 访问首页
    spider_12306.visit_resources_login()
    # 校验验证码
    answer = spider_12306.visit_captcha_check_until_success()
    # 登录
    spider_12306.visit_passport_web_login(answer)
    # 跳转主页
    # spider_12306.redirect_user_login()
    # 获取newapptk
    spider_12306.passport_web_auth_uamtk()
    # 设置cookie
    spider_12306.uamauthclient_tk_jsession()


    # 查询车票信息
    spider_12306.visit_search_station_info('dc','北京','廊坊','2018-12-12','K215')
    # 获取车站代码
    spider_12306.get_station_code()
    # 获取 trains_info，预定信息的车次代码
    spider_12306.get_trains_info()
    # 检查是否有座，无座返回
    valid_seat = spider_12306.valid_train_seat(train_no,seat_type)
    if not valid_seat:
        print(f"{ride_date}，自{from_station}开往{to_station}的{train_no}，无{seat_type}席别，请重新选择!!!")
    else:
        # 检查是否登录
        login_flag_check = spider_12306.check_user_login()
        # 检查登录配置
        if login_flag_check == False:
            spider_12306.check_login_conf()
            # 校验验证码
            answer = spider_12306.visit_captcha_check_until_success()
            # 登录
            login_flag2 = spider_12306.visit_passport_web_login(answer)
            # 获取newapptk
            spider_12306.passport_web_auth_uamtk()
            # 设置cookie
            spider_12306.uamauthclient_tk_jsession()

        # 发送提交订单请求
        spider_12306.submit_order_request()
        # 获取submit_token
        spider_12306.confirm_passenger_init_dc()
        # 获取乘客信息
        spider_12306.get_passenger_dtos()
        # 检查订单信息
        spider_12306.check_order_info()
        # 获取排队及剩余票数信息
        spider_12306.get_queue_count()
        # # 确定单程排队信息
        # spider_12306.confirm_single_for_queue()
        # # 查询订单等待时间
        # spider_12306.query_order_wait_time(0)
        # spider_12306.query_order_wait_time(random.randint(2500,3500))












