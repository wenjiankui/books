"""
小说爬取
书趣阁，笔趣阁
苗疆蛊事
"""

miaojiang = "https://www.miaojianggushi2.com"

import requests
import parsel
from lxml import etree
from tkinter import *


def miaojiang_get_chapter(url):
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
    chapter_title = sel.xpath('//div[@class="panel-footer col-md-12"]/h1/text()').get()
    content = sel.xpath('//div[@id="content"]/text()').getall()

    chapter_data = []
    # 去掉最后三行
    for con in content[1:-2]:
        # print(con)
        # str使用replace去除空格
        chapter_data.append(con.replace('\xa0', "") + "\n")

    print(chapter_title)
    return chapter_title, chapter_data

def miaojiang_down_chapter(book_name, chapter_title, content):
    with open(book_name+'.txt', mode='a+', encoding='utf-8') as f:
        f.write("\n\n" + chapter_title + "\n")
        # 去掉第一行和最后三行
        for con in content:
            f.write(con)

def miaojiang_get_url_list(url):
    """
    :param url: 传入需要爬取的网站
    :return: 响应体
    """
    response = requests.get(url)
    # 自动解决乱码问题
    response.encoding = response.apparent_encoding
    # 将网页数据结构化
    sel = parsel.Selector(response.text)


    book_name = sel.xpath('//div[@class="panel-heading"]/h1/text()').get()
    index = sel.xpath('//ul[@class="list-group"]/li/a/@href').getall()

    print(book_name)
    url_list = []
    for i in index:
        # print(url[:31] + i)
        # get_chapter(book_name, url[:31] + i)
        url_list.append(url[:31] + i)

    return book_name, url_list

def miaojiang_search_api(book_name):
    search_url = "https://www.miaojianggushi2.com/search?key={}".format(book_name)
    res = requests.get(search_url)  # 进行post请求
    res.encoding = 'utf-8'
    # print(res.text)
    html = etree.HTML(res.text)  # <Element html at 0x7ff3fe0d6108>
    # print(html)

    book_list = html.xpath("//*[@class='row']/div/table/tbody/tr")
    # print(book_list)
    # print(etree.tostring(book_list[0]))


    # book_list = book_root[0].xpath("//*[@class='bookbox']")
    # print(book_list)

    book_list_meesage = []
    i = 0
    for item in book_list:
        book_buf = {}
        book_message = item.xpath("./td/a/text()")
        # print(book_message)


        book_id = item.xpath("./td/a/@href")[0]
        # print(book_id)

        book_buf["book_name"] = book_message[0]
        book_buf["book_url"] = "https://www.miaojianggushi2.com" + book_id
        book_buf["book_user"] = book_message[2]
        book_buf["book_size"] = book_message[1]

        i += 1
        book_list_meesage.append(book_buf)
        # print(book_buf["book_name"], " : ", book_buf["book_user"], " : ", book_buf["book_size"])
        # print(book_buf["book_url"])
        # print("*********************************************")

    return book_list_meesage


    # get_book(book_list_meesage[0]["book_url"])




if __name__ == '__main__':
    url = "http://www.shuquge.com/txt/72929/index.html"
    # get_book(url)
    # miaojiang_search_api("斗罗大陆")
