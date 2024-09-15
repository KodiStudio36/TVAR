import os
from PyQt5.QtMultimediaWidgets import QGraphicsVideoItem
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QVBoxLayout, QWidget, QPushButton, QShortcut, QSlider, QStyle, QHBoxLayout
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, Qt, QSizeF
from PyQt5.QtGui import QWheelEvent, QMouseEvent, QKeySequence

from config import Config

class VideoWidget(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.fps = 30

        # Create a scene and a video item
        self.scene = QGraphicsScene(self)
        self.videoItem = QGraphicsVideoItem()
        self.scene.addItem(self.videoItem)

        # Set the scene on the view
        self.setScene(self.scene)

        # Set up the media player
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.mediaPlayer.setVideoOutput(self.videoItem)

        # Set some initial zoom factor
        self.zoom_factor = 1.0

        # Dragging variables
        self.dragging = False
        self.last_mouse_pos = None

        self.show()

    def resizeEvent(self, event):
        """ Resize the video item to maintain the aspect ratio 4:3 """
        view_width = self.size().width() - 2
        view_height = self.size().height() - 2

        if view_height > view_width:
            # Calculate the height for 4:3 aspect ratio
            view_height = view_width * 3 / 4

        else:
            view_width = view_height * 4 / 3

        # Set the size of the video item
        self.videoItem.setSize(QSizeF(view_width, view_height))

        # Center the video item in the scene
        self.videoItem.setPos(0, 0)

        super().resizeEvent(event)

    def wheelEvent(self, event: QWheelEvent):
        """ Handle mouse wheel event to zoom in and out """
        if event.angleDelta().y() > 0:
            self.zoom_in()
        else:
            self.zoom_out()

    def zoom_in(self):
        self.zoom_factor += 0.1
        self.setTransformAA()

    def zoom_out(self):
        if self.zoom_factor > 1.0:
            self.zoom_factor -= 0.1
            self.setTransformAA()

    def zoom_reset(self):
        self.zoom_factor = 1
        self.setTransformAA()

    def setTransformAA(self):
        transform = self.transform()
        transform.reset()  # Reset any previous transformations
        transform.scale(self.zoom_factor, self.zoom_factor)
        self.setTransform(transform)

    def mousePressEvent(self, event: QMouseEvent):
        """ Handle mouse press event for dragging """
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.last_mouse_pos = event.pos()

    def mouseMoveEvent(self, event: QMouseEvent):
        """ Handle mouse move event for dragging """
        if self.dragging:
            # Calculate how much the mouse moved
            delta = event.pos() - self.last_mouse_pos
            self.last_mouse_pos = event.pos()

            # Scroll the scene by the delta
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - delta.y())

    def mouseReleaseEvent(self, event: QMouseEvent):
        """ Handle mouse release event to stop dragging """
        if event.button() == Qt.LeftButton:
            self.dragging = False

    def play_video(self):
        self.mediaPlayer.play()

    def pause_video(self):
        self.mediaPlayer.pause()

    def set_position(self, position):
        self.mediaPlayer.setPosition(position)

    def frame_forward(self):
        current_position = self.mediaPlayer.position()
        new_position = int(current_position + 1000 / self.fps)
        self.mediaPlayer.setPosition(new_position)

    def frame_backward(self):
        current_position = self.mediaPlayer.position()
        new_position = int(current_position - 1000 / self.fps)
        self.mediaPlayer.setPosition(new_position)

    def sec_forward(self):
        current_position = self.mediaPlayer.position()
        new_position = int(current_position + 1000)
        self.mediaPlayer.setPosition(new_position)

    def sec_backward(self):
        current_position = self.mediaPlayer.position()
        new_position = int(current_position - 1000)
        self.mediaPlayer.setPosition(new_position)

    def load_video(self, filename, duration=None):
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(f'{Config.PATH}/{filename}')))
        if duration:
            self.mediaPlayer.setPosition(duration)

        self.mediaPlayer.play()
        self.mediaPlayer.pause()


class ReplayScreen(QWidget):
    def __init__(self, parent=None):
        super(ReplayScreen, self).__init__(parent)

        # Create and add the video widget
        self.videoWidget = VideoWidget()

        # Create a QPushButton to play or pause the video
        self.playBtn = QPushButton()
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn.clicked.connect(self.play_video)

        self.frameBackward = QPushButton()
        self.frameBackward.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekBackward))
        self.frameBackward.clicked.connect(self.frame_backward)

        self.frameForward = QPushButton()
        self.frameForward.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekForward))
        self.frameForward.clicked.connect(self.frame_forward)

        self.secondBackward = QPushButton()
        self.secondBackward.setIcon(self.style().standardIcon(QStyle.SP_ArrowBack))
        self.secondBackward.clicked.connect(self.sec_backward)

        self.secondForward = QPushButton()
        self.secondForward.setIcon(self.style().standardIcon(QStyle.SP_ArrowForward))
        self.secondForward.clicked.connect(self.sec_forward)

        # Create a QSlider for seeking within the video
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0,0)
        self.slider.sliderMoved.connect(self.set_position)
        self.slider.sliderPressed.connect(self.sliderPressed)
        self.slider.sliderReleased.connect(self.sliderReleased)
 
        # Create a QHBoxLayout for arranging widgets horizontally
        hboxLayout = QHBoxLayout()
        hboxLayout.setContentsMargins(0,0,0,0)
 
        # Add widgets to the QHBoxLayout
        hboxLayout.addWidget(self.playBtn)
        hboxLayout.addWidget(self.frameBackward)
        hboxLayout.addWidget(self.frameForward)
        hboxLayout.addWidget(self.slider)
        hboxLayout.addWidget(self.secondBackward)
        hboxLayout.addWidget(self.secondForward)
 
        # Create a QVBoxLayout for arranging widgets vertically
        layout = QVBoxLayout(self)
        layout.addWidget(self.videoWidget)
        layout.addLayout(hboxLayout)

        self.setLayout(layout)

        self.videoWidget.mediaPlayer.stateChanged.connect(self.mediastate_changed)
        self.videoWidget.mediaPlayer.positionChanged.connect(self.position_changed)
        self.videoWidget.mediaPlayer.durationChanged.connect(self.duration_changed)

        self.isPlaying = False
        self.isFirstOpen = False

        self.shortcut = QShortcut(QKeySequence("1"), self)
        self.shortcut.activated.connect(lambda: self.set_page(f"{Config.FILENAME}0.{Config.FILEFORMAT}"))

        self.shortcut = QShortcut(QKeySequence("2"), self)
        self.shortcut.activated.connect(lambda: self.set_page(f"{Config.FILENAME}1.{Config.FILEFORMAT}"))

        self.shortcut = QShortcut(QKeySequence("3"), self)
        self.shortcut.activated.connect(lambda: self.set_page(f"{Config.FILENAME}2.{Config.FILEFORMAT}"))

        self.shortcut = QShortcut(QKeySequence("4"), self)
        self.shortcut.activated.connect(lambda: self.set_page(f"{Config.FILENAME}3.{Config.FILEFORMAT}"))

        self.shortcut = QShortcut(QKeySequence(" "), self)
        self.shortcut.activated.connect(lambda: self.play_video())

        self.shortcut = QShortcut(QKeySequence("Right"), self)
        self.shortcut.activated.connect(lambda: self.frame_forward())

        self.shortcut = QShortcut(QKeySequence("Left"), self)
        self.shortcut.activated.connect(lambda: self.frame_backward())

        self.shortcut = QShortcut(QKeySequence("Ctrl+Right"), self)
        self.shortcut.activated.connect(lambda: self.sec_forward())

        self.shortcut = QShortcut(QKeySequence("Ctrl+Left"), self)
        self.shortcut.activated.connect(lambda: self.sec_backward())

        self.shortcut = QShortcut(QKeySequence("Escape"), self)
        self.shortcut.activated.connect(lambda: self.videoWidget.zoom_reset())

    # Method to play or pause the video
    def play_video(self):
        if self.videoWidget.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.videoWidget.pause_video()
            self.isPlaying = False
        else:
            self.videoWidget.play_video()
            self.isPlaying = True

    # Method to handle changes in media player state (playing or paused)
    def mediastate_changed(self, state):
        if state == QMediaPlayer.PlayingState:
            self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    # Method to handle changes in video position
    def position_changed(self, position):
        self.slider.setValue(position)
 
    # Method to handle changes in video duration
    def duration_changed(self, duration):
        self.slider.setRange(0, duration)

    # Method to set the video position
    def set_position(self, position):
        self.videoWidget.set_position(position)

    def sliderPressed(self):
        self.videoWidget.pause_video()

    def sliderReleased(self):
        self.videoWidget.play_video()

    def frame_forward(self):
        self.videoWidget.frame_forward()

    def frame_backward(self):
        self.videoWidget.frame_backward()

    def sec_forward(self):
        self.videoWidget.sec_forward()

    def sec_backward(self):
        self.videoWidget.sec_backward()

    def set_page(self, filename):
        self.videoWidget.load_video(filename, self.videoWidget.mediaPlayer.position())
        if self.isPlaying:
            self.videoWidget.play_video()

    def start_video(self, idx):
        self.isFirstOpen = True
        self.videoWidget.load_video(f'{Config.FILENAME}{idx}.{Config.FILEFORMAT}')

    def stop_video(self):
        pass