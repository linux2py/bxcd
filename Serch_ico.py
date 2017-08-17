import requests
from bs4 import BeautifulSoup
import re
import time

#下载文件,需将url,和存放文件路径传入
def download_file(url,File_path):
    # 文件地址格式为：href="http://download.easyicon.net/ico/1092557/16/，所以取出URL的-3字符串做文件名。
    local_filename = url.split('/')[-3]
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    #文件类型为图标文件，所以以ICO结尾。
    with open(File_path+local_filename+'.ico', 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                #f.flush() commented by recommendation from J.F.Sebastian
    return local_filename



#输入搜索关键字
SerchKEY = input('Please input Keywork: ')
#文件存放路径
File_path = 'D:\\Temp\\'
url = 'http://www.easyicon.net/iconsearch/'+SerchKEY+'/&min=16&max=16'


html_t = requests.get(url)
#<meta charset="utf-8">
html_t.encoding = 'utf-8'
soup = BeautifulSoup(html_t.content, "html.parser")
dlink_div = soup.find('div',id="result_right_layout")
#判断是否搜索到关键字，如果未搜索到关键字提示用户。
try:
    text = dlink_div.find('p').get_text()
except AttributeError:
    text = 'NoneType'
if ( text == 'Try another keyword / 换个关键词试试吧。'):
    print('Try another keyword')
else:
    ICO_a = dlink_div.find_all('a',title="ICO 格式图标下载")
    head = re.compile('<a href="')
    last = re.compile('" title="ICO 格式图标下载">ICO</a>')
    for i in ICO_a:
        i = head.sub('', str(i))
        i = last.sub('',i)
        download_file(i,File_path)
        time.sleep(3)
