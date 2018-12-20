#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Terry'

'''
    MD5:
    Message-Digest Algorithm 5（摘要算法5）
    1、压缩性：任意长度的数据，算出的MD5值长度都是固定的, 长度 32。
    2、容易计算：从原数据计算出MD5值很容易。
    3、抗修改性：对原数据进行任何改动，哪怕只修改1个字节，所得到的MD5值都有很大区别。
    4、强抗碰撞：已知原数据和其MD5值，想找到一个具有相同MD5值的数据（即伪造数据）是非常困难的。

    输出为 128 bit，  每4位二进制组合一个十六进制字符，一般输出为 长度 32 个16进制字符串

    特征：
    1、结果是 32个字符的16进制字符串
    2、任意2个不同的对象，计算出的md5值，不可能相同
    3、同一个对象，不管计算多少次，计算出的值永远相同
'''

import hashlib

s = 'this is a md5 test.'
# 得到 md5 对象
m = hashlib.md5()
# 传入需要计算的 原始内容
m.update(s.encode())
# 打印 md5 值
s_md5 = m.hexdigest()

# print('原始第一次计算的md5值：', s_md5)

s_md5_2 = hashlib.md5(s_md5.encode()).hexdigest()
# print('再次使用一个新的md5对象，计算的md5值：', s_md5_2)

m.update(s_md5.encode())
# print('第一个md5对象，计算第二次的md5值：', m.hexdigest())

# 一般的简便写法
print(hashlib.md5(s.encode()).hexdigest())