#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Terry'

'''
    base64：
    是网络上最常见的用于传输8Bit字节码的编码方式之一，
    Base64就是一种基于64个可打印字符来表示二进制数据的方法，用于在HTTP环境下传递较长的标识信息
    后一两位可能有“=”
    防君子不防小人，很容易解密

    64种可能： 0000000 - 00111111

    输出为 A-Z、a-z、0-9和"+"、"/" 字符组成的字符串
    在urlencode中：  _   -   替换  +   / 
    很多时候字符串尾部为 1个或2个  "="

    base64基本原理：每3个字节为一组，拆为4个字节
    3个十六进制字节：    A1       B2        C3
    二进制显示：     1010 0001 1011 0010 1100 0011  # 总共 24 位
    将24位以6位一组拆分4组： 101000 011011 001011 000011
    每组前面补 00:         00101000 00011011 00001011 00000011
    转为对应的 十六进制：  28  1B  0B  03

    把3个字节的二进制拼接， 24位， 按6位分割，变成4个字节，每个字节小于64
    最后留下1个字节的时候，会在尾部添加 2个 '='
    最后留下2个字节的时候，会在尾部添加 1个 '='


    特征：
    任意长度(4的倍数)，有大小写字母、数字、2个特殊字符（+和/ 或者 -和_），尤其是 尾部为 = 或 ==
    就要猜测这个串是base64， 字符数永远是4个倍数
'''

import base64

s = '我爱你中国，中国万岁万岁万万岁！中文测试askdjk123nas0d988178236任意长度(4的倍数)，有大小写字母、数字、2个特殊字符（+和/ 或者 -和_）'

# 会按57个字节的长度为间隔 加入 \n
# s1 = base64.encodebytes(s.encode())
# print(s1)
# s3 = base64.decodebytes(s1).decode()
# print(s3)


# 最常用的base64 加密，可以自定义替换 + 和 /
# s2 = base64.b64encode(s.encode())
# print(s2)
# s4 = base64.b64decode(s2).decode()
# print(s4)

# 手动指定替换 + / 的字符 ，使用一个 2个字符 的 字节串，譬如 b'@#'
# s2 = base64.b64encode(s.encode(), b'@#')
# print(s2)
# 转换回去，也必须指定相同的替换 字节串 b'@#' , 否则抛出 binascii.Error: Incorrect padding
# s4 = base64.b64decode(s2, b'@#').decode()
# print(s4)

# #
# # # # 标准base64加密，等同于不带额外参数的 b64encode
# s5 = base64.standard_b64encode(s.encode())
# print(s5)
# s6 = base64.standard_b64decode(s5)
# print(s6.decode())
#
# # url安全的，会把 + 替换为 - ， 把 / 替换为 _
# # 等同于 base64.b64encode(s.encode(), b'-_') base64.b64decode(s2, b'-_')
# s7 = base64.urlsafe_b64encode(s.encode())
# print(s7)
# s8 = base64.urlsafe_b64decode(s7)
# print(s8.decode())