## 一、介绍
> pyquery是一个第三方解析文本的库，解析器基于lxml，url访问基于requests，是一个符合jquery的语法进行操作得库

## 二、具体用法

	html_doc = '''
	 <html>
	  <head>
	   <title>
	    The Dormouse's story
	   </title>
	  </head>
	  <body>
	   <p class="title">
	    <b>
	     The Dormouse's story
	    </b>
	   </p>
	   <p class="story">
	    Once upon a time there were three little sisters; and their names were
	    <a class="sister" href="http://example.com/elsie" id="link1">
	     Elsie
	    </a>
	    <a class="sister" href="http://example.com/lacie" id="link2">
	     Lacie
	    </a>
	    and
	    <a class="sister" href="http://example.com/tillie" id="link2">
	     Tillie
	    </a>
	    and they lived at the bottom of a well.
	   </p>
	   <p class="story">
	    测试中文
	   </p>
	  </body>
	 </html>
	'''
	
	pyq_str=pq(html_doc)
	print(pyq_str('head').html()) #返回<title>hello</title>
	print(pyq_str('head').text())
	
	pyq_str=pq(etree.fromstring(html_doc))
	print(pyq_str('head').html()) #返回<title>hello</title>
	print(pyq_str('head').text())
	
	pyq_file=pq(filename='html_doc.txt') # 默认cp936 编码，即gbk编码，无法更改
	print(pyq_file('head').html()) #返回<title>hello</title>
	print(pyq_file('head').text())
	
	# 默认使用的requests的方法访问网络，也可以自己传入一个opener
	pyq_url=pq(url='http://www.baidu.com', encoding='utf-8')
	pyq_url=pq(url='http://www.baidu.com')
	print(pyq_url('head').html()) #返回<title>hello</title>
	print(pyq_url('head').text())
	
	pyq_str=pq(html_doc)
	link1 = pyq_str('#link1')
	print(link1.html())  # 标签内的所有东西
	print(link1.text())  # 标签内的文本
	
	print(pyq_str('body').html())
	print(pyq_str('body').text())
	
	print(pyq_str('a[@id="link1"]').html())  # css选择器，通过属性定位标签
	
	# 获取标签的属性值，通过 元素.attr.属性名  或 元素.attr['属性名']
	print(pyq_str('a[@id="link1"]').attr.id)
	print(pyq_str('a[@id="link1"]').attr['id'])
	
	print(pyq_str('a[@id="link1"]').parent()) # 父标签
	
	# 子标签  ， 漏掉第一行的文本
	print(pyq_str('p[@class="story"]').children())
	
	# 下一个平级的标签
	print(pyq_str('p[@class="title"]').next())
	
	# 之后平级的所有标签
	print(pyq_str('p[@class="title"]').next_all())


## 三、各个解析方法总结
- 1、正则：最快，最复杂
- 2、xpath：第二快，第二复杂
- 3、beautifulsoup4：第三快，最简单
- 4、pyquery：基于lxml的html，目前不完善，不建议使用，除非特别喜欢jquery语法


