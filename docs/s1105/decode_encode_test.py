#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

__author__ = 'Terry'


"""
    encode
    把 str 转换为 bytes
"""
s = '中文abc123'

# 普通的转换 ， 不填写转换的编码，那么默认是 UTF-8
# print('默认编码：', s.encode())
# # 指定转换的编码集
# print('utf-8编码：', s.encode('utf-8'))
# print('gbk编码：', s.encode('gbk'))

# errors的处理：
# strict 默认，  出现不能转换的字符，则 抛出错误 UnicodeEncodeError
# print(s.encode('ascii'))
# print(s.encode('ascii', 'strict'))

# ignore， 忽略错误的字符 ， 不可逆
# print(s.encode('ascii', 'ignore'))

# replace  使用 ?  替换错误的字符，  不可逆
print('encode 的 replace：', s.encode('ascii', 'replace'))

# xmlcharrefreplace  , 使用 &#20013; 这样的类型 替换 错误的字符 ， 可逆
xmlcharrefreplace_str = s.encode('ascii', 'xmlcharrefreplace')
# print('xmlcharrefreplace_str:', xmlcharrefreplace_str)

def xmlchar_2_cn(s):
    def convert_callback(matches):
        char_id = matches.group(1)
        try:
            return chr(int(char_id))
        except:
            return char_id

    # 正则的 sub， 替换
    # 第二个参数，是可以使用 函数
    # 正则表达式中， 表达式和操作的字符串 必须同为  str 或者 bytes,
    # 否则抛出 TypeError: cannot use a string pattern on a bytes-like object 错误
    ret = re.sub("&#(\d+)(;|(?=\s))", convert_callback, s)

    return ret

# print('xmlcharrefreplace_str 转换 字符串：', xmlchar_2_cn(xmlcharrefreplace_str.decode()))

# backslashreplace ， 使用unicode 转换错误字符， 可逆
# unicode_str = s.encode('ascii', 'backslashreplace')
# print('backslashreplace 转换:', unicode_str)
# # unicode-escape 将 unicode 转 str
# print('unicode 转换 str :', unicode_str.decode('unicode-escape'))


"""
    decode
    bytes 转换为 str
"""
s = '中文测试abc123'
utf8_bytes = s.encode('utf-8')
print(b'bytes :', utf8_bytes)

# strict 默认也是，抛出错误  UnicodeDecodeError
# print(utf8_bytes.decode('gbk'))

# ignore， 忽略不能转换的 字节
# print('ignore 处理：', utf8_bytes.decode('gbk', 'ignore'))
# print(b'\xe4\xb8'.decode('gbk'))
# print(b'\x95a'.decode('gbk'))

# replace， 使用 � 替换 错误的字节
print('replace 处理：', utf8_bytes.decode('gbk', 'replace'))
