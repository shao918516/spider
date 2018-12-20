#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import traceback

import time

__author__ = 'Terry'

class RetryException(Exception):
    pass

class RetryOvertimesException(Exception):
    pass

def call_until_success(try_times=10, retry_exceptions=None, sleep_time=.5):
    """
        装饰器，自动重试
    :param try_times: 重试次数
    :param retry_exceptions: 进行重试的异常对象列表
    :param sleep_time: 每次重试的间隔等待时间
    :return:
    """
    if not retry_exceptions:
        retry_exceptions = []

    # 所有 需要进行 重试的 异常的 元组
    all_retry_exceptions = tuple(retry_exceptions + [RetryException])
    def dec(func):
        def __decorator(*args, **kwargs):
            """
            调用fun,直到成功
            """
            times = 0
            while 1:
                try:
                    return func(*args, **kwargs)
                # 所有需要进行重试的 异常 捕获
                except all_retry_exceptions:
                    times = times + 1

                    # 如果超过最大异常次数，那么抛出 RetryOvertimesException重试次数超出 的异常
                    if times > try_times:
                        raise RetryOvertimesException("[%s]重试次数超过%s,放弃" % (func.__name__, try_times))
                except:
                    print("未知异常")
                    traceback.print_exc()
                    raise Exception()

                time.sleep(sleep_time)

        return __decorator
    return dec

