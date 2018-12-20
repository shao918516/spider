## 一、http网络库需要什么功能
- 正确发出http、https请求
- 不同的method，如get、post、options等
- 设置headers
- 处理cookie
- 设置代理
- 能正确处理response

## 二、http协议通讯包
> python自带的http包
> client、server、cookiejar、cookies
> 几乎所有的http库都使用的这个client进行数据发送，除了aiohttp

## 三、urllib
> 五个模块：request, error, parse, response, robotparser
> 最终使用python自带的http模块发送数据包给服务器

http库，我们只使用3个函数： quote、unquote 和 urlencode


### 1、request
1、urllib.request.urlopen

	from urllib import request
	start = time.time()
	response = request.urlopen(r'http://www.baidu.com/')
	html = response.read()
	text = html.decode('utf-8')
	print('共用： %s 秒' % (time.time() - start))

	/#response 有 read(),readline(),readlines(),fileno(),close(),info(),getcode(),geturl()

2、使用Request
> urllib.request.Request(url, data=None, headers={}, method=None)

	start = time.time()
	url = r'http://www.baidu.com/'
	headers = {
	    'User-Agent': r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
	    'Referer': r'http://www.baidu.com/',
	    'Connection': 'keep-alive'
	}
	req = request.Request(url, headers=headers)
	page = request.urlopen(req).read()
	page = page.decode('utf-8')
	print(page)
	print('共用： %s 秒' % (time.time() - start))

3、Post提交
> urllib库，默认是get方式提交，urlopen的data参数默认为None，当data参数不为空的时候，urlopen提交方式为POST（request的get_method）,
> 如果要使用其他方式必须Request(method='get')或req.get_method = lambda : 'options'。

	from urllib import request, parse
	url = r'http://www.lagou.com/jobs/positionAjax.json?'
	headers = {
	    'User-Agent': r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
	                  r'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
	    'Referer': r'http://www.lagou.com/zhaopin/Python/?labelWords=label',
	    'Connection': 'keep-alive'
	}
	data = {
	    'first': 'true',
	    'pn': 1,
	    'kd': 'Python'
	}
	data = parse.urlencode(data).encode('utf-8')
	req = request.Request(url, headers=headers, data=data)
	page = request.urlopen(req).read()
	page = page.decode('utf-8')

4、代理
> 默认会通过getproxies中的getproxies_environment和getproxies_registry调用系统代理设置
> requests库也是调用的这个getproxies方法获取系统代理设置
> urllib.request.ProxyHandler
>
	from urllib import request, parse
	url = r'http://www.lagou.com/jobs/positionAjax.json?'
	headers = {
	    'User-Agent': r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
	                  r'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
	    'Referer': r'http://www.lagou.com/zhaopin/Python/?labelWords=label',
	    'Connection': 'keep-alive'
	}
	data = {
	    'first': 'true',
	    'pn': 1,
	    'kd': 'Python'
	}
	proxy = request.ProxyHandler({'http': '127.0.0.1:8888'})  # 设置proxy
	opener = request.build_opener(proxy)  # 挂载opener
	request.install_opener(opener)  # 安装opener
	data = parse.urlencode(data).encode('utf-8')
	page = opener.open(url, data).read()
	page = page.decode('utf-8')
	print(page)

5、操作cookies
> 通过http.cookiejar

	import urllib.request
	import http.cookiejar
	
	URL_ROOT = r'http://d.weibo.com/'
	
	cookie = http.cookiejar.CookieJar()  # 声明一个CookieJar对象实例来保存cookie
	handler = urllib.request.HTTPCookieProcessor(cookie)  # 利用HTTPCookieProcessor对象来创建cookie处理器
	opener = urllib.request.build_opener(handler)  # 通过handler来构建opener
	
	response = opener.open(URL_ROOT)
	
	for item in cookie:
	    print('Name = ' + item.name)
	    print('Value = ' + item.value)

### 2、response
> 返回的值是HTTPResponse，response主要有read(),readline(),readlines(),fileno(),close(),info(),getcode(),geturl()

### 3、error
> error模块比较简单，就3个类型URLError、HTTPError和ContentTooShortError
>
	try:
        page = request.urlopen(req, data=data).read()
        page = page.decode('utf-8')
    except error.HTTPError as e:
        print(e.code())
        print(e.read().decode('utf-8'))

### 4、parse
> urllib.parse.urlencode、urllib.parse.unquote和urllib.parse.quote

### 5、robotparser
> 针对网站的robots.txt

## 四、 urllib3
- 第三方库，最终也是使用python自带的http模块发送数据包给服务器
- requests使用了urllib3
- pip也使用了urllib3
- 多次请求中可重复利用同一socket连接,应用了keep-alive特性，减少TCP握手次数和慢启动次数
- 支持File传输
- 内置重定向和重试
- 支持gzip和deflate解码
- 线程安全
- 支持代理


	http_pool = urllib3.connection_from_url("http://example.com")

### 1、PoolManager
	import urllib3
	http = urllib3.PoolManager()
	r = http.request('GET', 'http://httpbin.org/robots.txt')
	print(r.status)
	print(r.data)

### 2、HTTPConnectionPool
> 
	import urllib3
	http_pool = urllib3.HTTPConnectionPool('httpbin.org')
	r = http_pool.urlopen('GET', '/robots.txt')
	print(r.status)
	print(r.data)
	#不允许访问host之外的url

### 3、代理
>
	import urllib3
	proxy = urllib3.ProxyManager('http://127.0.0.1:8888', headers={'connection': 'keep-alive'})
	r = proxy.request('GET', 'http://httpbin.org/robots.txt')
	print(r.status)
	print(r.data)

### 4、操作cookie
> 没有找到相关的操作，只能通过headers设置的方式实现
	import urllib3
	proxy = urllib3.ProxyManager('http://127.0.0.1:8888', headers={'connection': 'keep-alive', 'Cookie': '内容'})
	r = proxy.request('GET', 'http://httpbin.org/robots.txt')
	print(r.status)
	print(r.data)