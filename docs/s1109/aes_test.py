#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Terry'


'''
    AES：
    高级加密标准（英语：Advanced Encryption Standard，缩写：AES），这个标准用来替代原先的DES
    AES的区块长度固定为128 比特，密钥长度则可以是128，192或256比特 （16、24和32字节）
    大致步骤如下：
    1、密钥扩展（KeyExpansion），
    2、初始轮（Initial Round），
    3、重复轮（Rounds），每一轮又包括：SubBytes、ShiftRows、MixColumns、AddRoundKey，
    4、最终轮（Final Round），最终轮没有MixColumns。
'''

from Crypto.Cipher import AES
from Crypto import Random
import binascii

# 加密
key = b'b6ce159334e155d8'
msg = b'Attack at dawn'
iv = Random.new().read(AES.block_size) # 16字节长度
cipher = AES.new(key, AES.MODE_CFB, iv)
msg = cipher.encrypt(msg)
print(binascii.b2a_hex(msg))


# # 解密
cipher = AES.new(key, AES.MODE_CFB, iv)
msg1 = cipher.decrypt(msg)
print(msg1)
