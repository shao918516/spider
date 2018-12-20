## 一、requests介绍
基于urllib3的一个爬虫库，目前最完善，简单，稳定，好用的库

## 二、requests用法
### 1、get、head、options、delete等
>
	r = requests.get('http://httpbin.org/') # head, option等
	print(r.text)

	payload = {'key1': 'value1', 'key2': 'value2'}
	r = requests.get("http://httpbin.org/get", params=payload)
	print(r.text）

	payload = {'key1': 'value1', 'key2': ['value2', 'value3']}
	r = requests.get('http://httpbin.org/get', params=payload)
	print(r.text)

### 2、post
>
	headers = {
	    'User-Agent': r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
	                  r'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
	    'Referer': r'http://httpbin.org',
	    'Connection': 'keep-alive'
	}
	data = {
		    'key1': 'value1',
		    'key2': 'value2'
		}
	url = 'http://httpbin.org/post'
	r = requests.post(url, data=data, headers=headers)
	print(r.text)

	print(r.json())

	#支持json
	import json
	r = requests.post(url, data=json.dumps(data), headers=headers) 
	# 字符串转json： json.loads(string)
	# dump和load 都是操作文件

### 3、编码
r.content 返回的是bytes，需要自己根据需求进行编码转换
r.text 是根据判断的编码转换后的str
判断方法如下：
>requests.adapters模块下 HTTPAdapter 类中的 build_response 方法：
response.encoding = get_encoding_from_headers(response.headers)
跳转到requests.utils模块的 get_encoding_from_headers 方法:
content_type = headers.get('content-type') # 值为：text/html
	if 'text' in content_type:
		return 'ISO-8859-1'
所以结论是这个 ISO-8859-1 的意义就是r.text的默认编码
如果response.encoding为None，就使用 chardet.detect(self.content)['encoding'] 判断出编码，一般是 utf-8

	r = requests.get('http://www.baidu.com')
	print(r.encoding)
	
	content = r.content
	print(content)
	print(content.decode('utf-8'))
	
	print(r.text)
	text = r.text
	print(text.encode('raw_unicode_escape').decode('utf-8'))
	print(text.encode('iso-8859-1').decode('utf-8'))
	print(text.encode(r.encoding).decode('utf-8')) # 有可能为None，这样不保险
	

编码解码 参数errors：
>
- 默认的参数就是strict，代表遇到非法字符时抛出异常； 
- 如果设置为ignore，则会忽略非法字符； 
- 如果设置为replace，则会用?取代非法字符； 
- 如果设置为xmlcharrefreplace，则使用XML的字符引用。
	s = '我是测试中文abc123'
	print(s.encode('ascii', 'ignore'))
	print(s.encode('ascii', 'replace'))
	print(s.encode('ascii', 'xmlcharrefreplace'))
	
	s = '我是测试中文abc123'
	s_ascii = s.encode('ascii', 'xmlcharrefreplace')
	print(s_ascii.decode('ascii'))
	from common.util import xmlchar_2_cn
	print(xmlchar_2_cn(s_ascii.decode('ascii')))

### 4、响应状态码
	r = requests.get('http://httpbin.org/') # head, option等
	if r.status_code == requests.codes.ok:
	if r.status_code == 200:
		print('成功')
	else:
		print('失败')

### 5、 cookie
>- path区分大小写，应与浏览器中的地址栏的输入一致
>- path不可读，只可写
>- path不可更改，试图更改，其实是新写另一个cookie
>- path和domain都有继承性，子目录可以读父目录的cookie，二级域名也能读取一级域名的cookie
	jar = RequestsCookieJar()
	jar.set('tasty_cookie', 'yum', domain='httpbin.org', path='/cookies')
	jar.set('gross_cookie', 'blech', domain='httpbin.org', path='/elsewhere')
	jar.set('root_cookie', 'root', path='/')
	jar.set('default_cookie', 'default')
	url = 'http://httpbin.org/cookies'
	r = requests.get(url, cookies=jar)
	print(r.text)
	
### 6、重定向
	r = requests.get('http://github.com', allow_redirects=False)
	print(r.status_code)

### 7、超时
	r = requests.get('http://httpbin.org/', timeout=0.001)
	print(r.status_code)

### 8、代理
	proxies = {'http': '127.0.0.1:8888'}
	r = requests.get('http://httpbin.org/', proxies=proxies)
	print(r.status_code)

### 9、https
> 出现SSLError("bad handshake: Error([('SSL routines', 'tls_process_server_certificate', 'certificate verify failed')],)",)错误
	r = requests.get('https://www.alipay.com', verify=False)
	print(r.status_code)

### 10、一般更多使用session，不直接使用request.get()
	s = requests.session()
	r = s.get('http://httpbin.org/')
	print(r.status_code)

### 11、多线程
	'''
	    多线程
	'''
	import threading
	from time import ctime
	
	def request_httpbin(num=0, url='http://httpbin.org/'):
	    print('第 %s 次请求 开始， %s' % (num, ctime()))
	    r = requests.get('http://httpbin.org/')
	    print('第 %s 次请求 结束， %s' % (num, ctime()))
	
	if __name__ == '__main__':
	    threads = []
	    for i in range(1, 101):
	        t = threading.Thread(target=request_httpbin, args=(i,))
	        threads.append(t)
	
	    for t in threads:
	        t.start()
	
	    for t in threads:
	        t.join()

### 12、使用gevent实现并发
	'''
	使用gevent实现并发
	'''
	import requests
	import gevent
	import urllib3
	urllib3.disable_warnings()
	import time
	from gevent import monkey
	monkey.patch_all()
	
	urls = [
	    'https://docs.python.org/2.7/library/index.html',
	    'https://docs.python.org/2.7/library/dl.html',
	    'http://www.iciba.com/partial',
	    'http://2489843.blog.51cto.com/2479843/1407808',
	    'http://blog.csdn.net/woshiaotian/article/details/61027814',
	    'https://docs.python.org/2.7/library/unix.html',
	    'http://2489843.blog.51cto.com/2479843/1386820',
	    'http://www.bazhuayu.com/tutorial/extract_loop_url.aspx?t=0',
	]
	
	def method1():
	    t1 = time.time()
	    for url in urls:
	        res = requests.get(url, verify=False)
	
	    t2 = time.time()
	    print('method1', t2 - t1)
	
	def method2():
	    jobs = [gevent.spawn(requests.get, url, verify=False) for url in urls]
	    t1 = time.time()
	    gevent.joinall(jobs)
	    t2 = time.time()
	    print('method2', t2 - t1)
	
	if __name__ == '__main__':
	    method1()
	    method2()

## 三、grequests库用法
> 是一个基于request和gevent的库

	import time
	import requests
	import grequests
	import urllib3
	urllib3.disable_warnings()
	
	urls = [
	    'https://docs.python.org/2.7/library/index.html',
	    'https://docs.python.org/2.7/library/dl.html',
	    'http://www.iciba.com/partial',
	    'http://2489843.blog.51cto.com/2479843/1407808',
	    'http://blog.csdn.net/woshiaotian/article/details/61027814',
	    'https://docs.python.org/2.7/library/unix.html',
	    'http://2489843.blog.51cto.com/2479843/1386820',
	    'http://www.bazhuayu.com/tutorial/extract_loop_url.aspx?t=0',
	]
	
	def method1():
	    t1 = time.time()
	    for url in urls:
	        res = requests.get(url, verify=False)
	
	    t2 = time.time()
	    print('method1', t2 - t1)
	
	def method2():
	    tasks = [grequests.get(u) for u in urls]
	    t1 = time.time()
	    res = grequests.map(tasks, size=3)
	    t2 = time.time()
	    print('method2', t2 - t1)
	
	def method3():
	    tasks = [grequests.get(u) for u in urls]
	    t1 = time.time()
	    res = grequests.map(tasks, size=8)
	    t2 = time.time()
	    print('method3', t2 - t1)
	
	def method4():
	    tasks = [grequests.get(u, callback=response_handle) for u in urls]
	    t1 = time.time()
	    res = grequests.map(tasks, size=8)
	    t2 = time.time()
	    print('method3', t2 - t1)
	
	def response_handle(r, *args, **kwargs):
	    print(r.url)
	
	if __name__ == '__main__':
	    method1()
	    method2()
	    method3()
	    method4()