#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Terry'

"""
    3DES 加密
    3DES（即Triple DES）是DES向AES过渡的加密算法，
    使用两个密钥，执行三次DES算法，
    加密的过程是加密-解密-加密
    解密的过程是解密-加密-解密
"""

# 3DES 加密
from Crypto.Cipher import DES3
from Crypto import Random
import binascii

key = 'Sixteen byte key'
msg = 'sona si latine loqueris '
iv = Random.new().read(DES3.block_size)
# print(iv)
def des3_encrypt(key, msg):
    cipher = DES3.new(key, DES3.MODE_OFB, iv)
    msg = iv + cipher.encrypt(msg)
    msg = binascii.b2a_hex(msg)
    return msg.decode()

s = des3_encrypt(key.encode(), msg.encode())
print(s)