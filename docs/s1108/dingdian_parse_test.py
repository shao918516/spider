#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Terry'

"""
    需求：
    访问 https://www.23us.so/xiaoshuo/14789.html
    解析其中的文本内容，
    使用3种方式，  正则、xpath、bs4
    得到如下信息：
    小说名
    小说类别
    作者
    状态
    全文长度
    总点击数
"""

import requests
import re
from lxml import etree
from bs4 import BeautifulSoup

def get_dingdian_text():
    # url = 'https://www.23us.so/xiaoshuo/14789.html'
    # text = requests.get(url).text

    text = """
<!DOCTYPE html>
<head>
<title>神级大魔头 拉姆|无弹窗广告|最新章节 - 顶点小说网</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf8" />
<meta name="keywords" content="神级大魔头" />
<meta name="description" content="神级大魔头 无弹窗广告全文阅读及神级大魔头最新章节第2081章 燃烧军团 ,神级大魔头 作者拉姆 " />
<link rel="stylesheet" href="/23us/css/style.css" type="text/css"/>
<script language="javascript" type="text/javascript" src="/23us/js/xiaoshuo.js?3"></script>

</head>
<!---->
<body>

<div class="main m_head">
<div class="h_logo fl"><a href="https://www.23us.so/"><img src="/23us/images/logo.gif" alt="顶点小说网" /></a></div>
<div class="h_body fl">
<div><p class="fr">
<a rel="nofollow" onclick="this.style.behavior='url(#default#homepage)';this.setHomePage('https://www.23us.so');" href="#">设为首页</a> | <a rel="nofollow" href="mailto:">联系我们</a> | <a rel="nofollow" href="javascript:window.external.addFavorite('https://www.23us.so','顶点小说网')">加入收藏</a></p>
顶点小说网：没有弹窗广告 小说免费阅读
</div>
<div>
<dl class="fl">
<script type="text/javascript">show_search_top();</script>
</dl>
<dl class="fr loginbox">
<script>login();</script>
</dl>

</div>
</div>
</div>
<div class="main m_menu">
    <ul>
        <li class="m_ml"></li><li><a href="/">首页</a></li>
            <li><a href="/list/1_1.html">玄幻魔法</a></li>
            <li><a href="/list/2_1.html">武侠修真</a></li>
            <li><a href="/list/3_1.html">都市言情</a></li>
            <li><a href="/list/4_1.html">历史军事</a></li>
            <li><a href="/list/5_1.html">网游竞技</a></li>
            <li><a href="/list/6_1.html">科幻小说</a></li>
            <li><a href="/list/7_1.html">恐怖灵异</a></li>
            <li><a href="/list/8_1.html">女生小说</a></li>
            <li><a href="/list/9_1.html">其他小说</a></li>
        <li><a href="/full.html">全本小说</a></li>
        <li class="m_bc"><a rel="nofollow" href="https://www.23us.so/modules/article/bookcase.php"></a></li><li class="m_mr"></li>
    </ul>
</div>
<script>top_bar()</script><!--中心区域-->
<div class="main">

    <div id="left">

        <div class="block">
            <div class="blocktitle wsd"><i></i>会员推荐</div>
            <div class="blockcontent">
              <ul class="ultop">

    <li><p>13527</p><a href="https://www.23us.so/xiaoshuo/2521.html" target="_blank">儒道至圣</a></li>
    <li><p>10589</p><a href="https://www.23us.so/xiaoshuo/2739.html" target="_blank">九星</a></li>
    <li><p>9947</p><a href="https://www.23us.so/xiaoshuo/2527.html" target="_blank">非凡洪荒</a></li>
    <li><p>9375</p><a href="https://www.23us.so/xiaoshuo/419.html" target="_blank">电影世界逍遥行</a></li>
    <li><p>8218</p><a href="https://www.23us.so/xiaoshuo/13694.html" target="_blank">圣墟</a></li>
    <li><p>8056</p><a href="https://www.23us.so/xiaoshuo/23024.html" target="_blank">黄金渔村</a></li>
    <li><p>7359</p><a href="https://www.23us.so/xiaoshuo/21987.html" target="_blank">全职召唤师系统</a></li>
    <li><p>6289</p><a href="https://www.23us.so/xiaoshuo/14823.html" target="_blank">我真不是开玩笑</a></li>
    <li><p>5272</p><a href="https://www.23us.so/xiaoshuo/9495.html" target="_blank">不朽凡人</a></li>
    <li><p>5012</p><a href="https://www.23us.so/xiaoshuo/23037.html" target="_blank">诸天投影</a></li>
    <li><p>4874</p><a href="https://www.23us.so/xiaoshuo/15146.html" target="_blank">逍遥梦路</a></li>
    <li><p>4707</p><a href="https://www.23us.so/xiaoshuo/3475.html" target="_blank">马前卒</a></li>
    <li><p>4653</p><a href="https://www.23us.so/xiaoshuo/14220.html" target="_blank">放开那个女巫</a></li>
    <li><p>4511</p><a href="https://www.23us.so/xiaoshuo/14617.html" target="_blank">民国之文豪崛起</a></li>
    <li><p>4331</p><a href="https://www.23us.so/xiaoshuo/14490.html" target="_blank">郭大炮的文娱生涯</a></li>

  <li style=" list-style:none; text-align:right; border:none;"><a href="/top/monthvisit_1.html">更多...</a></li>
              </ul>
            </div>
        </div>
        
            <div class="block">
                <div class="blocktitle wld"><i></i>排 行 榜</div>
                <div class="blockcontent wld"><ul class="ulcenter">
<li style="width:50%;float:left;"><a href="https://www.23us.so/top/allvisit_1.html">总排行榜</a></li>
<li style="width:50%;float:left;"><a href="https://www.23us.so/top/allvote_1.html">总推荐榜</a></li>
<li style="width:50%;float:left;"><a href="https://www.23us.so/top/monthvisit_1.html">月排行榜</a></li>
<li style="width:50%;float:left;"><a href="https://www.23us.so/top/monthvote_1.html">月推荐榜</a></li>
<li style="width:50%;float:left;"><a href="https://www.23us.so/top/weekvisit_1.html">周排行榜</a></li>
<li style="width:50%;float:left;"><a href="https://www.23us.so/top/weekvote_1.html">周推荐榜</a></li>
<li style="width:50%;float:left;"><a href="https://www.23us.so/top/postdate_1.html">最新入库</a></li>
<li style="width:50%;float:left;"><a href="https://www.23us.so/top/lastupdate_1.html">最近更新</a></li>
<li style="width:50%;float:left;"><a href="https://www.23us.so/top/authorupdate_1.html">原创更新</a></li>
<li style="width:50%;float:left;"><a href="https://www.23us.so/top/masterupdate_1.html">转载更新</a></li>
<li style="width:50%;float:left;"><a href="https://www.23us.so/top/goodnum_1.html">总收藏榜</a></li>
<li style="width:50%;float:left;"><a href="https://www.23us.so/top/size_1.html">字数排行</a></li>
</ul>
<div class="cl" style="margin-top:10px;"></div></div>
            </div>
        
    </div>
    <div id="centerm">
 
 

 
<!--BOOKcat-->

<div class="cl" style="height:8px;"></div>
<div class="bdtop"></div>
<div class="bdsub">
    <dl id="content">
    
<div class="adhtml"><script>show_book();</script></div>
<dd><h1>神级大魔头 全文阅读</h1></dd>
<dd><div class="fl"><a class="hst" href="https://www.23us.so/files/article/html/14/14789/index.html"><img style="padding:7px; border:1px solid #E4E4E4; width:120px; height:150px; margin:0 25px 0 15px;" alt="神级大魔头最新章节列表,神级大魔头全文阅读" src="https://www.23us.so/files/article/image/14/14789/14789s.jpg"/></a></div>
<div class="fl" style="width:550px;"><style>.pl{background:#F2F2F2; padding-left:10px;}</style>
<p>
<table cellspacing="1" cellpadding="0" bgcolor="#E4E4E4" id="at">
<tr>

<th>小说类别</th>
<td>&nbsp;<a href="/list/1_1.html">玄幻奇幻</a></td>

<th>小说作者</th>
<td>&nbsp;拉姆</td>
<th>小说状态</th>
<td>&nbsp;连载中</td></tr><tr>
<th>收 藏 数</th>
<td>&nbsp;236</td>
<th>全文长度</th>
<td>&nbsp;3796896字</td>
<th>最后更新</th>
<td>&nbsp;2018-11-08 08:44:44</td></tr>
<tr>
<th>总点击数</th>
<td>&nbsp;283571</td>
<th>本月点击</th>
<td>&nbsp;4218</td>
<th>本周点击</th>
<td>&nbsp;1917</td></tr>
<tr>
<th>总推荐数</th>
<td>&nbsp;876</td>
<th>本月推荐</th>
<td>&nbsp;8</td>
<th>本周推荐</th>
<td>&nbsp;2</td></tr>
</table>
</p>
<p class="btnlinks">

  <a class="read" href="https://www.23us.so/files/article/html/14/14789/index.html" title="神级大魔头最新章节">最新章节</a>

  <a href="Javascript:void(0);" onclick="javascript:Ajax.Request('/addbookcase/14789.php',{onComplete:function(){if('-1'==this.response){alert('先登录再收藏！');}else{alert('加入书架成功！');}}});">加入书架</a>

  <a href="Javascript:void(0);" onclick="javascript:Ajax.Request('/recommend/14789/',{onComplete:function(){alert('推荐本书成功！');}});">推荐本书</a>

  <script>get_down_url("https://www.23us.so/xiaoshuo/14789.html","https://www.23us.so/modules/article/txtarticle.php?id=14789","神级大魔头");</script>
</p>

</dd><div class="cl"></div>
<dd style="padding-top:0;">
<!-- Baidu Button BEGIN -->
  <div class="jia fl"><div class="fl">分享到：</div>
      <div id="bdshare" class="bdshare_t bds_tools get-codes-bdshare">
          <a class="bds_qzone">QQ空间</a>
          <a class="bds_tsina">新浪微博</a>
          <a class="bds_tqq">腾讯微博</a>
          <a class="bds_renren">人人网</a>
          <span class="bds_more">更多</span>
      </div>
  </div>
  <div class="mobile fl">手机看小说： <font style="color:#0066FF">m.23us.so</font></div>
</dd>
<!-- Baidu Button END -->
<div class="cl"></div>
<dd style="padding:10px 30px 0 25px;">
<p class="pl"><b>内容简介：</b></p>
<table width="740px" border="0" cellspacing="0" cellpadding="0" style="padding:5px 5px 5px 5px;">
  <tr> 
    
<td align="right" style="padding:5px 5px 5px 5px;"><script>show_book2();</script></td>
    
<td align="left" style="padding:5px 5px 5px 5px;"><script>show_book2();</script></td>
  </tr>
</table>

<p>&nbsp;&nbsp;&nbsp;&nbsp;    “无耻夏平，抢我秘籍，夺我丹药，泡我未婚妻，我和你不共戴天。”    “他是武道之耻，人类蛀虫，是人渣败类。”    “无恶不作，连三岁小儿的棒棒糖也抢，老人过马路都不扶。”    “四处惹是生非，各大家族的天才都被他殴打过，人神共愤啊。”    炎黄星无数武道强者对夏平咬牙切齿，简直恨不得将其挫骨扬灰。    而夏平面对这么多人的仇恨，淡定的拉出“超级仇恨系统”界面，看着上面各种好东西，摸了摸下巴：“都积攒到这么多仇恨值了，不知道是兑换圣品丹药混沌丹，还是绝世武学如来掌，或者是神器乾坤鼎，真是烦恼啊。”    作者自定义标签:                                                腹黑                                                练功流                                                学生                                                赚钱<br />
</p><p style="display:none" id="sidename">分享书籍《神级大魔头》作者：拉姆</p>
<p style="height:10px;"></p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;关键字：<u>神级大魔头 拉姆</u> <u>神级大魔头全文阅读</u> <u>神级大魔头最新章节</u></p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;最近章节：<a href="https://www.23us.so/files/article/html/14/14789/13918707.html">第2081章 燃烧军团</a></p>
<p style="height:10px;"></p>
</table>
</dd>
</dl>
    <div class="cl" style="padding-top:10px;"></div>
</div>

<!--BOOKcat-->
 

</div><!--中间部分DIV结束-->
 

</div>
<!--中心区域结束-->

 
<div class="cl" style="height:8px;"></div>
<div class="main footer">
<div class="bdtop"><i></i><span title="0.042314"></span></div>
<div class="ftc">顶点小说网没有弹窗广告，所有小说都能免费阅读。找好看的小说网站，就到顶点小说网。
<br />Copyright &copy; 2016 <a href="https://www.23us.so">顶点小说网</a>(www.23us.so) All Rights Reserved. </div>
<script>show_foot();</script>
</div>

<script>
  Ajax.Request('/bookclick/14789/',{onComplete:function(){}});
</script>
</body>
</html>
    """

    return text

def parse_text_re(text):
    # name = re.search(r'<h1>(.*?)</h1>', text).group(1).replace(' 全文阅读', '')
    name = re.search(r'name="keywords" content="(.*?)"', text).group(1)
    book_type = re.search(r'小说类别.*?<a.*?>(.*?)</a>', text, re.RegexFlag.S).group(1)
    author = re.search(r'小说作者.*?<td>(.*?)</td>', text, re.RegexFlag.S).group(1).replace('&nbsp;', '')
    status = re.search(r'小说状态.*?<td>(.*?)</td>', text, re.RegexFlag.S).group(1).replace('&nbsp;', '')
    words = re.search(r'全文长度.*?<td>(.*?)</td>', text, re.RegexFlag.S).group(1).replace('&nbsp;', '').replace('字', '')
    clicks = re.search(r'总点击数.*?<td>(.*?)</td>', text, re.RegexFlag.S).group(1).replace('&nbsp;', '')

    return {
        'name': name,
        'book_type': book_type,
        'author': author,
        'status': status,
        'words': words,
        'clicks': clicks,
    }

def parse_text_xpath(text):
    # 初始化 etree
    tree = etree.HTML(text)

    name = tree.xpath('//meta[@name="keywords"]/@content')[0]
    # 找到 table 元素
    table_ele = tree.xpath('//*[@id="at"]')[0]
    # 使用这种元素 进行再次搜索 , 不要使用 // ，
    # 一旦使用 // ，那么就会重新搜索整个 tree
    book_type = table_ele.xpath('./tr[1]/td[1]/a/text()')[0]
    author = table_ele.xpath('./tr[1]/td[2]/text()')[0].strip()
    status = table_ele.xpath('./tr[1]/td[3]/text()')[0].strip()
    words = table_ele.xpath('./tr[2]/td[2]/text()')[0].strip().replace('字', '')
    clicks = table_ele.xpath('./tr[3]/td[1]/text()')[0].strip()

    return {
        'name': name,
        'book_type': book_type,
        'author': author,
        'status': status,
        'words': words,
        'clicks': clicks,
    }

def parse_text_bs4(text):
    soup = BeautifulSoup(text, 'lxml')

    name = soup.find('meta', {'name': 'keywords'}).get('content')
    # 根据 id 确定table
    table_ele = soup.find(id='at')

    book_type = table_ele.a.text

    # 查找 table 下的 所有 td
    tds = table_ele.find_all('td')

    author = tds[1].text.strip()
    status = tds[2].text.strip()
    words = tds[4].text.strip().replace('字', '')
    clicks = tds[6].text.strip()

    return {
        'name': name,
        'book_type': book_type,
        'author': author,
        'status': status,
        'words': words,
        'clicks': clicks,
    }

def parse_dingdian_text(feature='re'):
    text = get_dingdian_text()

    if 'bs4' == feature:
        book_dict = parse_text_bs4(text)
    elif 'xpath' == feature:
        book_dict = parse_text_xpath(text)
    else:
        book_dict = parse_text_re(text)

    print(f"小说名：{book_dict['name']}, "
          f"类型：{book_dict['book_type']}, "
          f"作者：{book_dict['author']}， "
          f"状态：{book_dict['status']}， "
          f"总字数：{book_dict['words']}， "
          f"总点击数：{book_dict['clicks']}")

if __name__ == '__main__':
    # parse_dingdian_text()
    # parse_dingdian_text('xpath')
    parse_dingdian_text('bs4')