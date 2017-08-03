#!/use/bin/env python
#手动版本，输入URL及文件名获取分项页面中所有链接里的文字
import io
import sys
import requests
from bs4 import BeautifulSoup
import re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')

# 获取网页链接
def Get_link(url):
    #获取小类列表
    tag = re.search(r'bxcd[a-z]/',url).group()
    html_t = requests.get(url)
    html_t.encoding = 'gb18030'
    soup = BeautifulSoup(html_t.content, "html.parser")

    # 通过标签查找链接
    a_div = soup.find_all('div')[0]
    b_div = a_div.find_all('div')[4]
    c_table = b_div.find('table')
    d_table = c_table.find_all('table', width="572", bgcolor="#6687BA")[0]
    e_link = d_table.find_all('a')

    links = []
    sub = re.compile('" target=".*$')
    last = re.compile(r'下一页')
    up = re.compile(r'上一页')
    l = re.compile(r'">.*$')
    for i in e_link:
        i = str(i)
        i = i.replace('<a href="', 'http://www.qzr.cn')
        # 判断最后一条记录是否为下一页
        if (last.findall(i)):
            l = re.search(r'index_.*shtml',i).group()
            #拼接下一页地址
            l = 'http://www.qzr.cn/small/bxcd/' + tag + l
        elif(up.findall(i)):
            l = 0
        else:
            i = sub.sub('', i)
            links.append(i)
            l = 0
    return links, l


# 获取页面正文
def Get_text(url):
    html_t = requests.get(url)
    # 编码集转换
    html_t.encoding = 'gb18030'
    soup = BeautifulSoup(html_t.content, "html.parser")
    a_div = soup.find_all('div')[4]
    b_table = a_div.find('table')
    c_table = b_table.find('table')
    d_td = c_table.find_all('td')
    #获取文本应该用get_text()函数，而不应该用text方法。
    text1 = d_td[1].find('font').get_text()
    text2 = d_td[4].get_text()
    #去掉字符串里的回车符。
    rmn = re.compile('\n')
    text2 = rmn.sub('', text2)
    doc1 = text1+'\t'+text2
    return doc1


argv_text01 = '''
CS.py [URL] [PATH]
'''

p1 = re.compile('http(s)?://.*',re.I)
p2 = re.compile(r'[a-z]:\\.*',re.I)

if (len(sys.argv) < 3):
    print('请输入路径及网址')
    print(argv_text01)
    exit(1)
elif(p1.search(sys.argv[1]) and p2.search(sys.argv[2])):
    # 初始链接
    temp_url = sys.argv[1]
    URL_01 = []
    a = 10
    while a > 3:
        A = Get_link(temp_url)[0]
        temp_url = Get_link(temp_url)[1]
        # 判断，获取的该页面里是否有下一个页面
        if (temp_url == 0):
            URL_01 = URL_01 + A
            a = 1
            break
        else:
            URL_01 = URL_01 + A
    path = sys.argv[2]
    fp = open(path, 'a', encoding='gb18030')
    for i in URL_01:
        text = Get_text(i)
        fp.write(text + '\n')
    fp.close()
else:
    print('请输入正确的路径及网址')
    print(argv_text01)
    exit(1)








