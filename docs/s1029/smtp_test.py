#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Terry'

from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

import smtplib

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

# 发件人
from_addr = 'auratest2018@163.com'
# 密码
password = 'auratest2016'
# 收件人
to_addr = 'auratest2018@163.com'
# 发件人的smtp服务器地址
smtp_server = 'smtp.163.com'

# 构建一个文本的mail对象
# 内容主体
msg = MIMEText('hello, send by Python... we are 1808', 'plain', 'utf-8')
# 发件人
msg['From'] = _format_addr('Python爱好者 <%s>' % from_addr)
# 收件人
msg['To'] = _format_addr('管理员 <%s>' % to_addr)
# 标题
msg['Subject'] = Header('来自SMTP的问候……', 'utf-8').encode()

# 构建一个 smtp 对象
server = smtplib.SMTP(smtp_server, 25)
# 设置一个调试级别
server.set_debuglevel(1)
# 登录
server.login(from_addr, password)
# 发送邮件
server.sendmail(from_addr, [to_addr], msg.as_string())
server.quit()
