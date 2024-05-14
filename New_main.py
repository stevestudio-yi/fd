# -*- coding: utf-8 -*-
import sys
import time
import cv2
import dlib
from PySide6 import QtGui
from threading import Thread

################################################################################
## Form generated from reading UI file 'New.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                            QMetaObject, QObject, QPoint, QRect,
                            QSize, QTime, QUrl, Qt, QTimer, QThread)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
                           QCursor, QFont, QFontDatabase, QGradient,
                           QIcon, QImage, QKeySequence, QLinearGradient,
                           QPainter, QPalette, QPixmap, QRadialGradient,
                           QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow, QPushButton,
                               QSizePolicy, QStatusBar, QTextEdit, QWidget, QLineEdit, QMessageBox)

from test import Ui_MainWindow

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
none_faces = "未获取到数据"


class Ui_FD_Main_Window(QMainWindow):
    def __init__(self):
        super(Ui_FD_Main_Window, self).__init__()
        self.data_ear = 0
        self.data_mar = 0
        self.data_ear_delay = 0
        self.data_mar_delay = 0
        self.data_ear_gap = 0
        self.data_mar_gap = 0
        self.data_set_ear = 0.11
        self.data_set_ear_tired = 0.8
        self.data_set_mar = 0.2
        self.data_set_mar_tired = 0.8
        self.data_close_eyes_count = 0
        self.data_close_eyes_set_sleep = 0.3
        self.data_ear_freq = 0
        self.data_mar_freq = 0
        self.data_time_count = 0
        self.ear_freq_ps = 0
        self.mar_freq_ps = 0
        self.camera = cv2.VideoCapture(0)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        self.camera_timer = QTimer()
        self.camera_timer.setInterval(1)
        self.camera_timer.timeout.connect(self.update_frame)
        self.identify_timer = QTimer()
        self.identify_timer.setInterval(500)
        self.identify_timer.timeout.connect(self.update_data)
        self.setupUi(self)
        self.retranslateUi(self)
        self.exit_exec.clicked.connect(sys.exit)
        self.start_camera.clicked.connect(self.on_start_clicked)
        self.stop_camera.clicked.connect(self.on_stop_clicked)
        self.parameter_data1.setText("%.2f" % self.data_set_ear)
        self.parameter_data2.setText("%.2f" % self.data_set_ear_tired)
        self.parameter_data3.setText("%.2f" % self.data_set_mar)
        self.parameter_data4.setText("%.2f" % self.data_set_mar_tired)
        self.parameter_data5.setText("%.2f" % self.data_close_eyes_set_sleep)

    def setupUi(self, FD_Main_Window):
        if not FD_Main_Window.objectName():
            FD_Main_Window.setObjectName(u"FD_Main_Window")
        FD_Main_Window.resize(1218, 795)
        font = QFont()
        font.setFamilies([u"PingFang SC"])
        FD_Main_Window.setFont(font)
        self.actionQuit = QAction(FD_Main_Window)
        self.actionQuit.setObjectName(u"actionQuit")
        self.centralwidget = QWidget(FD_Main_Window)
        self.centralwidget.setObjectName(u"centralwidget")
        self.camera_main = QLabel(self.centralwidget)
        self.camera_main.setObjectName(u"camera_main")
        self.camera_main.setGeometry(QRect(50, 60, 960, 540))
        font1 = QFont()
        font1.setFamilies([u"PingFang SC"])
        font1.setPointSize(66)
        self.camera_main.setFont(font1)
        self.camera_main.setStyleSheet(u"border:2px solid black;")
        self.camera_main.setAlignment(Qt.AlignCenter)
        self.camera_title = QLabel(self.centralwidget)
        self.camera_title.setObjectName(u"camera_title")
        self.camera_title.setGeometry(QRect(50, 25, 151, 31))
        font2 = QFont()
        font2.setFamilies([u"PingFang SC"])
        font2.setPointSize(20)
        self.camera_title.setFont(font2)
        self.control_title = QLabel(self.centralwidget)
        self.control_title.setObjectName(u"control_title")
        self.control_title.setGeometry(QRect(50, 620, 58, 16))
        self.control_title.setFont(font)
        self.start_camera = QPushButton(self.centralwidget)
        self.start_camera.setObjectName(u"start_camera")
        self.start_camera.setGeometry(QRect(50, 640, 100, 41))
        self.start_camera.setFont(font)
        self.stop_camera = QPushButton(self.centralwidget)
        self.stop_camera.setObjectName(u"stop_camera")
        self.stop_camera.setGeometry(QRect(160, 640, 100, 41))
        self.stop_camera.setFont(font)
        self.exit_exec = QPushButton(self.centralwidget)
        self.exit_exec.setObjectName(u"exit_exec")
        self.exit_exec.setGeometry(QRect(270, 640, 100, 41))
        self.exit_exec.setFont(font)
        self.parameter_title = QLabel(self.centralwidget)
        self.parameter_title.setObjectName(u"parameter_title")
        self.parameter_title.setGeometry(QRect(380, 620, 58, 16))
        self.parameter_title.setFont(font)
        self.detail_data = QLabel(self.centralwidget)
        self.detail_data.setObjectName(u"detail_data")
        self.detail_data.setGeometry(QRect(750, 610, 58, 16))
        self.detail_data.setFont(font)
        self.parameter_data1 = QLineEdit(self.centralwidget)
        self.parameter_data1.setObjectName(u"parameter_data1")
        self.parameter_data1.setGeometry(QRect(450, 640, 71, 31))
        self.parameter_data1.setFont(font)
        self.parameter_data2 = QLineEdit(self.centralwidget)
        self.parameter_data2.setObjectName(u"parameter_data2")
        self.parameter_data2.setGeometry(QRect(630, 640, 71, 31))
        self.parameter_data2.setFont(font)
        self.parameter_data3 = QLineEdit(self.centralwidget)
        self.parameter_data3.setObjectName(u"parameter_data3")
        self.parameter_data3.setGeometry(QRect(450, 690, 71, 31))
        self.parameter_data3.setFont(font)
        self.parameter_data4 = QLineEdit(self.centralwidget)
        self.parameter_data4.setObjectName(u"parameter_data4")
        self.parameter_data4.setGeometry(QRect(630, 690, 71, 31))
        self.parameter_data4.setFont(font)
        self.parameter_data5 = QLineEdit(self.centralwidget)
        self.parameter_data5.setObjectName(u"parameter_data5")
        self.parameter_data5.setGeometry(QRect(450, 740, 71, 31))
        self.ear_data = QLabel(self.centralwidget)
        self.ear_data.setObjectName(u"ear_data")
        self.ear_data.setGeometry(QRect(760, 640, 181, 20))
        self.ear_data.setFont(font)
        self.mar_data = QLabel(self.centralwidget)
        self.mar_data.setObjectName(u"mar_data")
        self.mar_data.setGeometry(QRect(760, 700, 161, 16))
        self.mar_data.setFont(font)
        self.ear_freq = QLabel(self.centralwidget)
        self.ear_freq.setObjectName(u"ear_freq")
        self.ear_freq.setGeometry(QRect(950, 640, 181, 16))
        self.ear_freq.setFont(font)
        self.mar_freq = QLabel(self.centralwidget)
        self.mar_freq.setObjectName(u"mar_freq")
        self.mar_freq.setGeometry(QRect(950, 700, 181, 16))
        self.mar_freq.setFont(font)
        self.parameter_1 = QLabel(self.centralwidget)
        self.parameter_1.setObjectName(u"parameter_1")
        self.parameter_1.setGeometry(QRect(390, 650, 58, 16))
        self.parameter_1.setFont(font)
        self.parameter_2 = QLabel(self.centralwidget)
        self.parameter_2.setObjectName(u"parameter_2")
        self.parameter_2.setGeometry(QRect(540, 650, 70, 16))
        self.parameter_2.setFont(font)
        self.parameter_3 = QLabel(self.centralwidget)
        self.parameter_3.setObjectName(u"parameter_3")
        self.parameter_3.setGeometry(QRect(390, 700, 58, 16))
        self.parameter_3.setFont(font)
        self.parameter_4 = QLabel(self.centralwidget)
        self.parameter_4.setObjectName(u"parameter_4")
        self.parameter_4.setGeometry(QRect(540, 700, 75, 16))
        self.parameter_4.setFont(font)
        self.parameter_5 = QLabel(self.centralwidget)
        self.parameter_5.setObjectName(u"parameter_5")
        self.parameter_5.setGeometry(QRect(390, 750, 58, 16))
        self.parameter_5.setFont(font)
        self.statue_output = QLabel(self.centralwidget)
        self.statue_output.setObjectName(u"statue_output")
        self.statue_output.setGeometry(QRect(680, 20, 341, 31))
        font3 = QFont()
        font3.setFamilies([u"PingFang SC"])
        font3.setPointSize(25)
        self.statue_output.setFont(font3)
        FD_Main_Window.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(FD_Main_Window)
        self.statusbar.setObjectName(u"statusbar")
        FD_Main_Window.setStatusBar(self.statusbar)

        self.retranslateUi(FD_Main_Window)

        QMetaObject.connectSlotsByName(FD_Main_Window)

    # setupUi

    def retranslateUi(self, FD_Main_Window):
        FD_Main_Window.setWindowTitle(QCoreApplication.translate("FD_Main_Window", u"FD - Main", None))
        self.actionQuit.setText(QCoreApplication.translate("FD_Main_Window", u"Quit", None))
        self.camera_main.setText(QCoreApplication.translate("FD_Main_Window", u"CAMERA", None))
        self.camera_title.setText(QCoreApplication.translate("FD_Main_Window", u"\u6444\u50cf\u5934\u753b\u9762", None))
        self.control_title.setText(QCoreApplication.translate("FD_Main_Window", u"\u63a7\u5236\u9762\u677f", None))
        self.start_camera.setText(QCoreApplication.translate("FD_Main_Window", u"START", None))
        self.stop_camera.setText(QCoreApplication.translate("FD_Main_Window", u"STOP", None))
        self.exit_exec.setText(QCoreApplication.translate("FD_Main_Window", u"EXIT", None))
        self.parameter_title.setText(QCoreApplication.translate("FD_Main_Window", u"\u9608\u503c\u8c03\u6574", None))
        self.detail_data.setText(QCoreApplication.translate("FD_Main_Window", u"\u8be6\u7ec6\u6570\u636e", None))
        self.ear_data.setText(
            QCoreApplication.translate("FD_Main_Window", u"\u773c\u90e8\u5f00\u5408\u5ea6\uff1a", None))
        self.mar_data.setText(
            QCoreApplication.translate("FD_Main_Window", u"\u5634\u90e8\u5f00\u5408\u5ea6\uff1a", None))
        self.ear_freq.setText(
            QCoreApplication.translate("FD_Main_Window", u"\u773c\u90e8\u5f00\u5408\u9891\u7387\uff1a", None))
        self.mar_freq.setText(
            QCoreApplication.translate("FD_Main_Window", u"\u5634\u90e8\u5f00\u5408\u9891\u7387\uff1a", None))
        self.parameter_1.setText(QCoreApplication.translate("FD_Main_Window", u"\u0065\u0061\u0072\u9600\u503c", None))
        self.parameter_2.setText(QCoreApplication.translate("FD_Main_Window", u"\u0065\u0061\u0072\u75b2\u52b3\u9600"
                                                                              u"\u503c", None))
        self.parameter_3.setText(QCoreApplication.translate("FD_Main_Window", u"mar\u9600\u503c", None))
        self.parameter_4.setText(QCoreApplication.translate("FD_Main_Window", u"mar\u75b2\u52b3\u9600"
                                                                              u"\u503c", None))
        self.parameter_5.setText(QCoreApplication.translate("FD_Main_Window", u"\u95ed\u773c\u9600\u503c", None))
        self.statue_output.setText(
            QCoreApplication.translate("FD_Main_Window", u"\u76ee\u524d\u72b6\u6001\uff1a", None))

    # retranslateUi
    def on_start_clicked(self):
        if self.camera.isOpened():
            self.camera.release()
            self.camera_timer.stop()
            self.identify_timer.stop()
            self.start_camera.setText("START")
            self.camera_main.setText("摄像头未开启")
            self.stop_camera.setEnabled(False)
        else:
            self.camera = cv2.VideoCapture(0)
            self.camera_timer.start()
            self.identify_timer.start()
            self.camera_timer.timeout.connect(self.update_frame)
            self.stop_camera.setEnabled(True)

    def on_stop_clicked(self):
        self.camera.release()
        self.identify_timer.stop()
        self.camera_timer.stop()
        self.camera_main.setText("Disconnected.")

    def update_frame(self):
        if not self.camera.isOpened():
            return
        ret, frame = self.camera.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = detector(grey)
            for face in faces:
                landmarks = predictor(grey, face)
                for i in range(68):
                    x, y = landmarks.part(i).x, landmarks.part(i).y
                    cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)
            # if len(faces) == 0:
            #     self.ear_data.setText("眼部开合度：%s" % none_faces)
            #     self.mar_data.setText("嘴部开合度：%s" % none_faces)
            # if len(faces) > 0:
            #     self.data_ear: float = ear_count(landmarks)
            #     self.data_mar: float = mar_count(landmarks)
            #     self.ear_data.setText("眼部开合度：%.2f" % self.data_ear)
            #     self.mar_data.setText("嘴部开合度：%.2f" % self.data_mar)
            # else:
            #     self.ear_data.setText("眼部开合度：%s" % none_faces)
            #     self.mar_data.setText("嘴部开合度：%s" % none_faces)
            image = QtGui.QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(image)
            self.camera_main.setPixmap(pixmap)

    def warning_msg(self):
        warn = QMessageBox.critical(self, '警告',
                                   '被检测者可能已经睡着',
                                   buttons=QMessageBox.Ok | QMessageBox.Cancel)

    def update_data(self):
        self.data_set_ear = float(self.parameter_data1.text())
        self.data_set_ear_tired = float(self.parameter_data2.text())
        self.data_set_mar = float(self.parameter_data3.text())
        self.data_set_mar_tired = float(self.parameter_data4.text())
        self.data_close_eyes_set_sleep = float(self.parameter_data5.text())
        self.data_time_count = self.data_time_count + 0.5
        if not self.camera.isOpened():
            return
        ret, frame = self.camera.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = detector(grey)
            for face in faces:
                landmarks = predictor(grey, face)
            if len(faces) == 0:
                self.ear_data.setText("眼部开合度：%s" % none_faces)
                self.mar_data.setText("嘴部开合度：%s" % none_faces)
            if len(faces) > 0:
                self.data_ear: float = ear_count(landmarks)
                self.data_mar: float = mar_count(landmarks)
                if self.data_ear < self.data_close_eyes_set_sleep:
                    self.data_close_eyes_count += 1
                self.ear_data.setText("眼部开合度：%.2f" % self.data_ear)
                self.mar_data.setText("嘴部开合度：%.2f" % self.data_mar)
            else:
                self.ear_data.setText("眼部开合度：%s" % none_faces)
                self.mar_data.setText("嘴部开合度：%s" % none_faces)
        time.sleep(250 / 1000)
        if not self.camera.isOpened():
            return
        ret, frame = self.camera.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = detector(grey)
            for face in faces:
                landmarks = predictor(grey, face)
            if len(faces) == 0:
                self.data_ear_gap = self.data_ear
                self.data_mar_gap = self.data_mar
            if len(faces) > 0:
                self.data_ear_delay: float = ear_count(landmarks)
                self.data_mar_delay: float = mar_count(landmarks)
                self.ear_data.setText("眼部开合度：%.2f" % self.data_ear_delay)
                self.mar_data.setText("嘴部开合度：%.2f" % self.data_mar_delay)
                self.data_ear_gap = abs(self.data_ear - self.data_ear_delay)
                self.data_mar_gap = abs(self.data_mar - self.data_mar_delay)
                print("%.4f" % self.data_ear_gap)
                if self.data_ear_delay < self.data_close_eyes_set_sleep:
                    self.data_close_eyes_count += 1
                if self.data_mar_gap > self.data_set_mar:
                    self.data_mar_freq = self.data_mar_freq + 1
                if self.data_ear_gap > self.data_set_ear:
                    self.data_ear_freq = self.data_ear_freq + 1
                self.ear_freq.setText("眼部开合频率：%.2f" % self.ear_freq_ps)
                self.mar_freq.setText("嘴部开合频率：%.2f" % self.mar_freq_ps)

            else:
                self.ear_data.setText("眼部开合度：%s" % none_faces)
                self.mar_data.setText("嘴部开合度：%s" % none_faces)
        if self.data_time_count == 5:
            print(self.data_close_eyes_count)
            self.ear_freq_ps = self.data_ear_freq / self.data_time_count
            self.mar_freq_ps = self.data_mar_freq / (4 * self.data_time_count)
            if self.mar_freq_ps > self.data_set_mar_tired:
                self.statue_output.setStyleSheet("QLabel { color: red; }")
                self.statue_output.setText("目前状态：疲劳")
            if self.ear_freq_ps > self.data_set_ear_tired:
                self.statue_output.setStyleSheet("QLabel { color: red; }")
                self.statue_output.setText("目前状态：疲劳")
            if self.data_close_eyes_count >= ((4 * self.data_time_count) - 1):
                self.statue_output.setStyleSheet("QLabel { color: red; background:yellow}")
                self.statue_output.setText("目前状态：警告 已睡着")
                self.warning_msg()
            else:
                self.statue_output.setStyleSheet("QLabel { color: black; }")
                self.statue_output.setText("目前状态：正常")
            self.data_time_count = 0
            self.data_ear_freq = 0
            self.data_mar_freq = 0
            self.data_close_eyes_count = 0


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


# class identify_thread(QThread):
#     def __init__(self):
#         super(identify_thread, self).__init__()
#         QThread.__init__(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = Ui_FD_Main_Window()
    ui.show()
    sys.exit(app.exec())
