from urllib.request import urlretrieve
import os
import threading
from PyQt5.QtWidgets import QApplication,QMainWindow,QTableWidgetItem,QAbstractItemView,QPushButton,QHeaderView,QWidget
from PyQt5.QtCore import pyqtSignal, QObject, Qt
from PyQt5 import uic
import _thread

from preview_ui import *

from book_api.biquge_api import *
from book_api.biquge_2_api import *
from book_api.shuquge_api import *
from book_api.miaojiang_api import *
from book_api.wuyou_book_city_api import *


class preview_widget(QWidget):

    def __init__(self, book_url):
        super().__init__()
        # 连接PyQt5界面文件
        self.ui = Ui_form()
        self.ui.setupUi(self)
        # self.ui = uic.loadUi('preview.ui')

        # 连接界面信号与槽函数
        self.ui.btn_goto.clicked.connect(self.btn_goto_click)
        self.ui.btn_up_chapter.clicked.connect(self.btn_up_chapter_click)
        self.ui.btn_down_chapter.clicked.connect(self.btn_down_chapter_click)
        self.ui.btn_down.clicked.connect(self.btn_down_click)

        self.chapter_num = 0
        self.biquge_flg = "xbiquge"
        self.biquge_2_flg = "5atxt"
        self.shuquge_flg = "shuquge"
        self.miaojiang_flg = "miaojianggushi2"
        self.wuyou_flg = "51shucheng"

        print(book_url)
        self.book_url = book_url
        self.book_name = ""
        self.chapter_url_list = []

        self.ui.label.setText("小说预览")

        # 创建一个搜索小说每一章节网址的线程
        try:
            _thread.start_new_thread(self.get_chapter_url_list, ("get_chapter_url_list", 0))
        except:
            print("Error: 无法启动线程")


        # self.get_chapter_data()

    def get_chapter_url_list(self, name, age):
        self.chapter_url_list = []
        self.book_name = ""
        if self.biquge_flg in self.book_url:
            self.book_name, self.chapter_url_list = biquge_get_url_list(self.book_url)
        if self.biquge_2_flg in self.book_url:
            self.book_name, self.chapter_url_list = biquge_2_get_url_list(self.book_url)
        elif self.shuquge_flg in self.book_url:
            self.book_name, self.chapter_url_list = shuquge_get_url_list(self.book_url)
        elif self.miaojiang_flg in self.book_url:
            self.book_name, self.chapter_url_list = miaojiang_get_url_list(self.book_url)
        elif self.wuyou_flg in self.book_url:
            self.book_name, self.chapter_url_list = wuyou_get_url_list(self.book_url)
        print(self.book_name)
        # 添加书名
        self.ui.label.setText(self.book_name)
        self.get_chapter_data()

    def get_chapter_data(self):
        chapter_title = ""
        chapter_data = ""
        if self.biquge_flg in self.book_url:
            chapter_title, chapter_data = biquge_get_chapter(self.chapter_url_list[self.chapter_num])
        elif self.biquge_2_flg in self.book_url:
            chapter_title, chapter_data = biquge_2_get_chapter(self.chapter_url_list[self.chapter_num])
        elif self.shuquge_flg in self.book_url:
            chapter_title, chapter_data = shuquge_get_chapter(self.chapter_url_list[self.chapter_num])
        elif self.miaojiang_flg in self.book_url:
            chapter_title, chapter_data = miaojiang_get_chapter(self.chapter_url_list[self.chapter_num])
        elif self.wuyou_flg in self.book_url:
            chapter_title, chapter_data = wuyou_get_chapter(self.chapter_url_list[self.chapter_num])

        # print(chapter_title)
        # print(chapter_data)
        self.ui.textBrowser.append(chapter_title)
        for data in chapter_data:
            if data != '\r':
                self.ui.textBrowser.append(data)
        # 显示数据为第一行
        self.ui.textBrowser.moveCursor(self.ui.textBrowser.textCursor().Start)

    """
    跳转到指定的章节
    """
    def btn_goto_click(self):
        if len(self.chapter_url_list) == 0:
            return
        # 从输入框获取需要跳转的章节
        goto_num = self.ui.lineEdit.text()
        if len(goto_num) == 0:
            return
        goto_num = int(goto_num)
        if goto_num < len(self.chapter_url_list) - 1:
            self.chapter_num = goto_num
            self.ui.textBrowser.setText("")
            self.get_chapter_data()
        else:
            self.chapter_num = len(self.chapter_url_list) - 1
            self.ui.textBrowser.setText("")
            self.get_chapter_data()

    def btn_up_chapter_click(self):
        if self.chapter_num > 0:
            self.chapter_num -= 1
            self.ui.textBrowser.setText("")
            self.get_chapter_data()

    def btn_down_chapter_click(self):
        if self.chapter_num < len(self.chapter_url_list) -1:
            self.chapter_num += 1
            self.ui.textBrowser.setText("")
            self.get_chapter_data()

    def btn_down_click(self):
        if len(self.chapter_url_list) == 0:
            return
        # 添加提示
        self.ui.label.setText("从第: {} 章开始下载".format(self.chapter_num))

        # 创建一个下载小说地址，从当前页面到最后一页
        try:
            _thread.start_new_thread(self.down_now_to_end, ("down_now_to_end", 0))
        except:
            print("Error: 无法启动线程")

    def down_now_to_end(self, name, age):
        chapter_title = ""
        chapter_data = ""
        if self.biquge_flg in self.book_url:
            for url in self.chapter_url_list[self.chapter_num:]:
                chapter_title, chapter_data = biquge_get_chapter(url)
                biquge_chapter_down(self.book_name, chapter_title, chapter_data)
        elif self.biquge_2_flg in self.book_url:
            for url in self.chapter_url_list[self.chapter_num:]:
                chapter_title, chapter_data = biquge_2_get_chapter(url)
                biquge_2_chapter_down(self.book_name, chapter_title, chapter_data)
        elif self.shuquge_flg in self.book_url:
            for url in self.chapter_url_list[self.chapter_num:]:
                chapter_title, chapter_data = shuquge_get_chapter(url)
                shuquge_down_chapter(self.book_name, chapter_title, chapter_data)
        elif self.miaojiang_flg in self.book_url:
            for url in self.chapter_url_list[self.chapter_num:]:
                chapter_title, chapter_data = miaojiang_get_chapter(url)
                miaojiang_down_chapter(self.book_name, chapter_title, chapter_data)
        elif self.wuyou_flg in self.book_url:
            for url in self.chapter_url_list[self.chapter_num:]:
                chapter_title, chapter_data = wuyou_get_chapter(url)
                wuyou_down_chapter(self.book_name, chapter_title, chapter_data)

        # 添加提示
        self.ui.label.setText("下载完成: 《{}》".format(self.book_name))