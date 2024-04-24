# -*- coding: utf-8 -*-
import sys
# noinspection PyUnresolvedReferences
import time
import cv2
import dlib
import torchvision
import math
import numpy as np
import threading
from copy import deepcopy
from torchvision.models.detection import KeypointRCNN_ResNet50_FPN_Weights
# Form generated from reading UI file 'New.ui'
#
# Created by: Qt User Interface Compiler version 6.5.2
#
# WARNING! All changes made in this file will be lost when recompiling UI file!
#
#目前Main

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                            QMetaObject, QObject, QPoint, QRect,
                            QSize, QTime, QUrl, Qt, QTimer)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
                           QCursor, QFont, QFontDatabase, QGradient,
                           QIcon, QImage, QKeySequence, QLinearGradient,
                           QPainter, QPalette, QPixmap, QRadialGradient,
                           QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow, QMenu,
                               QMenuBar, QPushButton, QSizePolicy, QStatusBar,
                               QTextEdit, QWidget, QFrame)

# pytorch模型配置
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
#model = torchvision.models.detection.keypointrcnn_resnet50_fpn(weights=KeypointRCNN_ResNet50_FPN_Weights.DEFAULT)
#model.eval()

# cv2摄像头参数配置
cap = cv2.VideoCapture(0)
camera_id = 0
img_height = 360
# 480*640
img_width = 480
none_faces = "未获取到数据"


class Ui_FD_Main_Window(QMainWindow):
    def __init__(self):
        super(Ui_FD_Main_Window, self).__init__()

        self.count_timer = 0

        self.data_ear = 0
        self.data_mar = 0
        self.data_ear_delay = 0
        self.data_mar_delay = 0
        self.data_ear_freq = 0
        self.data_mar_freq = 0
        self.data_ear_freq_data = 0
        self.data_thre =0

        self.parameter_data1 = QTextEdit()
        self.parameter_data1.setPlainText("0.3")
        self.data_thre = self.parameter_data1.toPlainText()

        self.identify_interval_timer = QTimer()
        self.identify_interval_timer.setInterval(50)
        self.identify_interval_timer.timeout.connect(self.identify_data_update)

        self.camera_timer = QTimer()
        self.camera_timer.setInterval(1)
        self.camera_timer.timeout.connect(self.update_camera_frame)

        self.camera_main = QLabel(self)
        self.camera_main.setFrameShape(QFrame.StyledPanel)
        self.camera_main.setFrameShadow(QFrame.Raised)
        self.camera_main = QLabel(self)
        self.camera_main.setObjectName(u"camera_main")
        self.camera_main.setGeometry(QRect(50, 60, 960, 540))
        self.camera_main.setScaledContents(True)
        font = QFont()
        font.setFamilies([u"PingFang SC"])
        font.setPointSize(66)
        self.camera_main.setFont(font)
        self.camera_main.setStyleSheet(u"border:2px solid black;")
        self.camera_main.setAlignment(Qt.AlignCenter)

        self.identify_timer = QTimer()
        self.identify_timer.setInterval(1)

        self.camera = cv2.VideoCapture(0)

        # self.count_timer = QTimer()
        # self.count_timer.setInterval(1000)

        self.setupUi(self)
        self.retranslateUi(self)

        self.open_camera.clicked.connect(self.on_open_camera_clicked)
        self.stop_camera.setEnabled(False)
        self.stop_camera.clicked.connect(self.on_stop_clicked)
        self.exit_exec.clicked.connect(self.on_exit_clicked)

    def setupUi(self, FD_Main_Window):
        if not FD_Main_Window.objectName():
            FD_Main_Window.setObjectName(u"FD_Main_Window")
        FD_Main_Window.resize(1218, 795)
        self.actionQuit = QAction(FD_Main_Window)
        self.actionQuit.setObjectName(u"actionQuit")

        self.centralwidget = QWidget(FD_Main_Window)
        self.centralwidget.setObjectName(u"centralwidget")

        self.camera_title = QLabel(self.centralwidget)
        self.camera_title.setObjectName(u"camera_title")
        self.camera_title.setGeometry(QRect(50, 25, 101, 31))
        font1 = QFont()
        font1.setFamilies([u"PingFang SC"])
        font1.setPointSize(20)
        self.camera_title.setFont(font1)

        self.control_title = QLabel(self.centralwidget)
        self.control_title.setObjectName(u"control_title")
        self.control_title.setGeometry(QRect(50, 620, 58, 16))

        self.open_camera = QPushButton(self.centralwidget)
        self.open_camera.setObjectName(u"open_camera")
        self.open_camera.setGeometry(QRect(50, 640, 100, 41))

        self.stop_camera = QPushButton(self.centralwidget)
        self.stop_camera.setObjectName(u"stop_camera")
        self.stop_camera.setGeometry(QRect(160, 640, 100, 41))

        self.exit_exec = QPushButton(self.centralwidget)
        self.exit_exec.setObjectName(u"exit_exec")
        self.exit_exec.setGeometry(QRect(270, 640, 100, 41))

        self.parameter_title = QLabel(self.centralwidget)
        self.parameter_title.setObjectName(u"parameter_title")
        self.parameter_title.setGeometry(QRect(400, 620, 58, 16))

        self.detail_data = QLabel(self.centralwidget)
        self.detail_data.setObjectName(u"detail_data")
        self.detail_data.setGeometry(QRect(750, 620, 58, 16))

        self.parameter_data1 = QTextEdit(self.centralwidget)
        self.parameter_data1.setObjectName(u"parameter_data1")
        self.parameter_data1.setGeometry(QRect(470, 640, 71, 31))

        self.parameter_data2 = QTextEdit(self.centralwidget)
        self.parameter_data2.setObjectName(u"parameter_data2")
        self.parameter_data2.setGeometry(QRect(620, 640, 71, 31))

        self.ear_data = QLabel(self.centralwidget)
        self.ear_data.setObjectName(u"ear_data")
        self.ear_data.setGeometry(QRect(750, 650, 170, 20))

        self.mar_data = QLabel(self.centralwidget)
        self.mar_data.setObjectName(u"mar_data")
        self.mar_data.setGeometry(QRect(750, 680, 170, 16))

        self.ear_freq = QLabel(self.centralwidget)
        self.ear_freq.setObjectName(u"ear_freq")
        self.ear_freq.setGeometry(QRect(940, 650, 170, 16))

        self.mar_freq = QLabel(self.centralwidget)
        self.mar_freq.setObjectName(u"mar_freq")
        self.mar_freq.setGeometry(QRect(940, 680, 170, 16))

        self.parameter_1 = QLabel(self.centralwidget)
        self.parameter_1.setObjectName(u"parameter_1")
        self.parameter_1.setGeometry(QRect(410, 650, 58, 16))

        self.parameter_2 = QLabel(self.centralwidget)
        self.parameter_2.setObjectName(u"parameter_2")
        self.parameter_2.setGeometry(QRect(550, 650, 58, 16))

        self.statue_output = QLabel(self.centralwidget)
        self.statue_output.setObjectName(u"statue_output")
        self.statue_output.setGeometry(QRect(680, 20, 311, 31))
        font2 = QFont()
        font2.setPointSize(25)
        self.statue_output.setFont(font2)

        FD_Main_Window.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(FD_Main_Window)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1218, 24))

        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        FD_Main_Window.setMenuBar(self.menubar)

        self.statusbar = QStatusBar(FD_Main_Window)
        self.statusbar.setObjectName(u"statusbar")
        FD_Main_Window.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu.menuAction())
        self.menu.addAction(self.actionQuit)

        self.retranslateUi(FD_Main_Window)

        QMetaObject.connectSlotsByName(FD_Main_Window)

    # setupUi

    def retranslateUi(self, FD_Main_Window):
        FD_Main_Window.setWindowTitle("FD Main")
        self.actionQuit.setText("Quit")
        self.camera_main.setText("CAMERA")
        self.camera_title.setText("摄像头画面")
        self.control_title.setText("控制面板")
        self.open_camera.setText("打开摄像头")
        self.stop_camera.setText("关闭摄像头")
        self.exit_exec.setText("退出程序")
        self.parameter_title.setText("阈值调整")
        self.detail_data.setText("详细数据")
        self.ear_data.setText("加载中")
        self.mar_data.setText("加载中")
        self.ear_freq.setText("加载中")
        self.mar_freq.setText("加载中")
        self.parameter_1.setText("加载中")
        self.parameter_2.setText("加载中")
        self.statue_output.setText("目前状态：")
        self.menu.setTitle("菜单")

    # retranslateUi

    def on_open_camera_clicked(self):
        if self.camera.isOpened():
            self.camera.release()
            self.camera_timer.stop()
            self.open_camera.setText("打开摄像头")
            self.camera_main.setAlignment(Qt.AlignCenter)
            font = QFont()
            font.setPointSize(30)
            self.camera_main.setFont(font)
            self.camera_main.setText("摄像头未开启")
            self.stop_camera.setEnabled(False)
        else:
            self.camera = cv2.VideoCapture(0)
            self.camera_timer.start()
            # self.count_timer.start()
            self.identify_interval_timer.start()
            self.camera_timer.timeout.connect(self.update_camera_frame)
            self.stop_camera.setEnabled(True)

    def on_stop_clicked(self):
        self.camera.release()
        self.camera_timer.stop()
        self.camera_main.setText("Disconnected.")
        self.stop_camera.setEnabled(False)

    def on_exit_clicked(self):
        self.camera.release()
        self.camera_timer.stop()
        self.identify_timer.stop()
        # self.count_timer.stop()
        sys.exit()

    def update_camera_frame(self):
        self.camera = cv2.VideoCapture(0)
        if not self.camera.isOpened():
            return
        ret, frame = self.camera.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # faces = detector(gray)
            # for face in faces:
            #     landmarks = predictor(gray, face)
            #     for i in range(68):
            #         x, y = landmarks.part(i).x, landmarks.part(i).y
            #         cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)
            image = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(image)
            self.camera_main.setPixmap(pixmap)

    def update_identify(self):
        if time_count == 5:
            self.time_count = 0
            # self.count_timer.release()

    def identify_data_update(self):
        if not self.camera.isOpened():
            self.ear_data.setText(none_faces)
            self.mar_data.setText(none_faces)
            self.ear_freq.setText(none_faces)
            self.mar_freq.setText(none_faces)
            return
        ret, frame = self.camera.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = detector(gray)
            for face in faces:
                landmarks = predictor(gray, face)
            if len(faces) == 0:
                self.ear_data.setText("眼部开合度：%s" % none_faces)
                self.mar_data.setText("嘴部开合度：%s" % none_faces)
                self.ear_freq.setText("眼部开合频率：%d" % self.data_ear_freq_data)
                self.mar_freq.setText("嘴部开合频率：%d" % self.data_mar_freq)
            if len(faces) > 0:
                self.data_ear: float = ear_count(landmarks)
                self.data_mar: float = mar_count(landmarks)
                self.ear_data.setText("眼部开合度：%.2f" % self.data_ear)
                self.mar_data.setText("嘴部开合度：%.2f" % self.data_mar)
                time.sleep(500 / 1000)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = detector(gray)
                for face in faces:
                    landmarks = predictor(gray, face)
                if len(faces) == 0:
                    self.ear_data.setText("眼部开合度：%s" % none_faces)
                    self.mar_data.setText("嘴部开合度：%s" % none_faces)
                    self.ear_freq.setText("眼部开合频率：%d" % self.data_ear_freq_data)
                    self.mar_freq.setText("嘴部开合频率：%d" % self.data_mar_freq)
                if len(faces) > 0:
                    self.data_ear_delay: float = ear_count(landmarks)
                    self.data_mar_delay: float = mar_count(landmarks)
                    self.data_ear_gap = self.data_ear_delay - self.data_ear
                    self.data_mar_gap = self.data_mar_delay - self.data_mar
                    if self.data_ear_gap < -float(self.data_thre):
                        self.data_ear_freq_data = self.data_ear_freq_data + 1
                    if self.data_ear_gap > float(self.data_thre):
                        self.data_ear_freq_data = self.data_ear_freq_data + 1
                    print("ear: %.2f" % self.data_ear)
                    print("gap: %.2f" % self.data_ear_gap)
                    self.ear_data.setText("眼部开合度：%.2f" % self.data_ear_delay)
                    self.mar_data.setText("嘴部开合度：%.2f" % self.data_mar_delay)
                    self.ear_freq.setText("眼部开合频率：%d" % self.data_ear_freq_data)
                    self.mar_freq.setText("嘴部开合频率：%d" % self.data_mar_freq)

    def time_count(self):
        self.tc = self.tc + 1


def ear_count(landmarks):
    ear_result: float = (abs((landmarks.part(38).y - landmarks.part(42).y)) + abs(
        (landmarks.part(39).y - landmarks.part(41).y))) / (2 * abs(
        (landmarks.part(37).x - landmarks.part(40).x)))
    return ear_result


def mar_count(landmarks):
    mar_result: float = (abs((landmarks.part(51).y - landmarks.part(59).y)) + abs(
        (landmarks.part(53).y - landmarks.part(57).y))) / (2 * abs(
        (landmarks.part(55).x - landmarks.part(49).x)))
    return mar_result


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = Ui_FD_Main_Window()
    ui.show()
    sys.exit(app.exec())
