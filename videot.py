import sys

import cv2
import pyqtgraph as pg
from PySide6.QtCore import (QMetaObject, QRect)
from PySide6.QtGui import (QFont, QIcon)
from PySide6.QtWidgets import (QApplication, QLabel, QMenuBar,
                               QPushButton, QStatusBar, QWidget)


class MainWindow(QWidget):
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

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Test window")

        layout = QVBoxLayout()

        self.status_lable = QLabel()
        self.status_lable.setText("opened")

        self.cap = cv2.VideoCapture(0)

        self.timer = QTimer()
        self.timer.setInterval(33)
        self.timer.timeout.connect(self.update_frame)

        self.start_button = QPushButton("Open CAM")
        self.start_button.clicked.connect(self.start_camera)
        self.stop_button = QPushButton("Close CAM")
        self.stop_button.clicked.connect(self.stop_camera)

        layout.addWidget(self.status_lable)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)

        self.setLayout(layout)

        self.show()

    def start_camera(self):
        if not self.cap.isOpened():
            self.cap.open(0)
        self.timer.start()
        self.status_lable.setText("CAM is opened")

    def stop_camera(self):
        self.cap.release()
        self.timer.stop()
        self.status_lable.setText("CAM is closed")

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = pg.ImageView(frame)

            win = pg.GraphicsWindow(title="cam item")
            win.addItem(image)
            win.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
