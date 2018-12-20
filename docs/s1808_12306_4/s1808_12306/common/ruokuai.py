#!/usr/bin/env python
# -*- coding: utf-8 -*-

from hashlib import md5
import time

from common.control_helper import RetryException, call_until_success
from common.requests_helper import make_session

CREATE_URL = 'http://api.ruokuai.com/create.json'
REPORTERROR_URL = 'http://api.ruokuai.com/reporterror.json'

class DaMaException(Exception):
    pass

class Ruokuai:

    def __init__(self, s, user, pwd, soft_id='7545', soft_key='df49bdfd6416475181841e56ee1dc769', image_type="3040", timeout=60):
        """

        :param s: requests的 session对象
        :param user: 若快的用户名
        :param pwd: 若快的密码
        :param soft_id: 软件id
        :param soft_key: 软件的key
        :param image_type: 打码类型,参考http://ruokuai.com/pricelist.aspx
        :param timeout: 超时时间
        """
        self.write_log = print
        self.timeout = timeout
        self.image_type = image_type
        self.s = s
        self.soft_key = soft_key
        self.soft_id = soft_id
        self.pwd = md5(pwd.encode()).hexdigest()
        self.user = user

        self.create_data = self._make_data({
            'typeid': image_type,
            'timeout': timeout,
        })

    def _make_data(self, data):
        base_data = {
            'username': self.user,
            'password': self.pwd,
            'softid': self.soft_id,
            'softkey': self.soft_key,
        }
        base_data.update(data)
        return base_data

    def create_manual(self, get_vcode_data_func):
        content = get_vcode_data_func()
        with open('vcodde.jpg', 'wb') as f:
            f.write(content)

        vcode = input('请输入验证码：')
        return vcode, '手动打码'

    @call_until_success()
    def create(self, get_vcode_data_func):
        """ 提交一个打码任务

        :param get_vcode_data_func: 校验码二进制数据获取函数
        """

        #  构造一个最简单的 文件提交 参数
        # 2个参数， 第一个是 文件名， 第二个是 文件的bytes
        files = {'image': ('a.jpg', get_vcode_data_func())}

        try:
            r = self.s.post(CREATE_URL, data=self.create_data, files=files)

            # 如果 response的 body为空
            if not r.text:
                # 抛出一个 RetryException
                raise RetryException()
            j = r.json()
        except ValueError:
            self.write_log("若快返回ValueError：[%s]" % r.text)
            time.sleep(1)
            raise RetryException()
        except:
            # traceback.print_exc()
            self.write_log("若快返回未知异常：[%s]" % r.text)
            #  做一秒的延时，是防止 不间断 的访问网络
            time.sleep(1)
            # 抛出 RetryException 异常，这个异常会在 call_until_success 装饰器中捕获
            raise RetryException()

        if "Result" in j and "Id" in j:
            self.write_log("若快返回验证码：[%s]" % j["Result"])
            return j["Result"], j["Id"]
        elif "已经损坏或者不是正确的图像格式" in j.get("Error",""):
            time.sleep(1)
            raise RetryException()
        else:
            self.write_log("若快返回异常2：[%s]" % r.text)
            raise DaMaException("若快服务返回异常数据[%s]" % r.text)

    def report_error(self, id):
        """
        im_id:报错题目的ID
        """
        data = self._make_data({
            'id': id,
        })
        r = self.s.post(REPORTERROR_URL, data=data)
        text = r.text
        if "报告成功" in text or "报错成功" in text:
            self.write_log("若快提交验证码错误成功")
            pass
        else:
            self.write_log("若快提交验证码错误失败：" + text)
            raise DaMaException("若快报告错误异常[%s]" % text)

    def info(self):
        url = 'http://api.ruokuai.com/info.json'
        data = {
            'username': self.user,
            'password': self.pwd
        }
        r = self.s.post(url, data=data)
        return r.text

def create_dama(*args, **kwargs):
    return Ruokuai(*args, **kwargs)

if __name__ == '__main__':
    dm = create_dama(make_session(), 'mumuloveshine', 'mumu2017', image_type='6113')

    def get_vcode_data_func():
        with open('vcode1.jpg', 'rb') as f:
            data = f.read()
        return data

    result = dm.create(get_vcode_data_func)
    print(result)

    