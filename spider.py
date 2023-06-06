# -*- codeing = uft-8 -*-
import sys
from bs4 import BeautifulSoup  # 网页解析，获取数据
import re  # 正则表达式，进行文字匹配
import urllib.request, urllib.error  # 进行制定url，获取网页数据
import xlwt  # 进行excel操作
import pymysql


# 连接mysql
def mysql_connection(name):
    # 连接到MySQL数据库
    conn = pymysql.connect(
        host='localhost',  # MySQL服务器地址
        user='root',  # 用户名
        password='root',  # 密码
        database='database_name',  # 数据库名称
        charset='utf8mb4'  # 字符编码
    )

    # 创建游标对象
    cursor = conn.cursor()

    # 执行SQL查询
    sql = 'SELECT * FROM table_name'
    cursor.execute(sql)

    # 获取查询结果
    result = cursor.fetchall()
    for row in result:
        print(row)

    # 关闭游标和连接
    cursor.close()
    conn.close()


def main():
    baseurl = "https://movie.douban.com/top250?start="
    # 1、爬取网页
    datalist = getData(baseurl)
    # 2、解析数据
    # 3、保存数据
    # saveData(datalist,"豆瓣Top250.xls")
    saveData2DB(datalist)


findLink = re.compile(r'<a href="(.*?)">')  # 创建正则表达式对象，表示规则（字符串的模式）
findImgSrc = re.compile(r'<img.*src="(.*?)"', re.S)  # 忽略换行符
findTitle = re.compile(r'<span class="title">(.*)</span>')
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
findJudge = re.compile(r'<span>(\d*)人评价</span>')
findInq = re.compile(r'<span class="inq">(.*)</span>')
findBd = re.compile(r'<p class="">(.*?)</p>', re.S)


def getData(baseurl):
    datalist = []
    for i in range(0, 10):
        url = baseurl + str(i * 25)
        html = askURL(url)
        # 逐一解析数据
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.findAll('div', class_="item"):  # 查找符合要求的字符串，形成列表
            data = []  # 保存一部电影的所有信息
            item = str(item)
            # 影片链接
            link = re.findall(findLink, item)[0]  # re库用来通过正则表达式查找指定的字符串
            data.append(link)
            imgSrc = re.findall(findImgSrc, item)[0]  # 添加图片
            data.append(imgSrc)
            titles = re.findall(findTitle, item)  # 片名可能只有一个中文名，没有外国名
            if (len(titles) == 2):
                ctitle = titles[0]  # 添加中文名
                data.append(ctitle)
                otitle = titles[1].replace("/", "")  # 去掉无关的符合
                data.append(otitle)  # 添加外国名
            else:
                data.append(titles[0])
                data.append(' ')  # 外国人名为空

            rating = re.findall(findRating, item)[0]
            data.append(rating)  # 添加评分

            judgeNum = re.findall(findJudge, item)[0]
            data.append(judgeNum)  # 添加评价人数

            inq = re.findall(findInq, item)
            if len(inq) != 0:
                inq = inq[0].replace("。", "")  # 去掉句号
                data.append(inq)  # 添加概述
            else:
                data.append(' ')  # 添加概述

            bd = re.findall(findBd, item)[0]
            bd = re.sub('<br(\s+)?/>(\s+)?', " ", bd)  # 去掉<br/>
            bd = re.sub("/", " ", bd)  # 替换/
            data.append(bd.strip())  # 去掉前后的空格

            datalist.append(data)  # 处理好的一部电影信息放到list中
    # print(datalist)
    return datalist


def askURL(url):
    head = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
    }
    request = urllib.request.Request(url=url, headers=head)
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode('utf-8')
        return html
    except urllib.error.URLError as e:
        print(e.reason)


def saveData(datalist, savepath):
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)  # 创建workbook对象
    sheet = book.add_sheet('豆瓣电影Top250', cell_overwrite_ok=True)  # 创建工作表
    col = ("电影详情链接", "图片链接", "影片中文名", "影片外国名", "评分", "评价数", "概况", "相关信息")
    for i in range(0, 8):
        sheet.write(0, i, col[i])  # 列名
    for i in range(0, 250):
        print("第%d条" % (i + 1))
        data = datalist[i]
        for j in range(0, 8):
            sheet.write(i + 1, j, data[j])
    book.save(savepath)  # 保存数据表


def saveData2DB(datalist):
    init_db()
    conn = pymysql.connect(
        host='localhost',  # MySQL服务器地址
        user='root',  # 用户名
        password='root',  # 密码
        database='test.db',  # 数据库名称
        charset='utf8mb4'  # 字符编码
    )
    cur = conn.cursor()
    for data in datalist:
        for index in range(len(data)):
            if index==4 or index==5:
                continue
            data[index] = '"' + data[index] + '"'
        sql = '''
                insert into movie250(
                    info_link,pic_link,cname,ename,score,rated,instroduction,info
                )
                values(%s)
            ''' % ",".join(data)
        #print(sql)
        cur.execute(sql)
        conn.commit()
    cur.close()
    conn.close()


def init_db():
    sql = '''
    create table IF NOT EXISTS movie250
    (
        id INT  primary  key AUTO_INCREMENT,
        info_link text,
        pic_link text,
        cname varchar(64),
        ename varchar(64),
        score numeric(10, 2),
        rated numeric(10, 2),
        instroduction text,
        info text
    )
    '''  # 创建数据表
    conn = pymysql.connect(
        host='localhost',  # MySQL服务器地址
        user='root',  # 用户名
        password='root',  # 密码
        database='test.db',  # 数据库名称
        charset='utf8mb4'  # 字符编码
    )
    cursor = conn.cursor()
    # 执行创建表的SQL语句
    cursor.execute(sql)
    # 关闭游标和数据库连接
    cursor.close()
    conn.close()


if __name__ == '__main__':
    main()
    # init_db()
