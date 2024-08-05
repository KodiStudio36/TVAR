import cv2
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QScrollArea, QSizePolicy, QShortcut
from PyQt5.QtGui import QPixmap, QImage, QPalette, QKeySequence
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5 import QtCore
import os, time

list_of_cameras_state = [True, False, False, False]

class CaptureIpCameraFramesWorker(QThread):
    # Signal emitted when a new image or a new frame is ready.
    ImageUpdated = pyqtSignal(QImage)

    def __init__(self, url, id, size, fps) -> None:
        super(CaptureIpCameraFramesWorker, self).__init__()
        # Declare and initialize instance variables.
        self.url = url
        self.id = id
        self.size = size
        self.__thread_active = True
        self.fps = fps
        self.__thread_pause = False

    def run(self) -> None:
        global list_of_cameras_state
        # Capture video from a network stream.
        cap = cv2.VideoCapture(self.url)#, cv2.CAP_FFMPEG)
        # Get default video FPS.
        # self.fps = cap.get(cv2.CAP_PROP_FPS)

        result = cv2.VideoWriter(f'{os.path.dirname(__file__)}/filename{self.id}.avi',
                         cv2.VideoWriter_fourcc(*'MJPG'),
                         self.fps, self.size) 

        # If video capturing has been initialized already.q
        if cap.isOpened():
            print(f"Cam {self.id} started")
            # While the thread is active.
            while self.__thread_active:
                #
                if not self.__thread_pause:
                    # Grabs, decodes and returns the next video frame.
                    ret, frame = cap.read()
                    # If frame is read correctly.
                    if ret:
                        img = cv2.resize(frame, self.size)

                        if list_of_cameras_state[self.id]:
                            # Get the frame height, width and channels.
                            h, w, c = img.shape
                            # Calculate the number of bytes per line.
                            bytes_per_line = w * c
                            # Convert image from BGR (cv2 default color format) to RGB (Qt default color format).
                            cv_rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                            # Convert the image to Qt format.
                            qt_rgb_image = QImage(cv_rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
                            # Scale the image.
                            # NOTE: consider removing the flag Qt.KeepAspectRatio as it will crash Python on older Windows machines
                            # If this is the case, call instead: qt_rgb_image.scaled(1280, 720) 
                            # qt_rgb_image_scaled = qt_rgb_image.scaled(1280, 720, Qt.KeepAspectRatio)  # 720p
                            # qt_rgb_image_scaled = qt_rgb_image.scaled(1920, 1080, Qt.KeepAspectRatio)
                            # Emit this signal to notify that a new image or frame is available.
                            self.ImageUpdated.emit(qt_rgb_image)

                        result.write(img)
                    else:
                        break
                
                time.sleep(1/self.fps)
        # When everything done, release the video capture object.
        cap.release()
        result.release() 
        # Tells the thread's event loop to exit with return code 0 (success).
        self.quit()

    def stop(self) -> None:
        self.__thread_active = False

    def pause(self) -> None:
        self.__thread_pause = True

    def unpause(self) -> None:
        self.__thread_pause = False


class HomeScreen(QWidget):

    def __init__(self, parent=None) -> None:
        super(HomeScreen, self).__init__(parent)

        # rtsp://<Username>:<Password>@<IP Address>:<Port>/cam/realmonitor?channel=1&subtype=0
        self.url_0 = "rtsp://admin:TaekwondoVAR@169.254.1.1:554"
        self.url_1 = 0
        self.url_2 = None
        self.url_3 = None

        if self.url_0:
            # Create an instance of a QLabel class to show camera 0.
            self.camera_0 = QLabel()
            self.camera_0.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
            self.camera_0.setScaledContents(True)

            # Create an instance of a QScrollArea class to scroll camera 0 image.
            self.QScrollArea_0 = QScrollArea()
            self.QScrollArea_0.setBackgroundRole(QPalette.Dark)
            self.QScrollArea_0.setWidgetResizable(True)
            self.QScrollArea_0.setWidget(self.camera_0)

        if self.url_1:
            # Create an instance of a QLabel class to show camera 1.
            self.camera_1 = QLabel()
            self.camera_1.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
            self.camera_1.setScaledContents(True)

            # Create an instance of a QScrollArea class to scroll camera 1 image.
            self.QScrollArea_1 = QScrollArea()
            self.QScrollArea_1.setBackgroundRole(QPalette.Dark)
            self.QScrollArea_1.setWidgetResizable(True)
            self.QScrollArea_1.setWidget(self.camera_1)

        if self.url_2:
            # Create an instance of a QLabel class to show camera 2.
            self.camera_2 = QLabel()
            self.camera_2.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
            self.camera_2.setScaledContents(True)

            # Create an instance of a QScrollArea class to scroll camera 2 image.
            self.QScrollArea_2 = QScrollArea()
            self.QScrollArea_2.setBackgroundRole(QPalette.Dark)
            self.QScrollArea_2.setWidgetResizable(True)
            self.QScrollArea_2.setWidget(self.camera_2)

        if self.url_3:
            # Create an instance of a QLabel class to show camera 3.
            self.camera_3 = QLabel()
            self.camera_3.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
            self.camera_3.setScaledContents(True)

            # Create an instance of a QScrollArea class to scroll camera 3 image.
            self.QScrollArea_3 = QScrollArea()
            self.QScrollArea_3.setBackgroundRole(QPalette.Dark)
            self.QScrollArea_3.setWidgetResizable(True)
            self.QScrollArea_3.setWidget(self.camera_3)

        self.shortcut = QShortcut(QKeySequence("1"), self)
        self.shortcut.activated.connect(lambda: self.setPage(0))

        self.shortcut = QShortcut(QKeySequence("2"), self)
        self.shortcut.activated.connect(lambda: self.setPage(1))

        self.shortcut = QShortcut(QKeySequence("3"), self)
        self.shortcut.activated.connect(lambda: self.setPage(2))

        self.shortcut = QShortcut(QKeySequence("4"), self)
        self.shortcut.activated.connect(lambda: self.setPage(3))

        # Set the UI elements for this Widget class.
        grid_layout = QGridLayout()
        grid_layout.setContentsMargins(0, 0, 0, 0)
        if self.url_0: grid_layout.addWidget(self.QScrollArea_0, 0, 0)
        if self.url_1: grid_layout.addWidget(self.QScrollArea_1, 0, 1)
        if self.url_2: grid_layout.addWidget(self.QScrollArea_2, 1, 0)
        if self.url_3: grid_layout.addWidget(self.QScrollArea_3, 1, 1)

        self.setLayout(grid_layout)

        self.setPage(0)

        if self.url_0:
            # Create an instance of CaptureIpCameraFramesWorker.
            self.CaptureIpCameraFramesWorker_0 = CaptureIpCameraFramesWorker(self.url_0, 0, (800, 600), 30)
            self.CaptureIpCameraFramesWorker_0.ImageUpdated.connect(lambda image: self.ShowCamera0(image))
            
            # Start the thread getIpCameraFrameWorker_0.
            self.CaptureIpCameraFramesWorker_0.start()

        if self.url_1:
            # Create an instance of CaptureIpCameraFramesWorker.
            self.CaptureIpCameraFramesWorker_1 = CaptureIpCameraFramesWorker(self.url_1, 1, (800, 600), 10)
            self.CaptureIpCameraFramesWorker_1.ImageUpdated.connect(lambda image: self.ShowCamera1(image))

            # Start the thread getIpCameraFrameWorker_1.
            self.CaptureIpCameraFramesWorker_1.start()

        if self.url_2:
            # Create an instance of CaptureIpCameraFramesWorker.
            self.CaptureIpCameraFramesWorker_2 = CaptureIpCameraFramesWorker(self.url_2, 2, (800, 600), 30)
            self.CaptureIpCameraFramesWorker_2.ImageUpdated.connect(lambda image: self.ShowCamera2(image))

            # Start the thread getIpCameraFrameWorker_2.
            self.CaptureIpCameraFramesWorker_2.start()

        if self.url_3:
            # Create an instance of CaptureIpCameraFramesWorker.
            self.CaptureIpCameraFramesWorker_3 = CaptureIpCameraFramesWorker(self.url_3, 3, (800, 600), 30)
            self.CaptureIpCameraFramesWorker_3.ImageUpdated.connect(lambda image: self.ShowCamera3(image))

            # Start the thread getIpCameraFrameWorker_3.
            self.CaptureIpCameraFramesWorker_3.start()

    @QtCore.pyqtSlot()
    def ShowCamera0(self, frame: QImage) -> None:
        self.camera_0.setPixmap(QPixmap.fromImage(frame))

    @QtCore.pyqtSlot()
    def ShowCamera1(self, frame: QImage) -> None:
        self.camera_1.setPixmap(QPixmap.fromImage(frame))

    @QtCore.pyqtSlot()
    def ShowCamera2(self, frame: QImage) -> None:
        self.camera_2.setPixmap(QPixmap.fromImage(frame))

    @QtCore.pyqtSlot()
    def ShowCamera3(self, frame: QImage) -> None:
        self.camera_3.setPixmap(QPixmap.fromImage(frame))

    def setPage(self, id) -> None:
        global list_of_cameras_state
        if id == 0:
            if self.url_0: self.QScrollArea_0.show()
            if self.url_1: self.QScrollArea_1.hide()
            if self.url_2: self.QScrollArea_2.hide()
            if self.url_3: self.QScrollArea_3.hide()
            list_of_cameras_state = [True, False, False, False]
        elif id == 1:
            if self.url_0: self.QScrollArea_0.hide()
            if self.url_1: self.QScrollArea_1.show()
            if self.url_2: self.QScrollArea_2.hide()
            if self.url_3: self.QScrollArea_3.hide()
            list_of_cameras_state = [False, True, False, False]
        elif id == 2:
            if self.url_0: self.QScrollArea_0.hide()
            if self.url_1: self.QScrollArea_1.hide()
            if self.url_2: self.QScrollArea_2.show()
            if self.url_3: self.QScrollArea_3.hide()
            list_of_cameras_state = [False, False, True, False]
        elif id == 3:
            if self.url_0: self.QScrollArea_0.hide()
            if self.url_1: self.QScrollArea_1.hide()
            if self.url_2: self.QScrollArea_2.hide()
            if self.url_3: self.QScrollArea_3.show()
            list_of_cameras_state = [False, False, False, True]

    # Overwrite method closeEvent from class QMainWindow.
    def closeEvent(self, event) -> None:
        if self.url_0:
            # If thread getIpCameraFrameWorker_1 is running, then exit it.
            if self.CaptureIpCameraFramesWorker_0.isRunning():
                self.CaptureIpCameraFramesWorker_0.quit()

        if self.url_1:
            # If thread getIpCameraFrameWorker_2 is running, then exit it.
            if self.CaptureIpCameraFramesWorker_1.isRunning():
                self.CaptureIpCameraFramesWorker_1.quit()

        if self.url_2:
            # If thread getIpCameraFrameWorker_3 is running, then exit it.
            if self.CaptureIpCameraFramesWorker_2.isRunning():
                self.CaptureIpCameraFramesWorker_2.quit()

        if self.url_3:
            # If thread getIpCameraFrameWorker_4 is running, then exit it.
            if self.CaptureIpCameraFramesWorker_3.isRunning():
                self.CaptureIpCameraFramesWorker_3.quit()
        # Accept the event
        event.accept()