import sqlite3
import msvcrt
import os

#数据库链接
conn = sqlite3.connect(r'.\bxcd.db')

#--------------------------------
#       查询功能
#--------------------------------
def Search_text(Word):
    SQL = "SELECT Text from Dict01 where Word = '%s' ;" % (Word)
    text = conn.execute(SQL)
    text2 = text.fetchall()
    #空list本身等同于False
    if text2:
        return text2
    else:
        return [('无此关键字。',)]

def List_text(Word):
    #双%做转义使用。
    SQL = "SELECT * from Dict01 where Word like '%%%s%%';" % (Word)
    text = conn.execute(SQL)
    text2 = text.fetchall()
    if text2:
        return text2
    else:
        return [('无此关键字。','')]


#--------------------------------
#       新增功能
#--------------------------------
#--提示成功，但数据库中不存在,使用commit()提交。
def Add_text(Key,text = 'Null'):
    SQL = "INSERT INTO Dict01 VALUES('{_Key}','{_text}');".format(_Key=Key, _text=text)
    try:
        SID = conn.execute(SQL)
    except sqlite3.IntegrityError:
        return '词条已存在。'
    conn.commit()
    return '已插入数据。'

#--------------------------------
#       更新功能
#--------------------------------
#没有的关键字也会提示执行完毕
def Update_text(Key,text = 'Null'):
    SQL = "UPDATE  Dict01 SET Text = '{_text}' WHERE WORD = '{_Key}';".format(_Key=Key, _text=text)
    SID = conn.execute(SQL)
    conn.commit()
    return '已更新数据。'


#--------------------------------
#       删除功能
#--------------------------------
#delete 语句同update 语句一样，没有的词条也会提示执行完成。
def DEL_text(Key):
    SQL = "DELETE  from Dict01 where Word = '{_Key}';".format(_Key=Key)
    SID = conn.execute(SQL)
    conn.commit()
    return '已删除数据。'

def DEL_ALL_text(Key):
    SQL = "DELETE  from Dict01 where Word like '{_Key}%';".format(_Key=Key)
    SID = conn.execute(SQL)
    conn.commit()
    return '已删除所有数据。'


#--------------------------------
#       菜单功能
#--------------------------------
#获取一个输入
def get_key01():
    while True:
        Word = input('请输入关键字： ')
        if Word == '':
            print('输入不能为空！')
        else:
            return Word
            break

#获取两个输入
def get_key02():
    while True:
        Key = input('请输入词条头： ')
        text = input('请输入词条解释： ')
        if Key == '' or text == '':
            print('词条头或词条解释不能为空!')
        else:
            return [Key,text]
            break

#等待状态
def get_input():
    sleeps = msvcrt.getch()
    os.system('cls')

def menu():
    print('''
    1.查询词条
    2.模糊查询
    3.新增词条
    4.更新词条
    5.删除词条
    6.退出(Q)
    ''')
    N = ['1','2','3','4','5','6','Q','q']
    while True:
        Number = input('请选择功能： ')
        if Number in N:
            return Number
            break
        else:
            print("选择错误请重新选择")

while True:
    x = menu()
    if x == '1':
        Word = get_key01()
        # 查询
        for i in Search_text(Word):
            print(i[0])
        get_input()
    elif x == '2':
        Word = get_key01()
        # 查询
        for i in List_text(Word):
            print(i[0], ':', i[1])
        get_input()
    elif x == '3':
        Word = get_key02()
        print(Add_text(Word[0],Word[1]))
        get_input()
    elif x == '4':
        Word = get_key02()
        print(Update_text(Word[0], Word[1]))
        get_input()
    elif x == '5':
        Word = get_key01()
        print(DEL_text(Word))
        get_input()
    else:
        break


conn.close()