
import sys
from bs4 import BeautifulSoup
import urllib.request
import urllib.error
import re
import xlwt
import sqlite3
import requests
import os
count = 0
upage = 0


def main():
    print("网易云歌手专辑与发布时间爬取程序")
    a = "https://music.163.com/artist/album?id="
    print("请输入歌手在网易云的id号：")
    b = input()
    c = "&limit=12&offset=0"
    baseurl = a + b + c

    print("开始爬取。。。")
    getp(baseurl)
    dataname = getname(baseurl)
    datalist = getdata2(baseurl)

    w = "网易云歌手"
    x = "的专辑数据.xls"
    savepath = w + str(dataname[0][0]) + x

    global count
    global upage
    savedata2(datalist, savepath, upage, dataname, count)


findname = re.compile(r'<meta content="(.*?)" name="keywords">')
findalbum = re.compile(r'<p class="dec dec-1 f-thide2 f-pre" title="(.*?)">')
findtime = re.compile(r'<span class="s-fc3">(.*?)</span>')
findp = re.compile(r'')


def getp(baseurl):
    url = baseurl
    html = askurl(url)
    soup = BeautifulSoup(html, "html.parser")
    for item in soup.find_all('div',  class_="u-page"):
        for item2 in soup.find_all('a', class_="zpgi"):
            global upage
            upage = upage + 1


def getname(baseurl):
    dataname = []
    url = baseurl
    html = askurl(url)
    soup = BeautifulSoup(html, "html.parser")

    for item in soup.find_all('head'):
        item = str(item)
        name = re.findall(findname, item)
        dataname.append(name)
    return dataname


def getdata2(baseurl):
    datalist = []

    for i in range(0, upage):
        url = baseurl + str(i*12)
        html = askurl(url)
        soup = BeautifulSoup(html, "html.parser")

        for item in soup.find_all('li'):
            data = []
            item = str(item)

            album = re.findall(findalbum, item)
            data.append(album)

            time = re.findall(findtime, item)
            data.append(time)

            datalist.append(data)

        for item2 in soup.find_all('p', class_="dec dec-1 f-thide2 f-pre"):
            item2 = str(item2)

            global count
            count = count + 1

    return datalist


def askurl(url):
    head = {
       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
    }

    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")

    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "response"):
            print(e.response)
    return html


def savedata2(datalist, savepath, upage, dataname, count):
    print("保存中。。。")

    book = xlwt.Workbook(encoding="utf-8", style_compression=0)
    sheet = book.add_sheet('音乐专辑', cell_overwrite_ok=True)
    col = ("专辑", "发布时间", "音乐人")
    for c in range(0, 3):
        sheet.write(0, c, col[c])
    for i in range(0, upage):
        data = datalist[i*72 + 4]
        for m in range(0, 12):
            for j in range(0, 2):
                sheet.write(12 * i + m + 1, j, datalist[i*71 + 4 + m][j])
    for n in range(0, count):
        print("第%d条" % (n + 1))
        sheet.write(n + 1, 2, dataname[0])
    book.save(savepath)

if __name__ == '__main__':
    main()
    print('爬取完成')
    #os.system("pause")


