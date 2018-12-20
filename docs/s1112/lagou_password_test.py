#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Terry'

def lagou_encrypt_password(password):
    """ 实现 拉勾网 的密码加密

    :param password:  加密后的密码
    :return:
    """
    import hashlib

    # 第一次 md5 加密
    password = hashlib.md5(password.encode()).hexdigest()

    # 加 盐
    v = "veenike"
    password = v + password + v

    # 第二次 md5 加密
    password = hashlib.md5(password.encode()).hexdigest()
    return password

if __name__ == '__main__':
    password = 'mumu2018'
    print(lagou_encrypt_password(password))