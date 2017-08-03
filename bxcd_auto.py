#!/use/bin/env python
#自动版本，获取所有链接中的文字。
import io
import sys
import requests
from bs4 import BeautifulSoup
import re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')

#抓取分网页面URL
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
    #返回每页所有连接，及下一页连接，如果没有下一页，则返回状态0
    return links, l


# 获取具体页面正文
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



#抓取主页URL
def main_url():
    url = 'http://www.qzr.cn/dlbxcd/index.shtml'
    html_t = requests.get(url)
    html_t.encoding = 'gb18030'
    soup = BeautifulSoup(html_t.content, "html.parser")
    re_text = re.compile('/small/bxcd/bxcd[a-z]/index_1.shtml')
    a_div = soup.find_all('div')[0]
    b_td = a_div.find('td', width="576", align="right", valign="top", bgcolor="#FFFFFF", height="2794")
    a_tag = b_td.find_all('a', href=re_text)
    main_url = []
    head_text = re.compile('<a href="')
    tail_text = re.compile('">更多</a>')
    for i in a_tag:
        if (i.get_text() == '更多'):
            U = head_text.sub('http://www.qzr.cn', str(i))
            U = tail_text.sub('', U)
            main_url.append(U)
    return main_url


#调取Get_link返回所有分项URL
def get_papg(murl):
    URL_01 = []
    a = 10
    while a > 3:
        A = Get_link(murl)[0]
        murl = Get_link(murl)[1]
        # 判断，获取的该页面里是否有下一个页面
        if (murl == 0):
            URL_01 = URL_01 + A
            a = 1
        else:
            URL_01 = URL_01 + A
    return URL_01





path = 'D:\\Temp\\dict001.txt'
fp = open(path, 'a', encoding='gb18030')

fast_url = main_url()
ALL_URL = []
for url in fast_url:
    purl = get_papg(url)
    for i in purl:
        text = Get_text(i)
        fp.write(text + '\n')

fp.close()









