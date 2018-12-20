import requests

from bs4 import BeautifulSoup

def get_text():
    url = 'https://www.23us.so/xiaoshuo/13332.html'
    response = requests.get(url)
    response.encoding = "utf-8"
    text = response.text
    return text

def parse_html(html):
    # 这里 soup 的命名和后面的 for 循环中的 soup 容易引起误解
    soup = BeautifulSoup(html,'lxml')
    print(soup.h1.string)
    # 不应该有 soup2 这样的命名， 这里通过 id 查找， 不应该使用 find_all 而是 find
    # soup2 = soup.find_all(id='at')
    table_ele = soup.find(id='at')
    # 这里的 for 循环，变量名不应该叫 soup 和上面的  soup 混淆了
    # 而且这里因为 soup2 是 通过 id 唯一确定的，根本就不应该出现 for 循环
    # for soup in soup2:

    print("{}:{}".format(table_ele.contents[1].contents[1].string, table_ele.contents[1].contents[3].contents[1].string))
    print("{}:{}".format(table_ele.contents[1].contents[5].string,table_ele.contents[1].contents[7].string))
    print("{}:{}".format(table_ele.contents[1].contents[9].string, table_ele.contents[1].contents[11].string))
    print("{}:{}".format(table_ele.contents[2].contents[1].string, table_ele.contents[2].contents[3].string))
    print("{}:{}".format(table_ele.contents[2].contents[5].string, table_ele.contents[2].contents[7].string))
    print("{}:{}".format(table_ele.contents[2].contents[9].string, table_ele.contents[2].contents[11].string))
    print("{}:{}".format(table_ele.contents[4].contents[1].string, table_ele.contents[2].contents[3].string))
    print("{}:{}".format(table_ele.contents[4].contents[5].string, table_ele.contents[2].contents[7].string))
    print("{}:{}".format(table_ele.contents[4].contents[9].string, table_ele.contents[2].contents[11].string))
    print("{}:{}".format(table_ele.contents[6].contents[1].string, table_ele.contents[2].contents[3].string))
    print("{}:{}".format(table_ele.contents[6].contents[5].string, table_ele.contents[2].contents[7].string))
    print("{}:{}".format(table_ele.contents[6].contents[9].string, table_ele.contents[2].contents[11].string))

# 只有当 当前模块 是主模块时， 才会执行其中的 代码块
if __name__ == '__main__':
    html = get_text()
    parse_html(html)



