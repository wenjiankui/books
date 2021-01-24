"""
小说爬取
无忧书城
url： https://www.51shucheng.net/
"""

wuyou = "https://www.51shucheng.net/"

import requests
import parsel
from lxml import etree
from tkinter import *


def wuyou_get_chapter(url):
    """
    :param url:需要爬取这一章小说的地址
    :return: 爬取结果，0失败，1成功
    """
    response = requests.get(url)
    #自动解决乱码问题
    response.encoding = response
    # print(response.text)

    # 将网页数据结构化
    sel = parsel.Selector(response.text)
    print(sel)
    # 提取出标题
    chapter_title = sel.xpath('//*[@class="page"]/div[4]/h1/text()').get()
    print(chapter_title)

    # 提取内容
    content = sel.xpath('//*[@class="neirong"]/p/text()').getall()
    # print(content)

    chapter_data = []

    for con in content:
        # print(con)
        # str使用replace去除空格
        chapter_data.append(con.replace('\n', ""))
    # print(chapter_data)
    return chapter_title, chapter_data

def wuyou_down_chapter(book_name, chapter_title, content):
    with open(book_name+'.txt', mode='a+', encoding='utf-8') as f:
        f.write("\n\n" + chapter_title + "\n")
        for con in content:
            f.write(con)

def wuyou_get_url_list(url):
    """
    :param url: 传入需要爬取的小说地址
    :return: 响应体
    """
    response = requests.get(url)
    # 自动解决乱码问题
    response.encoding = response.apparent_encoding
    # 将网页数据结构化
    sel = parsel.Selector(response.text)

    # 提取出书名
    book_name = sel.xpath('//*[@class="catalog"]/h1/text()').get()
    # 根据xpath提取每个章节目录地址
    url_list = sel.xpath('//*[@class="mulu-list"]/ul/li/a/@href').getall()

    # print(book_name)
    # print(url_list)

    return book_name, url_list


def wuyou_search_api(book_name):
    search_url = "https://www.51shucheng.net/search?q={}".format(book_name)

    res = requests.get(search_url)  # 进行get请求
    res.encoding = 'utf-8'
    # print(res.text)
    html = etree.HTML(res.text)  # <Element html at 0x7ff3fe0d6108>
    # print(html)

    book_root = html.xpath("//*[@class='search_result']/ul/li")
    # print(etree.tostring(book_root[0]))
    # print(book_root)

    book_list_meesage = []
    for item in book_root:
        book_buf = {}
        book_name = item.xpath("./a/@title")
        # print(book_name)

        book_url = item.xpath("./a/@href")
        # print(book_url)

        book_buf["book_name"] = book_name[0]
        book_buf["book_url"] = book_url[0]
        book_buf["book_user"] = ""
        book_buf["book_size"] = ""

        book_list_meesage.append(book_buf)
        # print(book_buf["book_name"], " : ", book_buf["book_user"], " : ", book_buf["book_size"])
        # print(book_buf["book_url"])
        # print("*********************************************")

    return book_list_meesage
    # get_book(book_url)




if __name__ == '__main__':
    book_url = "https://www.51shucheng.net/jingji/qiongbabafubaba"
    chapter_url = "https://www.51shucheng.net/jingji/qiongbabafubaba/6044.html"
    wuyou_get_chapter(chapter_url)
    # wuyou_get_url_list(book_url)
    # wuyou_search_api("穷")
