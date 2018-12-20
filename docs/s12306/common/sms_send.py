#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from urllib import parse
from common.request_helper import make_session

__author__ = 'Terry'

YUNPIAN_SINGLE_URL = 'https://sms.yunpian.com/v2/sms/tpl_single_send.json'
APIKEY = '2e4bc7f7069477f6b35ccda2ee775c10'
TPL_ID = 1869322
CODE_LENGTH = 4
MSG = '您的车票已经购买成功，请尽快付款！！！'

def send_sms_single(apikey, code, mobile, tpl_id):
    s = make_session()
    params = {
        'apikey': apikey,
        'tpl_id':tpl_id,
        'mobile':mobile,
        'tpl_value':parse.urlencode({'#code#':code})
    }
    r = s.post(YUNPIAN_SINGLE_URL, params)
    json_data = r.json()
    print('发送短信：', r.text)
    if json_data['code'] == 0:
        return True
    else:
        return False

def send_sms(mobile):
    b = send_sms_single(APIKEY, MSG, mobile, TPL_ID)
    if b:
        return b
    else:
        return False

if __name__ == '__main__':
    send_sms('13929711995')