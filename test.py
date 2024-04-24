# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'test.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################
import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui
from matplotlib.backends.backend_qt import MainWindow

import test  # 导入QtTest文件
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                            QMetaObject, QObject, QPoint, QRect,
                            QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
                           QFont, QFontDatabase, QGradient, QIcon,
                           QImage, QKeySequence, QLinearGradient, QPainter,
                           QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow, QMenuBar,
                               QPushButton, QSizePolicy, QStatusBar, QWidget)


class testapp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.flag = 0
        self.__ui = Ui_MainWindow()
        self.__ui.setupUi(self)
        self.__ui.pushButton.clicked.connect(self.switchbutton)

    def switchbutton(self):
        if self.flag == 0:
            self.flag += 1
            self.__ui.pushButton.setText("Close")
        else:
            self.flag = 0
            self.__ui.pushButton.setText("Open")

    def closewindow(self):
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"close", None))


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(629, 473)
        icon = QIcon(QIcon.fromTheme(u"system-run"))
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(260, 310, 75, 24))
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(160, 90, 331, 181))
        font = QFont()
        font.setFamilies([u"\u5fae\u8f6f\u96c5\u9ed1"])
        font.setPointSize(36)
        font.setBold(True)
        self.label.setFont(font)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 629, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Test Page", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Hello World", None))
    # retranslateUi


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    window = testapp()
    window.show()

    sys.exit(app.exec())
