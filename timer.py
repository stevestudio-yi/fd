# -*- coding: utf-8 -*-
import sys

################################################################################
## Form generated from reading UI file 'timer.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                            QMetaObject, QObject, QPoint, QRect,
                            QSize, QTime, QUrl, Qt, QTimer)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
                           QFont, QFontDatabase, QGradient, QIcon,
                           QImage, QKeySequence, QLinearGradient, QPainter,
                           QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow, QMenuBar,
                               QPushButton, QSizePolicy, QStatusBar, QWidget)


class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.freq = 0
        self.clic = 0
        self.circle = 0
        self.ttc = 0
        self.setupUi(self)
        self.retranslateUi(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.timecount)

    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(160, 210, 75, 23))

        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(280, 210, 75, 23))

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(170, 150, 53, 15))
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(280, 150, 53, 15))
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(390, 150, 53, 15))
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(480, 150, 91, 16))
        self.pushButton_3 = QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QRect(450, 210, 75, 23))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.timer = QTimer(self)
        self.pushButton.clicked.connect(self.on_start_clicked)
        self.pushButton_2.clicked.connect(self.on_stop_clicked)
        self.pushButton_3.clicked.connect(self.on_tap_clicked)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def on_start_clicked(self):
        self.ttc = 0
        self.circle = 0
        self.timer.stop()
        self.timer.start(1000)

        self.label_2.setText(f"{self.ttc}秒")

    def on_tap_clicked(self):
        self.clic = self.clic + 1
    def on_stop_clicked(self):
        self.ttc = 0
        self.timer.stop()
        self.label_2.setText("计时已停止")

    def timecount(self):
        self.ttc = self.ttc + 1
        self.label_2.setText(f"{self.ttc}秒")
        if self.ttc == 10:
            self.circle = self.circle + 1
            self.label_3.setText(f"循环{self.circle}次")
            self.freq = self.clic / 10
            self.label_4.setText(f"点击频率为{self.freq}")
            self.ttc = 0
            self.clic = 0

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"start", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"stop", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u8ba1\u65f6", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"loading", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u5faa\u73af\u6b21\u6570", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u6bcf1\u79d2\u70b9\u51fb\u6b21\u6570", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"\u70b9\u51fb", None))

    # retranslateUi


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.show()
    sys.exit(app.exec_())
