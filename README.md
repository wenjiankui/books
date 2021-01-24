# books
多网爬取小说下载工具

## 系统环境

python3.7

Pycharm2019.3.3

Windows10x64

## 文件结构分析

main.py

主文件，程序入口文件，

包含以下内容：

​	1、小说搜索窗口qt界面调用

​	2、界面控件设置相关属性，并连接槽函数

​	3、小说整本下载

​	4、小说多平台搜索结果显示列表

preview.py

小说内容预览窗口

包含以下内容：

​	1、小说预览窗口qt界面调用

​	2、小说预览章节跳转

​	3、小说从当前页开始下载

main.ui（由QT界面生成软件：”designer.exe“ 生成的界面文件）

main_ui.py（由 “main.ui” 文件转化为python文件）

preview.ui（由QT界面生成软件：”designer.exe“ 生成的界面文件）

preview_ui.py（由 “preview.ui” 文件转化为python文件）

dist 文件夹（编译成功的软件，可执行程序）

book_api文件夹

包含以下内容：

​	1、biquge_api.py：笔趣阁网页小说爬取（http://www.biquge.info/）

​	2、biquge_2_api.py：新版笔趣阁网页小说爬取（https://m.5atxt.com/）

​	3、miaojiang_api.py：苗疆蛊事网页小说爬取（https://www.miaojianggushi2.com/）

​	4、shuquge_api.py：书趣阁网页小说爬取（http://www.shuquge.com/）

​	5、wuyou_book_city_api.py：无忧书城网页小说爬取（https://www.51shucheng.net/）





## python模块安装

```python
pip install threading	# 创建线程
pip install PyQt5		# 调用qt界面
pip install PyQt5-tools	# qt界面附带工具
pip install pyinstalle	# 将python文件打包为.exe可执行文件
pip install requsts		# 网络请求

```

