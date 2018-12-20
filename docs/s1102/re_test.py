#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Terry'


import re


text = '''
<!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
</head>
<body>
<script type="text/javascript">


	var href = decodeURIComponent("https:\/\/www.baidu.com\/cache\/user\/html\/v3Jump.html")+"?"

var accounts = '&accounts='

href += "err_no=123&callback=parent.bd__pcbs__fh3y76&codeString=&userName=mumuloveshine&phoneNumber=&mail=&hao123Param=RUZwZEVGSFJtcGxla1pUWldKamVFVklSVmxKTXpJdFlUQkpNaTFRV1dsLVVUSTBPRkZRYTBGYVozcFRUazVoUVZGQlFVRkJKQ1FBQUFBQUFBQUFBQUVBQUFCNFR5bk9iWFZ0ZFd4dmRtVnphR2x1WlFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBRE83cTFvenU2dGFi&u=https://www.baidu.com/&tpl=mn&secstate=&gotourl=&authtoken=&loginproxy=&resetpwd=&vcodetype=&lstr=&ltoken=&bckv=1&bcsync=1Mzv%2FGVc4pmKuDQdpf2p9b38qlqhPbzE7cTts1MoRxsBaAjhZuUWw84%2BTa35iajVEi11HZ6HH6xFwiVUYfUR2RNIl2DLq4Yj%2FfNUz9%2BTVVTShaygIgI4VeVcQcD8yy6Wklcihcc9g6LaVWjB6DMuvvvKLs54P5nolxeu8ZpfHsYwDxCcHgg8YGO%2FNgUltA8bZ4dsppFDUc6FspJ%2FmG9QYlkcN6oG0Sl5bs36ynODwL45Qd1mwmzIHN09USnjxdWSEK2nctHal1vKF7fTm%2FbG1xsd3pefvc0SbDS%2B4tuwQOWEcJQMXuXRAhgVzc4Iw597lAuWEjnqSGZJMFGPi%2BplAQ%3D%3D&bcchecksum=2848738951&code=&bdToken=&realnameswitch=&setpwdswitch=&bctime=1521204019&bdstoken=&authsid=&jumpset=&appealurl=&realnameverifyemail=0&traceid=&realnameauthsid="+accounts;


if(window.location){
    window.location.replace(href);
}else{
   document.location.replace(href); 
}
</script>
</body>
</html>
end&
'''


# err_no = re.findall(r'err_no=([0-9]+)&', text)[0]
# print(err_no)


# err_no = re.search(r'err_no=([0-9]+)&', text).group(1)
# print(err_no)

# err_no = re.search(r'err_no=(.*)&', text).group(1)
# print('没有添加s flag：', err_no)
#
#
# err_no = re.search(r'err_no=(.*)&', text, re.RegexFlag.S).group(1)
# print('添加了s flag：', err_no)
#
#
# err_no = re.search(r'err_no=(.*?)&', text, re.RegexFlag.S).group(1)
# print('添加了s flag，并且添加了 ? ：', err_no)


# 使用最多的写法：
err_no = re.search(r'err_no=(.*?)&', text).group(1)
print('最常用的写法：', err_no)

# 取编码
charset = re.search(r'content="text/html; charset=(.*?)"', text).group(1)
print('最常用的写法：', charset)



