#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Terry'



'''
    DES:
    全称为Data Encryption Standard，即数据加密标准，是一种使用密钥加密的块算法
    入口参数有三个：Key、Data、Mode
    Key为7个字节共56位，是DES算法的工作密钥；
    Data为8个字节64位，是要被加密或被解密的数据；
    Mode为DES的工作方式,有两种:加密或解密

    3DES（即Triple DES）是DES向AES过渡的加密算法，
    使用两个密钥，执行三次DES算法，
    加密的过程是加密-解密-加密
    解密的过程是解密-加密-解密

    pycrypto安装指南：
    帮助文档（https://www.dlitz.net/software/pycrypto/api/current/）
    要先安装VC2015：microsoft visual studio 2015(14)
    1、http://blog.csdn.net/a624806998/article/details/78596543
        在执行 python setup.py install 之前，运行
        set CL=/FI"%VCINSTALLDIR%\\INCLUDE\\stdint.h" %CL%
    2、出现ImportError: No module named 'winrandom'错误
        处理：修改python3安装目录下的 lib/Crypto/Random/OSRNG/nt.py 文件中找到
        import winrandom
        修改为
        from Crypto.Random.OSRNG import winrandom
'''

# DES 加密
from Crypto.Cipher import DES
from Crypto.Util import Counter
from Crypto import Random
import binascii

key = '-8B key-' # 长度为8
msg = 'We are no longer the knights who say ni!'
# noce不是一定有的
nonce = Random.new().read(int(DES.block_size/2))

def des_encrypt(key, msg):
    ctr = Counter.new(int(DES.block_size*8/2), prefix=nonce)
    cipher = DES.new(key, DES.MODE_CTR, counter=ctr)
    msg = nonce + cipher.encrypt(msg)
    msg = binascii.b2a_hex(msg)
    return msg.decode()

print(des_encrypt(key.encode(), msg.encode()))