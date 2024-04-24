import numpy as np
import cv2
import threading
from copy import deepcopy
from imutils.video import FPS

import dlib
import torchvision
from torchvision.models.detection import KeypointRCNN_ResNet50_FPN_Weights


thread_lock = threading.Lock()
thread_exit = False

# 加载人脸检测器和68点模型
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# 加载预训练的人脸检测模型
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# 加载预训练的PyTorch模型
model = torchvision.models.detection.keypointrcnn_resnet50_fpn(weights=KeypointRCNN_ResNet50_FPN_Weights.DEFAULT)
model.eval()
# yolomodel = YOLO('YOLOv8s.pt')


class myThread(threading.Thread):
    def __init__(self, camera_id, img_height, img_width):
        super(myThread, self).__init__()
        self.camera_id = camera_id
        self.img_height = img_height
        self.img_width = img_width
        self.frame = np.zeros((img_height, img_width, 3), dtype=np.uint8)

    def get_frame(self):
        return deepcopy(self.frame)

    def run(self):
        global thread_exit
        cap = cv2.VideoCapture(self.camera_id)
        while not thread_exit:
            ret, frame = cap.read()
            # 人脸识别
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            faces2 = detector(gray)
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
            if ret:
                frame = cv2.resize(frame, (self.img_width, self.img_height))
                thread_lock.acquire()
                self.frame = frame
                thread_lock.release()
            else:
                thread_exit = True
        cap.release()


def main():
    global thread_exit
    camera_id = 0
    img_height = 450
    img_width = 755
    thread = myThread(camera_id, img_height, img_width)
    thread.start()

    fps = FPS().start()
    while not thread_exit:
        thread_lock.acquire()
        frame = thread.get_frame()
        thread_lock.release()
        if frame.any() == 0:
            continue
        else:
            cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            thread_exit = True
        fps.update()
    thread.join()
    fps.stop()
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))


if __name__ == "__main__":
    main()