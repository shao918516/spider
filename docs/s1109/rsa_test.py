#!/usr/bin/env python
# -*- coding: utf-8 -*-
import base64

__author__ = 'Terry'

'''
    RSA:
    公钥加密算法，一种非对称密码算法
    公钥加密，私钥解密

    3个参数：
    rsa_n， rsa_e，message
    rsa_n, rsa_e  用于生成公钥
    message： 需要加密的消息
    
    
    每次加密后的值都不一样(通常情况下)
    极个别情况下， 加密过程中的填充值，不是随机，是固定的
    那么就会造成， 同样的 publickey 多次加密 同一个 密码， 得到一样的值
'''
import rsa
import binascii

# def rsa_encrypt(rsa_n, rsa_e, message):
#     key = rsa.PublicKey(rsa_n, rsa_e)  # 创建公钥
#     message = rsa.encrypt(message, key)  # 加密
#     message = binascii.b2a_hex(message)  # 将加密信息转换为16进制
#     return message.decode()
#
# pubkey = 'EB2A38568661887FA180BDDB5CABD5F21C7BFD59C090CB2D245A87AC253062882729293E5506350508E7F9AA3BB77F4333231490F915F6D63C55FE2F08A49B353F444AD3993CACC02DB784ABBB8E42A9B1BBFFFB38BE18D78E87A0E41B9B8F73A928EE0CCEE1F6739884B9777E4FE9E88A1BBE495927AC4A799B3181D6442443'
# print("pubkey length：%s" % len(pubkey))
# rsa_n = int(pubkey, 16)
# rsa_e = int('10001', 16) # js里面一般是 parseInt('10001', 16)
# text = '需要加密的字符串'
# print(rsa_encrypt(rsa_n, rsa_e, text.encode()))
# print(len(rsa_encrypt(rsa_n, rsa_e, text.encode())))


from Crypto.Cipher import PKCS1_v1_5, PKCS1_OAEP
from Crypto.PublicKey import RSA

# 这是百度密码的加密函数
def encript_password(pubkey, password):
    pub = RSA.importKey(pubkey)
    #构造“加密器”
    # PKCS1_OAEP 和 PKCS1_v1_5
    encryptor=PKCS1_v1_5.new(pub)
    #加密的内容必须为bytes类型
    en_passwd =encryptor.encrypt(password.encode())
    # 使用base64进行编码
    return base64.b64encode(en_passwd).decode()

pubkey= '-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDKr6Qn6VtqKdKpRXbSl9XkT3qN\nWJFK7U9QNNx6d+hsv3e77H7p0RLtXw8mBWNdPI8\/afA8Oo0IaskdBAIwkiDKm1T+\nV9v8+ggHAL3Haz04zgq3uYAzZp3ydETyqtQ3ayFbvFTq94x5jaeS8xxkKEmjT6AG\n3P\/ZGCMoqvxD37gqrQIDAQAB\n-----END PUBLIC KEY-----\n'
pwd = 'mumu2018'
print(encript_password(pubkey, pwd))
print(encript_password(pubkey, pwd))