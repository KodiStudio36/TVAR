import cv2
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QScrollArea, QSizePolicy, QShortcut
from PyQt5.QtGui import QPixmap, QImage, QPalette, QKeySequence
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5 import QtCore
import os
import threading
import queue

list_of_cameras_state = [True, False, False, False]

# class CaptureIpCameraFramesWorker(QThread):
#     ImageUpdated = pyqtSignal(QImage)

#     def __init__(self, url, id, size, fps) -> None:
#         super(CaptureIpCameraFramesWorker, self).__init__()
#         self.url = url
#         self.id = id
#         self.size = size
#         self.fps = fps
#         self.__thread_active = True
#         self.__thread_pause = False
#         self.frame_queue = queue.Queue(maxsize=100)

#     def run(self) -> None:
#         cap = cv2.VideoCapture(self.url)

#         if not cap.isOpened():
#             print("Error: Cannot open stream")
#             return

#         writer_thread = threading.Thread(target=self.write_frames)
#         writer_thread.start()

#         while self.__thread_active:
#             ret, frame = cap.read()
#             if not ret:
#                 print("Error: Cannot read frame")
#                 break

#             if not self.__thread_pause:
#                 img = cv2.resize(frame, self.size)

#                 h, w, c = img.shape
#                 bytes_per_line = w * c
#                 cv_rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#                 qt_rgb_image = QImage(cv_rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
#                 self.ImageUpdated.emit(qt_rgb_image)

#                 try:
#                     self.frame_queue.put_nowait(img)
#                 except queue.Full:
#                     print("Warning: Queue full, dropping frame")

#         cap.release()
#         self.__thread_active = False
#         writer_thread.join()

#     def write_frames(self):
#         result = cv2.VideoWriter(f'{os.path.dirname(__file__)}/filename{self.id}.avi',
#                                  cv2.VideoWriter_fourcc(*'XVID'),
#                                  self.fps, self.size)

#         while self.__thread_active or not self.frame_queue.empty():
#             try:
#                 frame = self.frame_queue.get(timeout=1)
#                 result.write(frame)
#             except queue.Empty:
#                 continue

#         result.release()

#     def stop(self) -> None:
#         self.__thread_active = False

#     def pause(self) -> None:
#         self.__thread_pause = True

#     def unpause(self) -> None:
#         self.__thread_pause = False

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
                # Grabs, decodes and returns the next video frame.
                ret, frame = cap.read()

                if not ret:
                    break

                # If frame is read correctly.
                if not self.__thread_pause:
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

        print(cap.isOpened(), self.__thread_active)

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

class Cam:

    def __init__(self, url, id, size, fps) -> None:
        self.url = url
        self.id = id
        self.size = size
        self.fps = fps

        self.camera = QLabel()
        self.camera.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.camera.setScaledContents(True)

        self.QScrollArea = QScrollArea()
        self.QScrollArea.setBackgroundRole(QPalette.Dark)
        self.QScrollArea.setWidgetResizable(True)
        self.QScrollArea.setWidget(self.camera)

        # Create an instance of CaptureIpCameraFramesWorker.
        self.CaptureIpCameraFramesWorker = CaptureIpCameraFramesWorker(self.url, self.id, self.size, self.fps)
        self.CaptureIpCameraFramesWorker.ImageUpdated.connect(lambda image: self.ShowCamera(image))
        
        # Start the thread getIpCameraFrameWorker_0.
        self.CaptureIpCameraFramesWorker.start()

    @QtCore.pyqtSlot()
    def ShowCamera(self, frame: QImage) -> None:
        self.camera.setPixmap(QPixmap.fromImage(frame))

class HomeScreen(QWidget):

    def __init__(self, parent=None) -> None:
        super(HomeScreen, self).__init__(parent)

        self.current_camera_idx = 0

        # rtsp://<Username>:<Password>@<IP Address>:<Port>/cam/realmonitor?channel=1&subtype=0
        self.cams = [
            Cam(
                "rtsp://admin:TaekwondoVAR@169.254.1.1:554",
                0,
                (1200, 800),
                30,
            ),
            # Cam(
            #     0,
            #     1,
            #     (800, 600),
            #     11
            # )
        ]

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
        for cam in self.cams:
            grid_layout.addWidget(cam.QScrollArea, 0, 0)

        self.setLayout(grid_layout)

        self.setPage(0)

    def setPage(self, id) -> None:
        global list_of_cameras_state
        for idx, cam in enumerate(self.cams):
            if cam.id == id:
                cam.QScrollArea.show()

            else:
                cam.QScrollArea.hide()

            list_of_cameras_state[idx] = cam.id == id
        
        self.current_camera_idx = id

    # Overwrite method closeEvent from class QMainWindow.
    def closeEvent(self, event) -> None:
        for cam in self.cams:
            if cam.CaptureIpCameraFramesWorker.isRunning():
                cam.CaptureIpCameraFramesWorker.quit()

        # Accept the event
        event.accept()