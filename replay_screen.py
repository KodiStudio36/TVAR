# from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QSlider, QStyle, QFileDialog
# from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
# from PyQt5.QtMultimediaWidgets import QVideoWidget
# from PyQt5.QtGui import QPainter, QPen
# from PyQt5.QtCore import Qt, QUrl, QRect
# import os


# class ZoomableVideoWidget(QVideoWidget):
#     def __init__(self, parent=None):
#         super(ZoomableVideoWidget, self).__init__(parent)
#         self.setMouseTracking(True)
#         self.zoom_rect = QRect()
#         self.drawing = False
#         self.zoom_factor = 1.0

#     def mousePressEvent(self, event):
#         print("aaa")
#         if event.button() == Qt.LeftButton:
#             print("press")
#             self.zoom_rect.setTopLeft(event.pos())
#             self.zoom_rect.setBottomRight(event.pos())
#             self.drawing = True
#             self.update()

#     def mouseMoveEvent(self, event):
#         if self.drawing:
#             print("drawing moving")
#             self.zoom_rect.setBottomRight(event.pos())
#             self.update()

#     def mouseReleaseEvent(self, event):
#         if event.button() == Qt.LeftButton:
#             self.drawing = False
#             self.update()
#             self.apply_zoom()

#     def paintEvent(self, event):
#         super(ZoomableVideoWidget, self).paintEvent(event)
#         if not self.zoom_rect.isNull():
#             painter = QPainter(self)
#             painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
#             painter.drawRect(self.zoom_rect)

#     def apply_zoom(self):
#         if not self.zoom_rect.isNull():
#             self.zoom_factor = min(self.width() / self.zoom_rect.width(),
#                                    self.height() / self.zoom_rect.height())
#             self.update()

#     def resizeEvent(self, event):
#         super(ZoomableVideoWidget, self).resizeEvent(event)
#         self.zoom_factor = 1.0
#         self.update()

#     def paintEvent(self, event):
#         super(ZoomableVideoWidget, self).paintEvent(event)
#         if not self.zoom_rect.isNull():
#             painter = QPainter(self)
#             painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
#             painter.drawRect(self.zoom_rect)

#             if self.drawing or self.zoom_factor != 1.0:
#                 target_rect = QRect(0, 0, self.width(), self.height())
#                 source_rect = QRect(self.zoom_rect.left() * self.zoom_factor,
#                                     self.zoom_rect.top() * self.zoom_factor,
#                                     self.zoom_rect.width() * self.zoom_factor,
#                                     self.zoom_rect.height() * self.zoom_factor)
#                 painter.drawImage(target_rect, self.grab(source_rect).toImage(), source_rect)

# class ReplayScreen(QWidget):

#     def __init__(self, parent=None):
#         super(ReplayScreen, self).__init__(parent)

#         # Create a QMediaPlayer object
#         self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

#         # Create a QVideoWidget object to display video
#         videowidget = ZoomableVideoWidget()

#         # Create a QPushButton to open video files
#         openBtn = QPushButton('Open Video')
#         openBtn.clicked.connect(self.open_file)

#         # Create a QPushButton to play or pause the video
#         self.playBtn = QPushButton()
#         self.playBtn.setEnabled(False)
#         self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
#         self.playBtn.clicked.connect(self.play_video)

#         # Create a QSlider for seeking within the video
#         self.slider = QSlider(Qt.Horizontal)
#         self.slider.setRange(0,0)
#         self.slider.sliderMoved.connect(self.set_position)

#         # Create a QHBoxLayout for arranging widgets horizontally
#         hboxLayout = QHBoxLayout()
#         hboxLayout.setContentsMargins(0,0,0,0)

#         # Add widgets to the QHBoxLayout
#         hboxLayout.addWidget(openBtn)
#         hboxLayout.addWidget(self.playBtn)
#         hboxLayout.addWidget(self.slider)

#         # Create a QVBoxLayout for arranging widgets vertically
#         vboxLayout = QVBoxLayout()
#         vboxLayout.addWidget(videowidget)
#         vboxLayout.addLayout(hboxLayout)

#         # Set the layout of the window
#         self.setLayout(vboxLayout)

#         # Set the video output for the media player
#         self.mediaPlayer.setVideoOutput(videowidget)

#         # Connect media player signals to their respective slots
#         self.mediaPlayer.stateChanged.connect(self.mediastate_changed)
#         self.mediaPlayer.positionChanged.connect(self.position_changed)
#         self.mediaPlayer.durationChanged.connect(self.duration_changed)

#         self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(f'{os.path.dirname(__file__)}/test.avi')))
#         self.playBtn.setEnabled(True)

#     # Method to open a video file
#     def open_file(self):
#         filename, _ = QFileDialog.getOpenFileName(self, "Open Video")

#         if filename != '':
#             self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
#             self.playBtn.setEnabled(True)

#     # Method to play or pause the video
#     def play_video(self):
#         if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
#             self.mediaPlayer.pause()
#         else:
#             self.mediaPlayer.play()

#     # Method to handle changes in media player state (playing or paused)
#     def mediastate_changed(self, state):
#         if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
#             self.playBtn.setIcon(
#                 self.style().standardIcon(QStyle.SP_MediaPause)
#             )
#         else:
#             self.playBtn.setIcon(
#                 self.style().standardIcon(QStyle.SP_MediaPlay)
#             )

#     # Method to handle changes in video position
#     def position_changed(self, position):
#         self.slider.setValue(position)

#     # Method to handle changes in video duration
#     def duration_changed(self, duration):
#         self.slider.setRange(0, duration)

#     # Method to set the video position
#     def set_position(self, position):
#         self.mediaPlayer.setPosition(position)


# replay_screen.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider, QHBoxLayout
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QImage
import cv2

class ReplayScreen(QWidget):
    def __init__(self, parent=None):
        super(ReplayScreen, self).__init__(parent)

        self.layout = QVBoxLayout(self)
        self.video_label = QLabel(self)
        self.layout.addWidget(self.video_label)

        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.valueChanged.connect(self.update_frame)
        self.layout.addWidget(self.slider)

        self.setLayout(self.layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.play_video)
        self.cap = None

    def load_video(self, video_path):
        self.cap = cv2.VideoCapture(video_path)
        self.frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.slider.setMaximum(self.frame_count - 1)
        self.timer.start(30)  # Adjust the interval as needed for the video FPS

    def play_video(self):
        if self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                self.display_frame(frame)
                self.slider.setValue(self.slider.value() + 1)

    def update_frame(self, position):
        if self.cap and self.cap.isOpened():
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, position)
            ret, frame = self.cap.read()
            if ret:
                self.display_frame(frame)

    def display_frame(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = frame.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
        self.video_label.setPixmap(QPixmap.fromImage(convert_to_Qt_format))

    def stop_video(self):
        self.timer.stop()
        if self.cap:
            self.cap.release()
