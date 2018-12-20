#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

__author__ = 'Terry'

text = '''


<!-- FD:homeproxy-home:homeproxy/home/startup.vm:START --><!-- FD:homeproxy-home:homeproxy/home/startup.vm:startup.schema:START --><!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="baidu-site-verification" content="OyUb4RVdSe" />
    <meta name="renderer" content="webkit" />
  
    <title>支付宝 知托付！</title>
    <meta name="keywords" content="支付宝,电子支付/网上支付/安全支付/手机支付,安全购物/网络购物付款/付款/收款,水电煤缴费/信用卡还款/AA收款,支付宝网站">
    <meta name="description" content="支付宝，全球领先的独立第三方支付平台，致力于为广大用户提供安全快速的电子支付/网上支付/安全支付/手机支付体验，及转账收款/水电煤缴费/信用卡还款/AA收款等生活服务应用。">
 	<link rel="icon" href="https://i.alipayobjects.com/common/favicon/favicon.ico" type="image/x-icon">
    <link rel="alternate" media="only screen and(max-width: 640px)" href="https://ds.alipay.com/" />
    <!--[if lte IE 7]>
    <script type="text/javascript">
        window.location.href = 'https://www.alipay.com/x/kill-ie.htm';
    </script>
    <![endif]-->
  
    <style>
        * {
            margin: 0;
            padding: 0;
        }

        table {
            border-collapse: collapse;
            border-spacing: 0;
        }

        h1, h2, h3, h4, h5, h6 {
            font-size: 100%;
        }

        ul, ol, li {
            list-style: none;
        }

        em, i {
            font-style: normal;
        }

        img {
            border: none;
        }

        input, img {
            vertical-align: middle;
        }

        body {
            background: #fff;
            color: #666;
            font-size: 14px;
            font-family: arial;
        }

        a {
            color: #666666;
            text-decoration: none;
        }

        html, body {
            background: #f9f9f9;
            width: 100%;
            height: 100%;
            font-family: Helvetica, sans-serif;
            -webkit-text-size-adjust: none;
        }

        * {
            -webkit-tap-highlight-color: rgba(0, 0, 0, 0);
        }

        textarea.fixAndroidKeyboard:focus, input.fixAKeyboard:focus {
            -webkit-tap-highlight-color: rgba(255, 255, 255, 0);
            -webkit-user-modify: read-write-plaintext-only;
        }

        .noscroll {
            position: absolute;
            width: 100%;
            height: 100%;
            overflow: hidden;
        }

        .app-dom {
            width: 100%;
        }

        .clearfix:after {
            display: block;
            content: '';
            clear: both;
            visibility: hidden;
        }
    </style>

    

    <style>
        /*@font-face {*/
        /*font-family: 'iconfont';*/
        /*src: url('//at.alicdn.com/t/font_1436009778_9049127.eot'); /!* IE9*!/*/
        /*src: url('//at.alicdn.com/t/font_1436009778_9049127.eot?#iefix') format('embedded-opentype'), /!* IE6-IE8 *!/ url('//at.alicdn.com/t/font_1436009778_9049127.woff') format('woff'), /!* chrome、firefox *!/ url('//at.alicdn.com/t/font_1436009778_9049127.ttf') format('truetype'), /!* chrome、firefox、opera、Safari, Android, iOS 4.2+*!/ url('//at.alicdn.com/t/font_1436009778_9049127.svg#iconfont') format('svg'); /!* iOS 4.1- *!/*/
        /*}*/

        /*.iconfont {*/
        /*font-family: "iconfont" !important;*/
        /*font-size: 32px;*/
        /*font-style: normal;*/
        /*-webkit-font-smoothing: antialiased;*/
        /*-webkit-text-stroke-width: 0.2px;*/
        /*-moz-osx-font-smoothing: grayscale;*/
        /*}*/

        body {
            font: 12px/1.5 "Microsoft YaHei", tahoma, arial, Hiragino Sans GB, \5b8b\4f53;
            overflow: hidden;
            position: relative;
            height: 100%;
            width: 100%;
        }

        a {
            text-decoration: none;
        }

        .header {
            position: fixed;
            width: 100%;
            top: 20px;
            left: 0px;
            z-index: 999;
        }

        .nav {
            width: 80%;
            height: 30px;
            line-height: 30px;
            margin: 0 auto;
        }


        .logo {
            float: left;
            background-image: url(https://img.alicdn.com/tps/TB17ghmIFXXXXXAXFXXXXXXXXXX.png);
            display: block;
            width: 70px;
            height: 25px;
            background-position: 0 0;
            background-repeat: no-repeat;
            background-size: 70px;
        }

        .entry {
            float: right;
            color: #fff;
        }

        .entry .state {
            color: #bfbfbf;
        }

        .entry a {
            font-size: 12px;
            color: #fff;
            margin: 0 5px;
        }

        .entry a:hover {
            color: #00bbee;
        }

        .container {
            width: 100%;
            height: 100%;
            background-color: #fff;
        }

        .content {
            width: 1200px;
            height: 100%;
            margin: 0 auto;;
        }

        .wrap {
            position: absolute;
            left: 0;
            top: 20%;
            width: 100%;
            text-align: center;
            z-index: 2;
        }

        .slogan {
            width: 600px;
            height: 200px;
            background: url(https://img.alicdn.com/tps/TB1POhqIFXXXXXbXFXXXXXXXXXX.png) no-repeat 0 0;
            display: inline-block;
            background-size: 600px;
        }

        .mid {
            width: 100%;
        }

        .main-entry {
            width: 550px;
            height: 50px;
            margin: 15px auto 0;
        }

        .main-entry a {
            display: block;
            text-decoration: none;
            float: left;
            text-align: center;
            cursor: pointer;
            border-radius: 8px;
            font-size: 14px;
            letter-spacing: 1px;
            height: 50px;
            width: 170px;
            color: #ffffff;
            line-height: 50px;
            position: relative;
            overflow: hidden;
        }

        .main-entry a .title {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 2;
            padding-left: 18px;
        }

        .main-entry a .title i {
            position: absolute;
            left: 20px;
            top: 14px;
            background: url(https://img.alicdn.com/tps/TB1uh30IpXXXXXKXVXXXXXXXXXX.png) no-repeat 0 0;
            display: block;
            width: 24px;
            height: 24px;
            background-size: 24px;
        }

        .main-entry a .title .seller {
            background-image: url(https://img.alicdn.com/tps/TB12JNkIFXXXXXBXXXXXXXXXXXX.png);
        }

        .main-entry a .title .developer {
            background-image: url(https://zos.alipayobjects.com/rmsportal/neqhNGwxBXBmhVY.png);
        }

        .main-entry s {
            background-color: #00a3ee;
            opacity: .9;
            display: block;
            border-radius: 8px;
            height: 100%;
            width: 100%;
            position: absolute;
            top: 0;
        }

        .main-entry a:hover s {
            background-color: #00aaee;
            opacity: 1;
        }

        a.personal-login,
        a.seller-login
        {
            margin-left: 20px;
            transition: all .3s ease-in-out;
            -webkit-transition: all .3s ease-in-out;
            -moz-transition: all .3s ease-in-out;
            -o-transition: all .3s ease-in-out;
        }
        a.seller-login .seller-entry {
            display: none;
            z-index: 2;
            position: relative;
            height: 50px;
        }
        a.seller-login .inerval-line {
            display: none;
            width: 150px;
            margin: 0 auto;
            border-bottom: 1px solid rgba(255, 255, 255, 0.2);
            position: relative;
            height: 0;
            z-index: 2;
        }
        a.seller-login:hover{
            height: 100px;
            margin-top: -25px;
        }
        a.seller-login:hover .title{
            display: none;
        }
        a.seller-login:hover .seller-entry,
        a.seller-login:hover .inerval-line
        {
            display: block;
        }

        .alipay-app {
            text-align: center;
            position: absolute;
            bottom: 70px;
            left: 0;
            z-index: 3;
            width: 100%;
        }

        .alipay-app .ma {
            width: 600px;
            margin: 0 auto;
        }

        .alipay-app img {
            width: 60px;
            height: 60px;
        }

        .alipay-app p {
            line-height: 30px;
            height: 30px;
            color: #ffffff;
            margin: 5px 0 10px;
        }

        .footer {
            position: absolute;
            bottom: 0px;
            left: 0px;
            width: 100%;
            height: 65px;
            background-color: white;
            z-index: 99;
        }

        .nav-links {
            width: 99%;
            height: 20px;
            margin: 0 auto;
            text-align: center;
            overflow: hidden;
        }

        .footer ul {
            padding-left: 5px;
        }

        .footer li {
            display: inline-block;
            margin: 2px;
        }

        .footer li a {
            color: #666;
        }

        .ownership {
            text-align: center;
            height: 20px;
            line-height: 25px;
        }

        .nav-icons {
            width: 250px;
            height: 30px;
            margin: 0 auto;
            text-align: center;
        }

        .nav-icons a {
            width: 20px;
            display: block;
            float: left;
            margin-right: 5px;
            height: 28px;
            background: url(https://img.alicdn.com/tps/TB1.cMTIpXXXXbLXVXXXXXXXXXX.png) no-repeat 0 0;
        }

        a.pic1 {
            background-position: 0px -5px;
            width: 18px;
        }

        a.pic1:hover {
            background-position: 1px -28px;
            width: 18px;
        }

        a.pic2 {
            background-position: -33px -5px;
            width: 40px;
        }

        a.pic2:hover {
            background-position: -32px -28px;
            width: 40px;
        }

        a.pic3 {
            background-position: -74px -5px;
            width: 33px;
        }

        a.pic3:hover {
            background-position: -73px -28px;
            width: 33px;
        }

        a.pic4 {
            background-position: -115px -5px;
            width: 18px;
        }

        a.pic4:hover {
            background-position: -114px -28px;
            width: 18px;
        }

        a.pic5 {
            background-position: -135px -5px;
            width: 31px;
        }

        a.pic5:hover {
            background-position: -134px -28px;
            width: 31px;
        }


        a.pic7 {
            background-position: -200px -5px;
            width: 20px;
        }

        a.pic7:hover {
            background-position: -200px -26px;
            width: 20px;
        }


      	#ServerNum,#ServerNum p {
			line-height: 10px;
			text-align: center;
			color: white;
			height: 10px;
		}


        /*slide*/
        .front, .items, .item {
            position: absolute;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            overflow: hidden;
        }

        .back {
            bottom: 70px;
            position: absolute;
            left: 0;
            top: 0;
            width: 100%;
            overflow: hidden;
        }

        .items {
            overflow: visible;
        }

        .item {
            background: #fff none no-repeat center center;
            -webkit-background-size: cover;
            -moz-background-size: cover;
            -o-background-size: cover;
            background-size: cover;
            display: none;
        }
    </style>
    
 	
    <!--[if lte IE 8]>
    <style>
        .slogan, .main-entry a .title i, .logo {
            background-image: none !important;
        }
        .slogan {
            filter: progid:DXImageTransform.Microsoft.AlphaImageLoader(src="https://img.alicdn.com/tps/TB1POhqIFXXXXXbXFXXXXXXXXXX.png", sizingMethod="scale");
        }

        .main-entry a .title i {
            filter: progid:DXImageTransform.Microsoft.AlphaImageLoader(src="https://img.alicdn.com/tps/TB1uh30IpXXXXXKXVXXXXXXXXXX.png", sizingMethod="scale");
        }

        .main-entry a .title .seller {
            filter: progid:DXImageTransform.Microsoft.AlphaImageLoader(src="https://img.alicdn.com/tps/TB12JNkIFXXXXXBXXXXXXXXXXXX.png", sizingMethod="scale");
        }

        .logo {
            filter: progid:DXImageTransform.Microsoft.AlphaImageLoader(src="https://img.alicdn.com/tps/TB17ghmIFXXXXXAXFXXXXXXXXXX.png", sizingMethod="scale");
        }

        .item1 {
            filter: progid:DXImageTransform.Microsoft.AlphaImageLoader(src="https://img.alicdn.com/tps/TB1h9xxIFXXXXbKXXXXXXXXXXXX.jpg", sizingMethod="scale");
        }

        .item2 {
            filter: progid:DXImageTransform.Microsoft.AlphaImageLoader(src="https://img.alicdn.com/tps/TB1pfG4IFXXXXc6XXXXXXXXXXXX.jpg", sizingMethod="scale");
        }

        .item3 {
            filter: progid:DXImageTransform.Microsoft.AlphaImageLoader(src="https://img.alicdn.com/tps/TB1sXGYIFXXXXc5XpXXXXXXXXXX.jpg", sizingMethod="scale");
        }
    </style>
    <![endif]-->
	
</head>
<body>
<div class="main">
    <div class="header">
        <div class="nav">
            <div class="logo"></div>
            <div class="entry">
                
                <span class="state">我已有支付宝账户</span>
				
                	<a href="https://auth.alipay.com/login/index.htm?goto=https%3A%2F%2Fwww.alipay.com%2F" target="_self" seed="">快速登录</a>
				
                
            </div>
        </div>
    </div>
    <div class="container">
        <div class="content">
            <div class="wrap">
                <div class="slogan"></div>
                <div class="mid">
                    <div class="main-entry">
                        <a href="javascript:;" class="developer-login"><span class="title"><i
                                class="developer"></i>我是合作伙伴</span><s></s></a>
                        <a href="javascript:;" class="seller-login">
                            <span class="title"><i class="seller"></i>我是商家用户</span>
                            <span class="seller-entry alipay">我是支付宝商家</span>
                            <span class="inerval-line"></span>
                            <span class="seller-entry koubei">我是口碑商家</span><s></s>
                        </a>
                        <a href="javascript:;" class="personal-login"><span class="title"><i
                                class="personal"></i>我是个人用户</span><s></s></a>
                    </div>
                </div>
            </div>
        </div>
        <div class="back">
 			
            <div class="items">
                <div class="item item1"
                     style="background-image:url(https://img.alicdn.com/tps/TB1h9xxIFXXXXbKXXXXXXXXXXXX.jpg)"></div>
                <div class="item item2"
                     style="background-image:url(https://img.alicdn.com/tps/TB1pfG4IFXXXXc6XXXXXXXXXXXX.jpg)"></div>
                <div class="item item3"
                     style="background-image:url(https://img.alicdn.com/tps/TB1sXGYIFXXXXc5XpXXXXXXXXXX.jpg)"></div>
            </div>
          	
        </div>
    </div>
    <div class="footer">
 		
        <div class="nav-links">
            <ul>
                <li><a href="https://www.antfin.com/" target="_blank" seed="">蚂蚁金服集团</a></li>
                <li>|</li>
                <li><a href="https://www.alipay.com" target="_blank" seed="">支付宝</a></li>
                <li>|</li>
                <li><a href="https://yebprod.alipay.com/yeb/index.htm" target="_blank" seed="">余额宝</a></li>
                <li>|</li>
                <li><a href="https://zcbprod.alipay.com/index.htm" target="_blank" seed="">招财宝</a></li>
                <li>|</li>
                <li><a href="https://b.alipay.com/?ynsrc=zhuzhanA" target="_blank" seed="">蚂蚁商家中心</a></li>
                <li>|</li>
                <li><a href="https://b.zmxy.com.cn/index.htm?scene=alipay" target="_blank" seed="">芝麻信用</a></li>
                <li>|</li>
                <li><a href="https://loan.mybank.cn/" target="_blank" seed="">蚂蚁微贷</a></li>
                <li>|</li>
                <li><a href="https://www.mybank.cn/index.htm" target="_blank" seed="">网商银行</a></li>
                <li>|</li>
                <li><a href="https://open.alipay.com/platform/home.htm?from=zhuzhanfooter20160818" target="_blank" seed="">开放平台</a></li>
                <li>|</li>
                <li><a href="https://job.alibaba.com/index.php" target="_blank" seed="">诚征英才</a></li>
                <li>|</li>
                <li><a href="https://ab.alipay.com/i/lianxi.htm" target="_blank" seed="">联系我们</a></li>
                <li>|</li>
                <li><a href="https://global.alipay.com/ospay/home.htm" target="_blank" seed="">International Business</a></li>

            </ul>
        </div>
        <div class="ownership">
            <span>沪ICP备15027489号</span>
        </div>
        <div class="nav-icons">
            <a href="https://fun.alipay.com/certificate/zfxkz.htm" class="pic1" target="_blank"></a>
            <a href="https://sealinfo.verisign.com/splash?form_file=fdf/splash.fdf&dn=WWW.ALIPAY.COM&zh_cn" class="pic2" target="_blank"></a>
            <a href="javascript:;" class="pic3" target="_blank"></a>
            <a href="https://218.242.124.22:8082/businessCheck/verifKey.do?showType=extShow&serial=9031000020170804134136000001976564-SAIC_SHOW_310000-20171207172223656605&signData=MEQCIDCR02jCtATl3sgiTFhhYL6QUvDtPGieb+RKNNviAcQvAiBkSTiJ2Z8PkNy//jFUelj5hVt+Zqth4/xDuiLv+FVibA==" class="pic4" target="_blank"></a>
            <a href="https://fun.alipay.com/certificate/index.htm" class="pic7" target="_blank"></a>
        </div>
      	
		<div id="ServerNum"><p>homeproxy-49-5008</p></div>
    </div>
</div>
<script src="https://t.alipayobjects.com/images/rmsweb/T19ctgXcRlXXXXXXXX.js"></script>
<script>

    var slideEle = slider($('.items'));

    function slider(elem) {
        var items = elem.children(),
                max = items.length - 1,
                animating = false,
                currentElem,
                nextElem,
                pos = 0;

        sync();

        return {
            next: function () {
                move(1);
            },
            prev: function () {
                move(-1);
            },
            itemsNum: items && items.length
        };

        function move(dir) {
            if (animating) {
                return;
            }
            if (dir > 0 && pos == max || dir < 0 && pos == 0) {
                if (dir > 0) {
                    nextElem = elem.children('div').first().remove();
                    nextElem.hide();
                    elem.append(nextElem);
                } else {
                    nextElem = elem.children('div').last().remove();
                    nextElem.hide();
                    elem.prepend(nextElem);
                }
                pos -= dir;
                sync();
            }
            animating = true;
            items = elem.children();
            currentElem = items[pos + dir];
            $(currentElem).fadeIn(400, function () {
                pos += dir;
                animating = false;
            });
        }

        function sync() {
            items = elem.children();
            for (var i = 0; i < items.length; ++i) {
                items[i].style.display = i == pos ? 'block' : '';
            }
        }

    }

    if (slideEle.itemsNum && slideEle.itemsNum > 1) {
        setInterval(function () {
            slideEle.next();
        }, 4000)
    }


</script>
<script>
    function setCookie(cname, cvalue, exdays) {
        var d = new Date();
        d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
        var expires = "expires=" + d.toUTCString();
        document.cookie = cname + "=" + cvalue + "; " + expires;
    }

	
    //cookie记录个人登录标记为1,商家登录标记为2
    $(".personal-login").click(function () {
        setCookie("_n_h_n_option", "1", 365);
        location.href = "https://www.alipay.com";
    });

    $(".seller-login").click(function (e) {
        var target = $(e.target);
        if (target.hasClass('alipay')) {
            location.href = "https://b.alipay.com/?ynsrc=zhuzhanA";
        } else if (target.hasClass('koubei')) {
            location.href = "https://e.alipay.com/index.htm?from=zhuzhan20160927";
        }
    });
    $(".developer-login").click(function () {
        location.href = "https://open.alipay.com/platform/home.htm?from=zhuzhan20160818";
    });
	

</script>
</body>
</html><!-- FD:homeproxy-home:homeproxy/home/startup.vm:startup.schema:END --><!-- FD:homeproxy-home:homeproxy/home/startup.vm:END -->
'''

soup = BeautifulSoup(text, 'lxml') # 会补全 html，body和p

# print(soup.prettify())  # 直接输出文档，str类型，默认utf-8
# print(soup.prettify('gbk')) # 传入编码，输出 bytes
# print(soup.prettify('gbk').decode('gbk')) # 传入编码，输出 str


# print(soup.title) # 标签，包括标签本身
# print(soup.title.name) # 标签的名字
# s = soup.title.string
# print(soup.title.string) # 标签的内容, NavigableString 对象
# print(soup.title.text) # 标签的内容， str 对象  ,一般都使用这个方法 获取 文本

# print(soup.meta) # 标签  取任意位置的第一个 meta 标签
# print(soup.meta['charset']) # 标签属性
# print(soup.meta.get('charset'))

# print(soup.meta.parent.name) # 标签的父标签
# print(soup.html.parent.name)
# print(soup.html.parent.parent)

# text = '''
# <a><b>text1</b> <c>text2</c>
# <d>text3</d><e e1='100'/><f f1='101'/><></a>
# '''
sibling_soup = BeautifulSoup(text, 'lxml')
# print(sibling_soup.b.next_sibling) #  兄弟节点
# print(sibling_soup.c.previous_sibling) #  兄弟节点
# print(sibling_soup.c.next_sibling) #  兄弟节点，是 换行符
# print(sibling_soup.d.previous_sibling) #  兄弟节点，是 换行符

# \n 、 空格、  文本， 都算作一个 element
# print(sibling_soup.a.next_element) #  下一个元素，是 <b>text1</b>
# print(sibling_soup.b.next_element) #  下一个元素，是 text1
# print(sibling_soup.b.next_element.next_element) #  下一个元素，是 换行符
# print(sibling_soup.d.previous_element) #  上一个元素，是 换行符
# print(sibling_soup.f.previous_element) #  上一个元素，是 <e e1='100'/>
# print('结束')

# print(soup.find_all('meta')) # 查找所有
# print(soup.find_all('meta', limit=2)) # 查找所有,  limit 限制取 2个
# print(soup.find('meta', {'name': 'renderer'})) # 查找特定的一个标签，其实也是调用的find_all，不过会在取到一个值后返回
# print(target="_blank") # 根据id查找特定的一个标签
#
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
#
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
print(soup.select("title")) # 标签名
print(soup.select("html > head > title")) # 逐层查找
print(soup.select("body a")) # 不逐层查找

print(soup.select("body > a")) # >  子节点
print(len(soup.select("body > div"))) # >  子节点
print(soup.select("body > div")) # >  子节点

print(soup.select("input ~ p")) # >  兄弟节点

print(soup.select("#test_id"))  # 通过id
print(soup.select("input#test_id"))  # 通过id

print(soup.select('.test_class')) # 通过class

print(soup.select('meta[charset="gb2312"]'))