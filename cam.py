import cv2
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QScrollArea, QSizePolicy, QShortcut
from PyQt5.QtGui import QPixmap, QImage, QPalette, QKeySequence
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5 import QtCore
import os

from preferences import load_preferences
from config import Config

class Cam:
    def __init__(self, url, id, size=(1200, 800), fps=30) -> None:
        self.url = url
        self.id = id
        self.size = size
        self.fps = fps

        self.CaptureIpCameraFramesWorker = None

        self.camera = QLabel()
        self.camera.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.camera.setScaledContents(True)

        self.QScrollArea = QScrollArea()
        self.QScrollArea.setBackgroundRole(QPalette.Dark)
        self.QScrollArea.setWidgetResizable(True)
        self.QScrollArea.setWidget(self.camera)

        self.start()

    @QtCore.pyqtSlot()
    def ShowCamera(self, frame: QImage) -> None:
        self.camera.setPixmap(QPixmap.fromImage(frame))

    def clear_pixmap(self):
        """Clears the current pixmap from the QLabel."""
        self.camera.setPixmap(QPixmap())

    def set_url(self, url) -> None:
        self.url = url

    def set_size(self, size) -> None:
        self.size = size

    def set_fps(self, fps) -> None:
        self.fps = fps

    def get_widget(self):
        return self.QScrollArea
    
    def show(self) -> None:
        self.QScrollArea.show()

    def hide(self) -> None:
        self.QScrollArea.hide()

    def isVisible(self) -> bool:
        return self.QScrollArea.isVisible()
    
    def start_recording(self):
        if self.CaptureIpCameraFramesWorker:
            self.CaptureIpCameraFramesWorker.start_recording()

    def stop_recording(self):
        if self.CaptureIpCameraFramesWorker:
            self.CaptureIpCameraFramesWorker.stop_recording()
    
    def start(self):
        print("start")
        if self.url != None:
            # Create an instance of CaptureIpCameraFramesWorker.
            self.CaptureIpCameraFramesWorker = CaptureIpCameraFramesWorker(self)
            self.CaptureIpCameraFramesWorker.ImageUpdated.connect(lambda image: self.ShowCamera(image))
            print("starting")
            
            self.CaptureIpCameraFramesWorker.start()
            print("started")

    def pause(self):
        if self.CaptureIpCameraFramesWorker != None:
            self.CaptureIpCameraFramesWorker.pause()

    def unpause(self):
        if self.CaptureIpCameraFramesWorker != None:
            self.CaptureIpCameraFramesWorker.unpause()

    def stop(self):
        print("stop")
        if self.CaptureIpCameraFramesWorker != None and self.CaptureIpCameraFramesWorker.isRunning():
            print("stopping")
            self.CaptureIpCameraFramesWorker.stop()
            self.CaptureIpCameraFramesWorker.wait()  # Ensure the thread is properly terminated
            self.CaptureIpCameraFramesWorker = None
        
        self.clear_pixmap()

    def fromJson(data):
        return Cam(data["url"], data["id"], data["size"], data["fps"])


class CaptureIpCameraFramesWorker(QThread):
    # Signal emitted when a new image or a new frame is ready.
    ImageUpdated = pyqtSignal(QImage)

    def __init__(self, parent: Cam) -> None:
        super(CaptureIpCameraFramesWorker, self).__init__()

        # Declare and initialize instance variables.
        self.cam = parent

        self.video_writer = None
        self.recording = False
        self.url = parent.url
        self.id = parent.id
        self.size = parent.size
        self.__thread_active = True
        self.fps = parent.fps
        self.__thread_pause = False

    def run(self) -> None:
        # Capture video from a network stream.
        cap = cv2.VideoCapture(self.url)#, cv2.CAP_FFMPEG)
        # Get default video FPS.
        # self.fps = cap.get(cv2.CAP_PROP_FPS)

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

                    if self.cam.isVisible():
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

                    if self.recording:
                        self.video_writer.write(img)

        print(cap.isOpened(), self.__thread_active)

        # When everything done, release the video capture object.
        cap.release()
        # Tells the thread's event loop to exit with return code 0 (success).
        self.quit()

    def initialize_writer(self):
        """Initialize the VideoWriter with the current filename."""
        if self.video_writer is not None:
            self.video_writer.release()
        
        self.video_writer = cv2.VideoWriter(
            os.path.join(Config.PATH, f"{Config.FILENAME}{self.id}.{Config.FILEFORMAT}"),
            cv2.VideoWriter_fourcc(*'MJPG'),
            self.fps,
            self.size
        )
        print(f"VideoWriter initialized with filename: {Config.FILENAME}{self.id}")

    def start_recording(self) -> None:
        self.initialize_writer()
        self.recording = True

    def stop_recording(self) -> None:
        self.video_writer.release()
        self.recording = False

    def stop(self) -> None:
        self.__thread_active = False

    def pause(self) -> None:
        self.__thread_pause = True

    def unpause(self) -> None:
        self.__thread_pause = False

def load_cams():
    preferences = load_preferences()
    return [Cam.fromJson(cam) for cam in preferences["cams"]]