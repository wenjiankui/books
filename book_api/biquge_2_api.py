"""
小说爬取
书趣阁，笔趣阁
苗疆蛊事
"""

buquge_2 = "https://m.5atxt.com/"

import requests
import parsel
from lxml import etree
from tkinter import *


def biquge_2_get_chapter(url):
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

    # 根据css选择器提取标题//*[@id="chaptercontent"]/text()[1]
    chapter_title = sel.xpath('//*[@id="chaptercontent"]/p[2]/text()').get()
    # print(chapter_title)

    # 提取内容
    content = sel.css('#chaptercontent::text').getall()
    # print(content)

    chapter_data = []

    for con in content:
        # print(con)
        if con != '\n\t' and con != '\n  \t':
            # str使用replace去除空格
            chapter_data.append(con.replace('\xa0', ""))

    # print(chapter_title)
    # print(chapter_data)
    if chapter_title is None:
        return "", ""
    return chapter_title, chapter_data
    # book_down(book_name, chapter_title, content)

def biquge_2_chapter_down(book_name, chapter_title, content):
    with open(book_name+'.txt', mode='a+', encoding='utf-8') as f:
        f.write("\n\n" + chapter_title + "\n")
        for con in content:
            # print(con)
            f.write(con)


def biquge_2_get_url_list(url):
    """
    :param url: 传入需要爬取的网站
    :return: 响应体
    """
    response = requests.get(url)
    # 自动解决乱码问题
    response.encoding = response.apparent_encoding
    # 将网页数据结构化
    sel = parsel.Selector(response.text)
    # print(sel)

    # 提取出书名//*[@id="top"]/span
    book_name = sel.xpath('//*[@id="top"]/span/text()').get()
    # print(book_name)

    # 根据xpath提取每个章节目录地址
    index = sel.xpath('//*[@id="chapterlist"]/p/a/@href').getall()
    del index[0]
    # print(index)

    url_list = []
    # 前12个地址为最新章节地址，有重复，去除掉
    for i in index:
        get_url = "https://m.5atxt.com" + i
        # print(get_url)
        url_list.append(get_url)
        get_url = "https://m.5atxt.com" + i.split('.')[0] + "_2.html"
        # print(get_url)
        url_list.append(get_url)
        get_url = "https://m.5atxt.com" + i.split('.')[0] + "_3.html"
        # print(get_url)
        url_list.append(get_url)
        # get_chapter(book_name, url)
    return book_name, url_list


def biquge_2_search_api(book_name):
    search_url = "https://m.5atxt.com/SearchBook.php"
    data = {
        'keyword': book_name
    }
    # print(data)
    res = requests.post(search_url, data)  # 进行post请求
    res.encoding = 'utf-8'
    # print(res.text)

    html = etree.HTML(res.text)  # <Element html at 0x7ff3fe0d6108>
    # print(html)
    # print(etree.tostring(html))


    book_root = html.xpath("/html/body/div/div/div/div")
    # print(book_root)
    # print(etree.tostring(book_root[0]))

    if len(book_root) == 0:
        return[]
    book_list = book_root[0].xpath("./div")

    # print(book_list)
    print(etree.tostring(book_list[0]))

    if len(book_list) == 0:                # 搜索结果为空时
        return []

    book_user_list = book_list[0].xpath("//*[@class='author']/a/text()")
    # print(book_user_list)

    num = 0
    book_list_meesage = []

    for item in book_list:
        book_buf = {}
        # str使用replace去除空格
        book_buf["book_name"] = item.xpath("./a/p/text()")[0].replace("\r\n","").replace("\t","").strip()

        book_url_id = item.xpath("./a/@href")[0].replace("\r\n","").replace("\t","").strip()
        book_buf["book_url"] = "https://m.5atxt.com" + book_url_id.replace(".html","")


        book_buf["book_user"] = book_user_list[num].replace("\r\n","").replace("\t","").strip()
        num += 1
        book_buf["book_size"] = book_user_list[num].replace("\r\n","").replace("\t","").strip()
        num += 1

        book_list_meesage.append(book_buf)

        # print(book_buf["book_name"], " : ", book_buf["book_user"], " : ", book_buf["book_size"])
        # print(book_buf["book_url"])
        # print("*********************************************")
    return book_list_meesage
    # get_book(book_list_meesage[0]["book_url"])




if __name__ == '__main__':
    url = "https://m.5atxt.com/wapbook/6498_18951013_2.html"
    # get_book(url)
    # biquge_2_search_api("斗破苍穹")
    # biquge_2_get_url_list(url)
    biquge_2_get_chapter(url)
