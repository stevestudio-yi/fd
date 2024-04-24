import sys
import time
import cv2
import dlib
import torchvision
import math
import numpy as np
import threading
from copy import deepcopy
from imutils.video import FPS

from torchvision.models.detection import KeypointRCNN_ResNet50_FPN_Weights
from PySide6 import QtCore, QtGui, QtWidgets
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

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

model = torchvision.models.detection.keypointrcnn_resnet50_fpn(weights=KeypointRCNN_ResNet50_FPN_Weights.DEFAULT)
model.eval()

cap = cv2.VideoCapture(0)
camera_id = 0
img_height = 480
img_width = 640
fps = FPS().start()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("摄像头控制窗口")
        self.resize(1820, 820)

        # 创建摄像头画面框
        self.camera_frame = QtWidgets.QLabel(self)
        self.camera_frame.setGeometry(QtCore.QRect(20, 20, 1200, 600))
        self.camera_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.camera_frame.setFrameShadow(QtWidgets.QFrame.Raised)

        # 创建摄像头开关按钮
        self.control_label = QtWidgets.QLabel(self)
        self.control_label.setGeometry(QtCore.QRect(20, 650, 120, 30))
        self.control_label.setText("控制面板")

        self.camera_button = QtWidgets.QPushButton(self)
        self.camera_button.setGeometry(QtCore.QRect(20, 680, 120, 30))
        self.camera_button.setText("打开摄像头")
        self.camera_button.clicked.connect(self.on_camera_button_clicked)

        self.identify_button = QtWidgets.QPushButton(self)
        self.identify_button.setGeometry(QtCore.QRect(180, 680, 120, 30))
        self.identify_button.setText("开始识别")
        self.identify_button.clicked.connect(self.on_identify_button_clicked)

        # 创建退出程序按钮
        self.exit_button = QtWidgets.QPushButton(self)
        self.exit_button.setGeometry(QtCore.QRect(360, 680, 120, 30))
        self.exit_button.setText("退出程序")
        self.exit_button.clicked.connect(self.on_exit_button_clicked)

        # 创建摄像头开关状态显示Label
        self.list_label = QtWidgets.QLabel(self)
        self.list_label.setGeometry(QtCore.QRect(1400, 20, 200, 30))
        self.list_label.setText("状态列表")

        self.camera_status_label = QtWidgets.QLabel(self)
        self.camera_status_label.setGeometry(QtCore.QRect(1400, 60, 160, 30))
        self.camera_status_label.setText("摄像头已关闭")

        self.eye_data = QtWidgets.QLabel(self)
        self.eye_data.setGeometry(QtCore.QRect(1400, 90, 200, 30))
        self.eye_data.setText("眼部数据")

        self.eye_data1 = QtWidgets.QLabel(self)
        self.eye_data1.setGeometry(QtCore.QRect(1400, 130, 200, 30))
        self.eye_data1.setText("loading....")

        self.eye_data_ear = QtWidgets.QLabel(self)
        self.eye_data_ear.setGeometry(QtCore.QRect(1400, 150, 160, 30))
        self.eye_data_ear.setText("loading...")

        self.mouth_data = QtWidgets.QLabel(self)
        self.mouth_data.setGeometry(QtCore.QRect(1400, 180, 200, 30))
        self.mouth_data.setText("嘴部数据")

        self.mouth_data1 = QtWidgets.QLabel(self)
        self.mouth_data1.setGeometry(QtCore.QRect(1400,200,200,30))
        self.mouth_data1.setText("loading...")

        # OpenCV摄像头初始化
        self.camera = cv2.VideoCapture(0)
        self.timer = QtCore.QTimer()
        self.timer.setInterval(1)
        self.timer.timeout.connect(self.update_camera_frame)
        # self.timer.timeout.connect(self)

        self.camera2 = cv2.VideoCapture(0)
        self.timer2 = QtCore.QTimer()
        self.timer2.setInterval(10)
        self.timer2.timeout.connect(self.update_camera_frame)

    def on_camera_button_clicked(self):
        if self.camera.isOpened():
            self.camera.release()
            self.timer2.stop()
            self.camera_button.setText("打开摄像头")
            self.camera_frame.setAlignment(Qt.AlignCenter)
            font = QFont()
            font.setPointSize(30)
            self.camera_frame.setFont(font)
            self.camera_frame.setText("摄像头未开启")

            self.camera_status_label.setText("摄像头已关闭")
            self.eye_data1.setText("loading....")
        else:
            self.camera = cv2.VideoCapture(0)
            self.timer2.start()
            self.camera_button.setText("关闭摄像头")
            self.camera_status_label.setText("摄像头已打开")

    def on_identify_button_clicked(self):
        if self.camera.isOpened():
            self.camera.release()
            self.timer.stop()
            self.identify_button.setText("开始识别")
            self.camera_frame.setAlignment(Qt.AlignCenter)
            font = QFont()
            font.setPointSize(30)
            self.camera_frame.setFont(font)
            self.camera_frame.setText("摄像头未开启")

            self.camera_status_label.setText("摄像头已关闭")
            self.eye_data1.setText("loading....")
            self.eye_data_ear.setText("loading...")
            self.mouth_data1.setText("loading...")
        else:
            self.camera = cv2.VideoCapture(0)
            self.timer.start()
            self.timer.timeout.connect(self.update_camera_frame)
            self.identify_button.setText("结束识别")
            self.camera_status_label.setText("摄像头已打开")

    def largerFont(self):
        self.font.setPointSize(24)
        self.label.setFont(self.font)

    def update_camera_frame(self):
        if not self.camera.isOpened():
            return

        ret, frame = self.camera.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = detector(gray)
            for face in faces:
                landmarks = predictor(gray, face)
                for i in range(68):
                    x, y = landmarks.part(i).x, landmarks.part(i).y
                    cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)
            image = QtGui.QImage(frame.data, frame.shape[1], frame.shape[0], QtGui.QImage.Format_RGB888)
            pixmap = QtGui.QPixmap.fromImage(image)
            self.camera_frame.setPixmap(pixmap)
            if len(faces) == 0:
                self.eye_data1.setText("未检测到")
                self.eye_data_ear.setText("未检测到")
            if len(faces) > 0:
                eye_data: float = abs(((landmarks.part(38).y + landmarks.part(39).y) - (
                        landmarks.part(42).y + landmarks.part(41).y)) / 2)
                eye_data2: float = (abs((landmarks.part(38).y - landmarks.part(42).y)) + abs(
                    (landmarks.part(39).y - landmarks.part(41).y))) / (2 * abs(
                    (landmarks.part(37).x - landmarks.part(40).x)))
                self.eye_data1.setText("上下眼皮间距平均值：%.2f" % eye_data)
                self.eye_data_ear.setText("EAR(眼部开合度): %.2f" % eye_data2)
                mouth_data1: float = (abs((landmarks.part(51).y - landmarks.part(59).y)) + abs(
                    (landmarks.part(53).y - landmarks.part(57).y))) / (2 * abs(
                    (landmarks.part(55).x - landmarks.part(49).x)))
                self.mouth_data1.setText("MAR(嘴部开合度):%.2f"% mouth_data1)

    # def update_camera_frame2(self):
    #     if not self.camera.isOpened():
    #         return
    #
    #     ret2, frame2 = self.camera2.read()
    #     if ret2:
    #         frame = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
    #         gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    #         image2 = QtGui.QImage(frame2.data, frame2.shape[1], frame2.shape[0], QtGui.QImage.Format_RGB888)
    #         pixmap2 = QtGui.QPixmap.fromImage(image2)
    #         self.camera_frame.setPixmap(pixmap2)

    def on_exit_button_clicked(self):
        self.camera.release()
        self.timer.stop()
        sys.exit()




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
