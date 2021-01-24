"""
小说下载工具

辰良

1968967834@qq.com

CSDN地址：https://blog.csdn.net/qq_39025957

2020年12月21日

"""


from urllib.request import urlretrieve
import os
import threading
from PyQt5.QtWidgets import QApplication,QMainWindow,QTableWidgetItem,QAbstractItemView,QPushButton,QHeaderView,QWidget
from PyQt5.QtCore import pyqtSignal, QObject, Qt
from PyQt5 import uic
import _thread
from main_ui import *

from book_api.biquge_api import *
from book_api.shuquge_api import *
from book_api.miaojiang_api import *
from book_api.biquge_2_api import *
from book_api.wuyou_book_city_api import *
from preview import *






# 信号类，更新QWidget_table
class mysignal(QObject):
    up_widget = pyqtSignal(object, int)

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        # 连接PyQt5界面文件
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        #self.ui = uic.loadUi('main.ui')

        # 连接界面信号与槽函数
        self.ui.btn_search.clicked.connect(self.btn_search_click)

        # 下载保存的路径为：当前软件运行的目录下的"book"文件中，
        # self.down_load_addr = "./book"
        # if not os.path.exists(self.down_load_addr):  # 判断一个目录是否存在
        #     os.makedirs(self.down_load_addr)  # 多层创建目录

        # 搜索结果存放列表，包含歌名，歌手，时长，id, 下载地址
        self.biquge_book_list_meesage = []
        self.biquge_2_book_list_meesage = []
        self.shuquge_book_list_meesage = []
        self.miaojiang_book_list_meesage = []
        self.wuyou_book_list_meesage = []
        # 启动搜索标志
        self.biquge_search_flag = 0
        self.biquge_2_search_flag = 0
        self.shuquge_search_flag = 0
        self.miaojiang_search_flag = 0
        self.wuyou_search_flag = 0

        # 开始写入表格标志
        self.up_table_widget_flag = 0
        self.biquge_up_table_flag = 0
        self.biquge_2_up_table_flag = 0
        self.shuquge_up_table_flag = 0
        self.miaojiang_up_table_flag = 0
        self.wuyou_up_table_flag = 0

        # 需要更新的table_widget控件名
        self.table_widget_list = []
        # 当前需要更新的列表行号
        self.run_count = 0



        # 循环初始化每一个table_widget控件
        tablewidget_list = [self.ui.tableWidget_biquge, self.ui.tableWidget_biquge_2, self.ui.tableWidget_shuquge, self.ui.tableWidget_miaojiang, self.ui.tableWidget_wuyou]
        for item in tablewidget_list:
            # 设置4列1行
            item.setColumnCount(4)
            item.setRowCount(0)
            # 设置控件为只读，不允许修改
            item.setEditTriggers(QAbstractItemView.NoEditTriggers)
            # 设置为整行选中方式
            item.setSelectionBehavior(QAbstractItemView.SelectRows)
            # 设置单选目标
            item.setSelectionMode(QAbstractItemView.SingleSelection)
            # 设置不显示格子线
            item.setShowGrid(False)
            # 设置列内容自适应宽度
            item.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            item.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            # 设置双击触发
            item.cellDoubleClicked.connect(self.table_widget_clicked)
            # 设置单击触发
            # item.itemClicked.connect(self.Select)

        # 创建所有线程
        self.build_thread()

        # 实例化触发更新table widget信号
        self.up_table_widget_sig = mysignal()
        self.up_table_widget_sig.up_widget.connect(self.up_table_widget)

        # 创建定时器线程，用于检测更新界面
        self.timer = threading.Timer(1, self.time_up_table_widgt)
        self.timer.start()  # 启动定时器
        # self.timer.cancel()  # 取消定时器

        self.preview = ""
        """
        # 设置控件透明度
        op = QtWidgets.QGraphicsOpacityEffect()
        op.setOpacity(0.8)
        self.ui.tableWidget_biquge.setGraphicsEffect(op)
        self.ui.tableWidget_biquge.setAutoFillBackground(True)
        """



    # 创建所有的线程
    def build_thread(self):

        # 创建一个笔趣阁搜索线程
        try:
            _thread.start_new_thread(self.biquge_search_book, ("biquge_search_book", 0))
        except:
            print("Error: 无法启动线程")
        # 创建一个笔趣阁_2搜索线程
        try:
            _thread.start_new_thread(self.biquge_2_search_book, ("biquge_2_search_book", 0))
        except:
            print("Error: 无法启动线程")
        # 创建一个书趣阁搜索线程
        try:
            _thread.start_new_thread(self.shuquge_search_book, ("shuquge_search_book", 0))
        except:
            print("Error: 无法启动线程")
        # 创建一个苗疆搜索线程
        try:
            _thread.start_new_thread(self.miaojiang_search_book, ("miaojiang_search_book", 0))
        except:
            print("Error: 无法启动线程")
        # 创建一个无忧书城搜索线程
        try:
            _thread.start_new_thread(self.wuyou_search_book, ("wuyou_search_book", 0))
        except:
            print("Error: 无法启动线程")


    """
    点击下载按钮触发的槽函数
    row : 需要下载的小说在列表中的行号
    table_type : 下载按钮所在的table_widget
    """
    def btn_down_click(self,row, table_type):
        # print(row)
        # 根据列表行号和控件名称获取对应的小说url和小说名称
        book_url, book_name = self.object_to_url_name(row, table_type)
        if len(book_name) == 0 or len(book_url) == 0:
            return
        # 创建一个下载线程
        try:
            _thread.start_new_thread(self.down_book, ("down_book", book_name, book_url))
        except:
            print("Error: 无法启动线程")

    # 根据列表行号和控件名称获取对应的书籍url和书籍名称
    def object_to_url_name(self, row, table_type):
        table_name = table_type.objectName()
        # print(table_name)

        if table_name == "tableWidget_biquge":
            book_url = self.biquge_book_list_meesage[row]["book_url"]
            book_name = self.biquge_book_list_meesage[row]["book_name"] + ' - ' + self.biquge_book_list_meesage[row][
                            "book_user"]
        elif table_name == "tableWidget_biquge_2":
            book_url = self.biquge_2_book_list_meesage[row]["book_url"]
            book_name = self.biquge_2_book_list_meesage[row]["book_name"] + ' - ' + self.biquge_2_book_list_meesage[row][
                            "book_user"]
        elif table_name == "tableWidget_shuquge":
            book_url = self.shuquge_book_list_meesage[row]["book_url"]
            book_name = self.shuquge_book_list_meesage[row]["book_name"] + ' - ' + self.shuquge_book_list_meesage[row][
                "book_user"]
        elif table_name == "tableWidget_miaojiang":
            book_url = self.miaojiang_book_list_meesage[row]["book_url"]
            book_name = self.miaojiang_book_list_meesage[row]["book_name"] + ' - ' + self.miaojiang_book_list_meesage[row][
                "book_user"]
        elif table_name == "tableWidget_wuyou":
            book_url = self.wuyou_book_list_meesage[row]["book_url"]
            book_name = self.wuyou_book_list_meesage[row]["book_name"] + ' - ' + self.wuyou_book_list_meesage[row][
                "book_user"]
        else:
            book_name = ""
            book_url = ""
        return book_url, book_name
    """
    table_widget 双击触发的槽函数
    row : 点击的行号
    column : 点击的列号
    """
    def table_widget_clicked(self,row,column):
        # print(row, " : ", column)
        # print(self.sender().objectName())
        
        # 根据列表行号和控件名称获取对应的小说url和小说名称
        book_url, book_name = self.object_to_url_name(row, self.sender())

        if len(book_name) == 0 or len(book_url) == 0:
            return

        self.preview = preview_widget(book_url)
        self.preview.show()



    # 根据搜索的小说名称，找到搜索结果
    def btn_search_click(self):
        # 从输入框获取需要搜索的小说名
        search_name = self.ui.lineEdit.text()
        if len(search_name) == 0:
            return
        # 添加提示
        self.ui.label.setText("正在搜索: 《{}》...".format(search_name))
        # 参数复位
        self.table_widget_list = []
        self.up_table_widget_flag = 0
        self.biquge_up_table_flag = 0
        self.biquge_2_up_table_flag = 0
        self.shuquge_up_table_flag = 0
        self.miaojiang_up_table_flag = 0
        self.wuyou_up_table_flag = 0


        # 启动搜索标志
        self.biquge_search_flag = 1
        self.biquge_2_search_flag = 1
        self.shuquge_search_flag = 1
        self.miaojiang_search_flag = 1
        self.wuyou_search_flag = 1


    def biquge_search_book(self, name, age):
        while 1:
            if self.biquge_search_flag:
                search_name = self.ui.lineEdit.text()
                self.biquge_book_list_meesage = biquge_search_api(search_name)
                self.biquge_search_flag = 0
                self.biquge_up_table_flag = 1
                self.up_table_widget_flag = 1
                print("笔趣阁搜索完成")

    def biquge_2_search_book(self, name, age):
        while 1:
            if self.biquge_search_flag:
                search_name = self.ui.lineEdit.text()
                self.biquge_2_book_list_meesage = biquge_2_search_api(search_name)
                self.biquge_2_search_flag = 0
                self.biquge_2_up_table_flag = 1
                self.up_table_widget_flag = 1
                print("笔趣阁_2搜索完成")

    def shuquge_search_book(self, name, age):
        while 1:
            if self.shuquge_search_flag:
                search_name = self.ui.lineEdit.text()
                self.shuquge_book_list_meesage = shuquge_search_api(search_name)
                self.shuquge_search_flag = 0
                self.shuquge_up_table_flag = 1
                self.up_table_widget_flag = 1
                print("书趣阁搜索完成")

    def miaojiang_search_book(self, name, age):
        while 1:
            if self.miaojiang_search_flag:
                search_name = self.ui.lineEdit.text()
                self.miaojiang_book_list_meesage = miaojiang_search_api(search_name)
                self.miaojiang_search_flag = 0
                self.miaojiang_up_table_flag = 1
                self.up_table_widget_flag = 1
                print("苗疆搜索完成")

    def wuyou_search_book(self, name, age):
        while 1:
            if self.wuyou_search_flag:
                search_name = self.ui.lineEdit.text()
                self.wuyou_book_list_meesage = wuyou_search_api(search_name)
                self.wuyou_search_flag = 0
                self.wuyou_up_table_flag = 1
                self.up_table_widget_flag = 1
                print("无忧书城搜索完成")


    """
    根据控件名返回对应的小说列表
    table_type : 控件名
    """
    def object_to_book_list(self, table_type):
        # 将table_type 转换为 objectName()
        table_name = table_type.objectName()
        if table_name == "tableWidget_biquge":
            return self.biquge_book_list_meesage
        if table_name == "tableWidget_biquge_2":
            return self.biquge_2_book_list_meesage
        elif table_name == "tableWidget_shuquge":
            return self.shuquge_book_list_meesage
        elif table_name == "tableWidget_miaojiang":
            return self.miaojiang_book_list_meesage
        elif table_name == "tableWidget_wuyou":
            return self.wuyou_book_list_meesage
        else:
            return ""

    # 定时器触发函数，更新table_widget界面显示
    def time_up_table_widgt(self):
        # 当有搜索完成标志时，向table_widget_list添加对应的控件名，等待小说信息写入对应控件
        if self.biquge_up_table_flag:
            self.table_widget_list.append(self.ui.tableWidget_biquge)
            self.biquge_up_table_flag = 0
        elif self.biquge_2_up_table_flag:
            self.table_widget_list.append(self.ui.tableWidget_biquge_2)
            self.biquge_2_up_table_flag = 0
        elif self.shuquge_up_table_flag:
            self.table_widget_list.append(self.ui.tableWidget_shuquge)
            self.shuquge_up_table_flag = 0
        elif self.miaojiang_up_table_flag:
            self.table_widget_list.append(self.ui.tableWidget_miaojiang)
            self.miaojiang_up_table_flag = 0
        elif self.wuyou_up_table_flag:
            self.table_widget_list.append(self.ui.tableWidget_wuyou)
            self.wuyou_up_table_flag = 0


        # 如果更新table_widget标志和self.table_widget_list列表不为空，则向up_table_widget发送信号
        if self.up_table_widget_flag == 1 and len(self.table_widget_list) != 0:
            # print(self.run_count)
            # 发送更新信号，并附带需要更新的控件名和列表行号
            self.up_table_widget_sig.up_widget.emit(self.table_widget_list[0], self.run_count)

            book_list = self.object_to_book_list(self.table_widget_list[0])
            if self.run_count < len(book_list)-1:
                self.run_count += 1
            else:
                # print(self.table_widget_list)
                self.run_count = 0
                # 如果更新列表不为空，则删除第一个元素
                if len(self.table_widget_list):
                    del self.table_widget_list[0]

                # 如果更新列表不为空，则继续更新下一个控件，否则停止更新
                if len(self.table_widget_list) == 0:
                    self.up_table_widget_flag = 0
                    self.ui.label.setText("搜索完成")
                else:
                    self.up_table_widget_flag = 1

        # print(datetime.datetime.utcnow().strftime('%Y-%m-%d%H:%M:%S'))  # 测试定时器响应时间
        self.timer = threading.Timer(0.3, self.time_up_table_widgt)  # 创建一个定时任务，每0.3秒启动一次
        self.timer.start()  # 启动定时器

    """
    更新table_widget界面显示
    table_type : table_widget控件名
    row : 添加第几行
    """
    def up_table_widget(self, table_type, row):
        self.up_table_widget_flag = 0
        # num = 0
        # table_type.setRowCount(0)
        # table_type.clearContents()
        # print(datetime.datetime.now())

        # 根据要操作的控件名，获取对应的小说列表
        book_list = self.object_to_book_list(table_type)
        # 如果小说列表为空，说明搜索结果为空，清空该控件，并返回
        if len(book_list) == 0:
            self.up_table_widget_flag = 1
            table_type.setRowCount(0)  # 清空table显示
            return

        # 如果写入的行号大于小说列表的的长度，说明该行号不可用，
        if len(book_list) <= row:
            # print(len(book_list), " ： ", row)
            self.up_table_widget_flag = 1
            return

        # 向控件添加一行小说信息
        book_list = book_list[row]
        # print(book_list)
        table_type.setRowCount(row + 1)  # 总行数增加1
        table_type.setItem(row, 0, QTableWidgetItem(book_list["book_name"]))
        table_type.setItem(row, 1, QTableWidgetItem(book_list["book_user"]))
        table_type.setItem(row, 2, QTableWidgetItem(book_list["book_size"]))
        btn_down = QPushButton("下载")
        # 将按钮点击事件链接btn_down_click，在点击时，附带row_n, column参数传递，
        btn_down.clicked.connect(lambda state, row_n=row, column=table_type: self.btn_down_click(row_n, column))
        # 将按钮添加至table_widget
        table_type.setCellWidget(row, 3, btn_down)

        self.up_table_widget_flag = 1
        # self.up_table_widget_flag = 0

        # num += 1
        # print(datetime.datetime.now())


    """
    根据书名和url下载书籍，每一本书籍的下载，都是一个新的线程
    name : 线程名称
    book_name : 书籍名称
    book_url : 书籍下载的url
    """
    def down_book(self, name, book_name, book_url):
        if len(book_url) == 0:
            return
        self.biquge_flg = "xbiquge"
        self.biquge_2_flg = "5atxt"
        self.shuquge_flg = "shuquge"
        self.miaojiang_flg = "miaojianggushi2"
        self.wuyou_flg = "51shucheng"
        print(book_name, " : ", book_url)
        # 添加提示
        self.ui.label.setText("正在下载: 《{}》...".format(book_name))
        # 下载保存
        if self.biquge_flg in book_url:
            book_name, url_list = biquge_get_url_list(book_url)
            for url in url_list:
                chapter_title, chapter_data = biquge_get_chapter(url)
                biquge_chapter_down(book_name, chapter_title, chapter_data)
        if self.biquge_2_flg in book_url:
            book_name, url_list = biquge_2_get_url_list(book_url)
            for url in url_list:
                chapter_title, chapter_data = biquge_2_get_chapter(url)
                biquge_2_chapter_down(book_name, chapter_title, chapter_data)
        elif self.shuquge_flg in book_url:
            book_name, url_list = shuquge_get_url_list(book_url)
            for url in url_list:
                chapter_title, chapter_data = shuquge_get_chapter(url)
                shuquge_down_chapter(book_name, chapter_title, chapter_data)
        elif self.miaojiang_flg in book_url:
            book_name, url_list = miaojiang_get_url_list(book_url)
            for url in url_list:
                chapter_title, chapter_data = miaojiang_get_chapter(url)
                miaojiang_down_chapter(book_name, chapter_title, chapter_data)
        elif self.wuyou_flg in book_url:
            book_name, url_list = wuyou_get_url_list(book_url)
            for url in url_list:
                chapter_title, chapter_data = wuyou_get_chapter(url)
                wuyou_down_chapter(book_name, chapter_title, chapter_data)
            
        # 添加提示
        self.ui.label.setText("下载完成: 《{}》".format(book_name))

    # 重载键盘回车
    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == Qt.Key_Return:
            # print('Space')
            self.btn_search_click()

    # 重载qt窗体关闭函数
    def closeEvent(self, event):
        print("window close")
        self.close()
        event.accept()
        os._exit(0)


if __name__ == '__main__':
    app = QApplication([])
    stats = MainWindow()
    stats.show()

    sys.exit(app.exec_())

    """
    app = QApplication([])
    stats = MainWindow()
    stats.ui.show()
    app.exec_()
    """


