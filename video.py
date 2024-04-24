# -*- coding: utf-8 -*-
import sys

################################################################################
## Form generated from reading UI file 'video.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                            QMetaObject, QObject, QPoint, QRect,
                            QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
                           QCursor, QFont, QFontDatabase, QGradient,
                           QIcon, QImage, QKeySequence, QLinearGradient,
                           QPainter, QPalette, QPixmap, QRadialGradient,
                           QTransform)
from PySide6.QtWidgets import (QApplication, QGraphicsView, QLabel, QMainWindow,
                               QMenu, QMenuBar, QPushButton, QSizePolicy,
                               QStatusBar, QWidget)
#from PyQt5 import QtGui,QtWidgets,QtCore
from pyqt5_plugins.examplebutton import QtWidgets


class testapp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.flag = 0
        self.__ui = Ui_MainWindow()
        self.__ui.setupUi(self)
        self.__ui.pushButton.clicked.connect(self.switchbutton())
        self.__ui.pushButton_2.clicked.connect(self.closewindow())

    def switchbutton(self):
        if self.flag == 0:
            self.flag += 1
            self.__ui.pushButton.setText("Close")
        else:
            self.flag = 0
            self.__ui.pushButton.setText("Open")

    def closewindow(self):
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"close", None))

    def sipPyTypeDictRef(self):
        return super().sipPyTypeDictRef()


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.graphicsView = QGraphicsView(self.centralwidget)
        self.graphicsView.setObjectName(u"graphicsView")
        self.graphicsView.setGeometry(QRect(30, 60, 421, 271))
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(100, 360, 75, 24))
        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(320, 360, 75, 24))
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(70, 30, 351, 21))
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(30, 360, 61, 16))
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(210, 360, 49, 16))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        self.menuOption = QMenu(self.menubar)
        self.menuOption.setObjectName(u"menuOption")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuOption.menuAction())
        self.menuOption.addAction(self.actionExit)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.label.setText(
            QCoreApplication.translate("MainWindow", u"PythonApplication_Opencv_Fatigue_Detection_Algorithm_torch",
                                       None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Cam Status", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Closed", None))
        self.menuOption.setTitle(QCoreApplication.translate("MainWindow", u"Option", None))
    # retranslateUi


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    MainWindow = testapp()
    MainWindow.show()

    sys.exit(app.exec())
