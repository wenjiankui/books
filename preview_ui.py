# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'preview.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_form(object):
    def setupUi(self, form):
        form.setObjectName("form")
        form.resize(777, 537)
        self.gridLayout = QtWidgets.QGridLayout(form)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit = QtWidgets.QLineEdit(form)
        self.lineEdit.setMaximumSize(QtCore.QSize(100, 16777215))
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.btn_goto = QtWidgets.QPushButton(form)
        self.btn_goto.setObjectName("btn_goto")
        self.horizontalLayout.addWidget(self.btn_goto)
        self.btn_down = QtWidgets.QPushButton(form)
        self.btn_down.setObjectName("btn_down")
        self.horizontalLayout.addWidget(self.btn_down)
        self.label = QtWidgets.QLabel(form)
        self.label.setMinimumSize(QtCore.QSize(200, 0))
        self.label.setText("")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.btn_up_chapter = QtWidgets.QPushButton(form)
        self.btn_up_chapter.setObjectName("btn_up_chapter")
        self.horizontalLayout.addWidget(self.btn_up_chapter)
        self.btn_down_chapter = QtWidgets.QPushButton(form)
        self.btn_down_chapter.setObjectName("btn_down_chapter")
        self.horizontalLayout.addWidget(self.btn_down_chapter)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.textBrowser = QtWidgets.QTextBrowser(form)
        self.textBrowser.setStyleSheet("font: 12pt \"Agency FB\";")
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout.addWidget(self.textBrowser, 1, 0, 1, 1)

        self.retranslateUi(form)
        QtCore.QMetaObject.connectSlotsByName(form)

    def retranslateUi(self, form):
        _translate = QtCore.QCoreApplication.translate
        form.setWindowTitle(_translate("form", "小说预览"))
        self.btn_goto.setText(_translate("form", "跳转"))
        self.btn_down.setText(_translate("form", "下载"))
        self.btn_up_chapter.setText(_translate("form", "上一章"))
        self.btn_down_chapter.setText(_translate("form", "下一章"))
