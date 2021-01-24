"""
小说爬取
书趣阁
"""

miaojiang = "https://www.miaojianggushi2.com"
shuquge = "http://www.shuquge.com"

import requests
import parsel
from lxml import etree
from tkinter import *


def shuquge_get_chapter(url):
    """
    :param url:需要爬取这一章小说的地址
    :return: 爬取结果，0失败，1成功
    """
    response = requests.get(url)
    #自动解决乱码问题
    response.encoding = response.apparent_encoding
#    print(response.text)
    # 将网页数据结构化
    sel = parsel.Selector(response.text)
    if shuquge in url:
        # 根据css选择器提取标题
        chapter_title = sel.css('div.content > h1::text').get()
        # 提取内容
        content = sel.css('#content::text').getall()

    chapter_data = []
    # 去掉最后三行
    for con in content[:-3]:
        # print(con)
        # str使用replace去除空格
        chapter_data.append(con.replace('\xa0', ""))
    # print(chapter_title)
    return chapter_title, chapter_data

def shuquge_down_chapter(book_name, chapter_title, content):
    with open(book_name+'.txt', mode='a+', encoding='utf-8') as f:
        f.write("\n\n" + chapter_title + "\n")
        # 去掉最后三行
        for con in content:
            f.write(con)

def shuquge_get_url_list(url):
    """
    :param url: 传入需要爬取的网站
    :return: 响应体
    """
    response = requests.get(url)
    # 自动解决乱码问题
    response.encoding = response.apparent_encoding
    # 将网页数据结构化
    sel = parsel.Selector(response.text)

    if shuquge in url:
        # 提取出书名
        book_name = sel.xpath('//div[@class="info"]/h2/text()').get()
        # 根据xpath提取每个章节目录地址
        index = sel.xpath('//dl/dd/a/@href').getall()

    print(book_name)
    url_list = []

    # 前12个地址为最新章节地址，有重复，去除掉
    for i in index[12:]:
        # print(url.replace('index.html', "") + i)
        # get_chapter(book_name, url.replace('index.html', "") + i)
        url_list.append(url.replace('index.html', "") + i)

    return book_name, url_list


def shuquge_search_api(book_name):
    search_url = "http://www.shuquge.com/search.php"
    data = {
        's': "6445266503022880974",
        'searchkey': book_name
    }
    # print(data)
    res = requests.post(search_url, data)  # 进行post请求
    res.encoding = 'utf-8'
    # print(res.text)
    html = etree.HTML(res.text)  # <Element html at 0x7ff3fe0d6108>
    # print(html)

    book_root = html.xpath("//*[@class='bookcase']")
    # print(etree.tostring(book_root[0]))

    book_list = book_root[0].xpath("//*[@class='bookbox']")
    # print(book_list)

    if len(book_list) == 0:  # 搜索结果为空时
        return []
    book_id_list = book_list[0].xpath("//*[@class='bookname']/a/@href")
    # print(book_id_list)

    book_name_list = book_list[0].xpath("//*[@class='bookname']/a/text()")
    # print(book_name_list)

    book_user_list = book_list[0].xpath("//*[@class='author']/text()")
    # print(book_user_list)

    book_size_list = book_list[0].xpath("//*[@class='update']/a/text()")
    # print(book_size_list)
    book_list_meesage = []

    i = 0
    for item in book_name_list:
        book_buf = {}
        book_buf["book_name"] = item
        book_id = re.match(r"(.*)/(.*?)/.*", book_id_list[i]).group(2)
        book_buf["book_url"] = "http://www.shuquge.com/txt/{}/index.html".format(book_id)
        book_buf["book_user"] = book_user_list[i].split("：")[1]
        try:
            book_buf["book_size"] = book_size_list[i]
        except:
            print("book_size_list erro")
            book_buf["book_size"] = ""

        i += 1
        book_list_meesage.append(book_buf)
        # print(book_buf["book_name"], " : ", book_buf["book_user"], " : ", book_buf["book_size"])
        # print(book_buf["book_url"])
        # print("*********************************************")
    return book_list_meesage
    # get_book(book_url)




if __name__ == '__main__':
    url = "http://www.shuquge.com/txt/100/index.html"
    shuquge_get_url_list(url)
    # shuquge_search_api("羊皮卷")
