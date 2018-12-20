## 一、介绍
python用于解析文本得库，支持第三方的解析器，譬如lxml、html5lib

## 二、用法
### 1、初始化
	soup = BeautifulSoup(html_doc, features)
>features有11种：fast, html, html.parser, html5, html5lib, lxml, lxml-html, lxml-xml, permissive, strict, xml
>

- bs4.builder._lxml.LXMLTreeBuilderForXML：xml、lxml-xml、      也支持fast、xml、permissive
- bs4.builder._lxml.LXMLTreeBuilder：默认、lxml、fast、html、lxml-html、permissive  # 使用最多的对象
- bs4.builder._html5lib.HTML5TreeBuilder：html5、html5lib，      也支持html、permissive
- bs4.builder._htmlparser.HTMLParserTreeBuilder：strict、html.parser，       也支持html

- TreeBuilder，4个类继承
- HTMLTreeBuilder, 继承TreeBuilder，并由LXMLTreeBuilder、HTML5TreeBuilder和HTMLParserTreeBuilder继承
- bs4.builder._htmlparser.BeautifulSoupHTMLParser ，继承系统的html.parser.HTMLParser，HTMLParserTreeBuilder 最终也是使用的这个类进行解析

>差异性：
>
- 如果被解析的HTML文档是标准格式,那么解析器之间没有任何差别
- 文档不规范时，会各自不同的处理

	from bs4 import BeautifulSoup
	text = '<a><b /></a>'
	soup_test = BeautifulSoup(text, 'lxml') # 会补全 html，body和p
	print('lxml:')
	print(soup_test)
	soup_test = BeautifulSoup(text, 'html.parser') # 会补全 p
	print('html.parser:')
	print(soup_test)
	soup_test = BeautifulSoup(text, 'html5')  # 会补全 html，head，body和p
	print('html5:')
	print(soup_test)
	soup_test = BeautifulSoup(text, 'xml')  # 会加xml头，忽略错误的标签
	print('xml:')
	print(soup_test) 

### 2、详细用法

	'''
	soup = BeautifulSoup(html_doc, 'html')
	#features: fast, html, html.parser, html5, html5lib, lxml, lxml-html, lxml-xml, permissive, strict, xml
	fast:一般不推荐使用，不同的系统选择不同的方式
	'''
	# soup = BeautifulSoup(html_doc, ['lxml', 'html5'])
	# soup = BeautifulSoup(html_doc, ['html', 'html5'])
	# soup = BeautifulSoup(html_doc, 'lxml')
	
	'''不同builder的差异'''
	# text = '<a><b /></a>'
	# soup_test = BeautifulSoup(text, 'lxml') # 会补全 html，body和p
	# print('lxml:')
	# print(soup_test)
	# soup_test = BeautifulSoup(text, 'html.parser') # 会补全 p
	# print('html.parser:')
	# print(soup_test)
	# soup_test = BeautifulSoup(text, 'html5')  # 会补全 html，head，body和p
	# print('html5:')
	# print(soup_test)
	# soup_test = BeautifulSoup(text, 'xml')  # 会加xml头，忽略错误的标签
	# print('xml:')
	# print(soup_test)
	
	
	# print(soup.prettify())  # 直接输出文档，str类型，默认utf-8
	# print(soup.prettify('gbk')) # 传入编码，输出 bytes
	# print(soup.prettify('gbk').decode('gbk')) # 传入编码，输出 bytes
	
	# print(soup.title) # 标签，包括标签本身
	# print(soup.title.name) # 标签的名字
	# s = soup.title.string
	# print(soup.title.string) # 标签的内容, NavigableString 对象
	# print(soup.title.text) # 标签的内容， str 对象
	
	# print(soup.meta) # 标签
	# print(soup.meta['charset']) # 标签属性
	
	# print(soup.meta.parent.name) # 标签的父标签
	# print(soup.html.parent.name)
	# print(soup.html.parent.parent)
	
	# text = '''
	# <a><b>text1</b><c>text2</c>
	# <d>text3</d><e e1='100'/><f f1='101'/><></a>
	# '''
	# sibling_soup = BeautifulSoup(text, 'lxml')
	# print(sibling_soup.b.next_sibling) #  兄弟节点
	# print(sibling_soup.c.previous_sibling) #  兄弟节点
	# print(sibling_soup.c.next_sibling) #  兄弟节点，是 换行符
	# print(sibling_soup.d.previous_sibling) #  兄弟节点，是 换行符
	
	# print(sibling_soup.a.next_element) #  下一个元素，是 <b>text1</b>
	# print(sibling_soup.b.next_element) #  下一个元素，是 text1
	# print(sibling_soup.b.next_element.next_element) #  下一个元素，是 换行符
	# print(sibling_soup.d.previous_element) #  上一个元素，是 换行符
	# print(sibling_soup.f.previous_element) #  上一个元素，是 <e e1='100'/>
	# print('结束')
	
	# print(soup.find_all('meta')) # 查找所有
	# print(soup.find_all('meta', limit=2)) # 查找所有
	# print(soup.find('meta', {'name': 'renderer'})) # 查找特定的一个标签，其实也是调用的find_all，不过会在取到一个值后返回
	# print(soup.find(id="seajsnode")) # 根据id查找特定的一个标签
	
	# print(soup.find(text='支付宝 知托付！')) # 根据标签内容查找特定的一个标签，不能仅仅有标签内容一个参数
	# print(soup.find(text='支付宝 知托付！', test='test')) # 根据标签内容查找特定的一个标签，不能仅仅有标签内容一个参数
	# print(soup.find('title', text='支付宝 知托付！')) # 根据标签内容查找特定的一个标签，不能仅仅有标签内容一个参数
	
	# meta = soup.find('meta', {'name': 'renderer'})
	# print(meta)
	# print(meta.find_next_sibling('meta')) # 查找下个符合条件的兄弟节点
	# print(meta.find_next_siblings('meta')) # 查找所有符合条件的兄弟节点
	#
	# print(meta.find_next_sibling('a')) # 查找下个符合条件的兄弟节点
	# print(meta.find_next('a')) # 查找下个符合条件的节点
	# print(meta.find_all_next('a')) # 查找所有符合条件的节点
	
	# print(soup.find('body').get_text()) # 获取所有文本
	# print(soup.find('body').get_text('|')) # 获取所有文本，| 是分隔符
	
	'''
	    标签对象一样可以使用所有方法
	'''
	# body = soup.find('body')
	# print(body.find('div'))
	
	'''
	    标签对象，可以和字符串一样编码和解码
	'''
	# markup = "<b>\N{SNOWMAN}</b>"
	# snowman_soup = BeautifulSoup(markup, 'html.parser')
	# tag = snowman_soup.b
	# print(tag)
	# print(tag.encode("utf-8"))
	# print(tag.encode("utf-8").decode('utf-8'))
	# print(tag.encode("iso-8859-1"))
	# print(tag.encode("iso-8859-1").decode('iso-8859-1'))
	# print(tag.encode("gbk"))
	# print(tag.encode("gbk").decode('gbk'))
	
	'''
	    css选择器
	'''
	# print(soup.select("title")) # 标签名
	# print(soup.select("html head title")) # 逐层查找
	# print(soup.select("body a")) # 不逐层查找
	
	# print(soup.select("body > a")) # >  子节点
	# print(len(soup.select("body > div"))) # >  子节点
	# print(soup.select("body > div")) # >  子节点
	
	# print(soup.select("input ~ p")) # >  兄弟节点
	
	# print(soup.select("#test_id"))  # 通过id
	# print(soup.select("input#test_id"))  # 通过id
	
	# print(soup.select('.test_class')) # 通过class
	
	# print(soup.select('meta[charset="gb2312"]'))

### 3、注意事项：
>
- bs4会自动替换 html_doc 中的 <meta charset="gb2312" /\> 为 <meta charset="utf-8" /\>，这是html5的写法，html4之前是：<meta http-equiv="content-type" content="text/html; charset=gb2312">
- 标签未结束的，会自动补全，例如：<meta charset="gb2312" \> 会补全为 <meta charset="gb2312" /\>

## 三、beautifulsoup4 和其他方法的差异
- beautifulsoup4 支持CSS选择器、Python标准库中的HTML解析器，也支持 lxml 的 XML解析器(css选择器，但是不支持xpath)，但是基于 DOM 的，会解析整个DOM树 ，全文档查询，
- lxml使用xpath，则只会局部遍历
- 正则表达式，速度最快，但是最复杂，获取js中当中的数据一般使用正则