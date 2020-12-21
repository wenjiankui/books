"""
小说爬取
书趣阁，笔趣阁
苗疆蛊事
"""

miaojiang = "https://www.miaojianggushi2.com"
shuquge = "http://www.shuquge.com"

import requests
import parsel
from lxml import etree
from tkinter import *


def biquge_get_chapter(url):
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

    # 根据css选择器提取标题
    chapter_title = sel.css('div.bookname > h1::text').get()
    # 提取内容
    content = sel.css('#content::text').getall()

    chapter_data = []
    # 去掉最后三行
    for con in content:
        # print(con)
        # str使用replace去除空格
        chapter_data.append(con.replace('\xa0', ""))

    # print(chapter_title)
    if chapter_title is None:
        return "", ""
    return chapter_title, chapter_data
    # book_down(book_name, chapter_title, content)

def biquge_chapter_down(book_name, chapter_title, content):
    with open(book_name+'.txt', mode='a+', encoding='utf-8') as f:
        f.write("\n\n" + chapter_title + "\n")
        for con in content:
            # print(con)
            # str使用replace去除空格
            f.write(con)


def biquge_get_url_list(url):
    """
    :param url: 传入需要爬取的网站
    :return: 响应体
    """
    response = requests.get(url)
    # 自动解决乱码问题
    response.encoding = response.apparent_encoding
    # 将网页数据结构化
    sel = parsel.Selector(response.text)


    # 提取出书名
    book_name = sel.xpath('//div[@id="info"]/h1/text()').get()
    # 根据xpath提取每个章节目录地址
    index = sel.xpath('//*[@id="list"]/dl/dd').getall()

    # print(book_name)
    url_list = []
    # 前12个地址为最新章节地址，有重复，去除掉
    for i in index:
        get_url = "http://www.xbiquge.la" + re.match(r'(.*)"(.*?)".*', i).group(2)
        url_list.append(get_url)
        # get_chapter(book_name, url)
    return book_name, url_list


def biquge_search_api(book_name):
    search_url = "http://www.xbiquge.la/modules/article/waps.php"
    data = {
        'searchkey': book_name
    }
    # print(data)
    res = requests.post(search_url, data)  # 进行post请求
    res.encoding = 'utf-8'
    # print(res.text)
    html = etree.HTML(res.text)  # <Element html at 0x7ff3fe0d6108>
    # print(html)
    # print(etree.tostring(html))


    book_root = html.xpath("//*[@class='grid']")
    # print(book_root)
    # print(etree.tostring(book_root[0]))

    book_list = book_root[0].xpath("./tr")
    del book_list[0]
    # print(book_list)
    # print(etree.tostring(book_list[0]))

    if len(book_list) == 0:                # 搜索结果为空时
        return []

    book_url_list = book_list[0].xpath("./td/a/@href")[0]
    # print(book_url_list)

    book_message = book_list[0].xpath("./td/a/text()")
    # print(book_message)

    book_user_list = book_list[0].xpath("./td/text()")[1]
    # print(book_user_list)

    book_list_meesage = []

    for item in book_list:
        book_buf = {}
        book_buf["book_name"] = item.xpath("./td/a/text()")[0]
        book_buf["book_url"] = item.xpath("./td/a/@href")[0]
        book_buf["book_user"] = item.xpath("./td/text()")[1]
        book_buf["book_size"] = item.xpath("./td/a/text()")[1]

        book_list_meesage.append(book_buf)

        # print(book_buf["book_name"], " : ", book_buf["book_user"], " : ", book_buf["book_size"])
        # print(book_buf["book_url"])
        # print("*********************************************")
    return book_list_meesage
    # get_book(book_list_meesage[0]["book_url"])




if __name__ == '__main__':
    url = "http://www.biquge.info/3_3214/"
    # get_book(url)
    # biquge_search_api("帝霸")
