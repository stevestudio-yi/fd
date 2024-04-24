# -*-coding:gb2312-*-
import cv2
import torch
# from ultralytics import YOLO
import dlib
from torchvision import models, transforms
import torchvision
from torchvision.models.detection import KeypointRCNN_ResNet50_FPN_Weights
import torchvision.transforms as transforms
import torchvision.models as models
from torchvision.models import ResNet50_Weights
from PIL import Image
import time

import numpy as np
import threading
from copy import deepcopy
from imutils.video import FPS

thread_lock = threading.Lock()
thread_exit = False


# 多线程处理
class mThread(threading.Thread):
    def __init__(self, camera_id, img_height, img_width):
        super(mThread, self).__init__()
        self.camera_id = camera_id
        self.img_height = img_height
        self.img_width = img_width
        self.frame = np.zeros((img_height, img_width, 3), dtype=np.uint8)

    def get_frame(self):
        return deepcopy(self.frame)

    def run(self):
        global thread_exit
        mcap = cv2.VideoCapture(self.camera_id)
        while not thread_exit:
            m_ret, m_frame = mcap.read()
            if m_ret:
                m_frame = cv2.resize(m_frame, (self.img_width, self.img_height))
                thread_lock.acquire()
                self.frame = m_frame
                thread_lock.release()
            else:
                thread_exit = True
        mcap.release()


# 加载人脸检测器和68点模型
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# 加载预训练的人脸检测模型
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# 加载预训练的PyTorch模型
model = torchvision.models.detection.keypointrcnn_resnet50_fpn(weights=KeypointRCNN_ResNet50_FPN_Weights.DEFAULT)
model.eval()
# yolomodel = YOLO('YOLOv8s.pt')

# 打开摄像头
cap = cv2.VideoCapture(0)
camera_id = 0
img_height = 480
img_width = 640
frame_count = 0
fps = FPS().start()


while True:
    ret, frame = cap.read()
    # frame_count += 1
    # cv2.putText(frame, f"Frame: {frame_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # 转换为灰度图像
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 检测人脸
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    faces2 = detector(gray)
    # 在图像中绘制人脸框
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        # text = ('face')
        # cv2.putText(frame,(x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255, 0, 0), 2)
    for face2 in faces2:
        # 获取关键点
        landmarks = predictor(gray, face2)

        # 在图像上绘制关键点
        for i in range(68):
            x, y = landmarks.part(i).x, landmarks.part(i).y
            cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)
    # 显示图像
    cv2.imshow('Face Detection', frame)
    if cv2.waitKey(1) & 0xFF == ord(" "):
        cv2.waitKey(0)
    # 退出循环
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放摄像头并关闭窗口
cap.release()
cv2.destroyAllWindows()
