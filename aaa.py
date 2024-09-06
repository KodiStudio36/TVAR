import sys, os
from PyQt5.QtMultimediaWidgets import QGraphicsVideoItem
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QVBoxLayout, QWidget, QPushButton, QGraphicsRectItem
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, Qt, QRectF, QSizeF
from PyQt5.QtGui import QWheelEvent, QMouseEvent, QBrush, QColor

class VideoWidget(QGraphicsView):
    def __init__(self):
        super().__init__()

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

        # Load a video (replace with your video file path)
        video_url = QUrl.fromLocalFile(f"{os.path.dirname(__file__)}/filename0.avi")
        self.mediaPlayer.setMedia(QMediaContent(video_url))
        self.mediaPlayer.play()

        self.show()

    def resizeEvent(self, event):
        """ Resize the video item to maintain the aspect ratio 4:3 """
        view_width = self.size().width() - 2

        # Calculate the height for 4:3 aspect ratio
        view_height = view_width * 3 / 4

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

        # print(self.mapToScene(event.pos()))

        # print(self.width(), self.viewport().height())

        # self.centerOn()

    # def wheelEvent(self, event: QWheelEvent):
    #     """ Handle mouse wheel event to zoom in and out towards the mouse position """
    #     # Zoom in or out
    #     if event.angleDelta().y() > 0:
    #         self.zoom_in()
    #     else:
    #         self.zoom_out()

    #     # Get the position of the mouse in the scene after zooming
    #     offset = self.mapToScene(event.pos())

    #     # Adjust the scrollbars to keep the mouse position consistent
    #     self.horizontalScrollBar().setValue(int(self.horizontalScrollBar().value() + offset.x()))
    #     self.verticalScrollBar().setValue(int(self.verticalScrollBar().value() + offset.y()))

    def zoom_in(self):
        self.zoom_factor += 0.1
        self.setTransformAA()

    def zoom_out(self):
        if self.zoom_factor > 1.0:
            self.zoom_factor -= 0.1
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

        print(self.horizontalScrollBar().value(), self.verticalScrollBar().value())

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


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Layout for the main window
        layout = QVBoxLayout(self)

        # Create and add the video widget
        self.videoWidget = VideoWidget()
        layout.addWidget(self.videoWidget)

        # Create and add control buttons (e.g., play, pause)
        self.playButton = QPushButton("Play")
        self.playButton.clicked.connect(self.videoWidget.mediaPlayer.play)
        layout.addWidget(self.playButton)

        self.pauseButton = QPushButton("Pause")
        self.pauseButton.clicked.connect(self.videoWidget.mediaPlayer.pause)
        layout.addWidget(self.pauseButton)

        self.setLayout(layout)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

##############################################x

# class DraggableView(QGraphicsView):
#     def __init__(self):
#         super().__init__()
        
#         # Create a scene for the view
#         self.scene = QGraphicsScene(self)
#         self.setScene(self.scene)

#         # Set the background color or image (optional)
#         self.background_item = QGraphicsRectItem(QRectF(0, 0, 2000, 2000))  # Make it large enough for dragging
#         self.background_item.setBrush(QBrush(QColor(240, 240, 240)))  # Light gray background
#         self.scene.addItem(self.background_item)

#         # Add the video item
#         self.videoItem = QGraphicsVideoItem()
#         self.scene.addItem(self.videoItem)

#         # Set up the media player
#         self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
#         self.mediaPlayer.setVideoOutput(self.videoItem)

#         # Initial zoom factor
#         self.zoom_factor = 1.0

#         # Dragging variables
#         self.dragging = False
#         self.last_mouse_pos = None

#         # self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
#         # self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

#         # Load a video (replace with your video file path)
#         video_url = QUrl.fromLocalFile(f"{os.path.dirname(__file__)}/filename0.avi")
#         self.mediaPlayer.setMedia(QMediaContent(video_url))
#         self.mediaPlayer.play()

#         # Center the video item in the background rect
#         self.centerVideoItem()

#     def centerVideoItem(self):
#         """ Center the video item within the background rectangle """
#         self.show()
#         self.videoItem.setSize(QSizeF(self.size().width() - 31.5, self.size().width() / 16 * 9 - 31.5))

#         rect_center = self.background_item.boundingRect()
#         video_rect = self.videoItem.boundingRect()

#         print(rect_center.width(), rect_center.height())
#         print(video_rect.width(), video_rect.height())

#         # Calculate the top-left position to center the video item
#         top_left_x = rect_center.width() / 2 - video_rect.width() / 2
#         top_left_y = rect_center.height() / 2 - video_rect.height() / 2

#         # Set the position of the video item
#         self.videoItem.setPos(top_left_x, top_left_y)

#     #     self.updateScrollbars()

#     # def updateScrollbars(self):
#     #     """ Manually adjust scrollbar ranges after the view has been resized """
#     #     self.horizontalScrollBar().setRange(0, 1083)
#     #     self.verticalScrollBar().setRange(0, 1075)

#     #     # Center the scrollbars' values
#     #     self.horizontalScrollBar().setValue(1083 // 2)
#     #     self.verticalScrollBar().setValue(1075 // 2)

#     # def resizeEvent(self, event):
#     #     print(self.width(), self.height())
#         # """ Handle the resize event to reset scrollbars after resizing """
#         # super().resizeEvent(event)  # Call the base class implementation
#         # self.updateScrollbars()  # Adjust the scrollbars after resize

#     def wheelEvent(self, event: QWheelEvent):
#         """ Handle mouse wheel event to zoom in and out """
#         if event.angleDelta().y() > 0:
#             self.zoom_in()
#         else:
#             self.zoom_out()

#     def zoom_in(self):
#         self.zoom_factor += 0.1
#         self.setTransformAA()

#     def zoom_out(self):
#         if self.zoom_factor > 1.0:  # Prevent zooming out below initial scale
#             self.zoom_factor -= 0.1
#             self.setTransformAA()

#     def setTransformAA(self):
#         transform = self.transform()
#         transform.reset()  # Reset any previous transformations
#         transform.scale(self.zoom_factor, self.zoom_factor)
#         self.setTransform(transform)

#     def mousePressEvent(self, event: QMouseEvent):
#         """ Handle mouse press event for dragging """
#         if event.button() == Qt.LeftButton:
#             self.dragging = True
#             self.last_mouse_pos = event.pos()

#         print(self.horizontalScrollBar().value(), self.verticalScrollBar().value())

#     def mouseMoveEvent(self, event: QMouseEvent):
#         """ Handle mouse move event for dragging """
#         if self.dragging:
#             # Calculate how much the mouse moved
#             delta = event.pos() - self.last_mouse_pos
#             self.last_mouse_pos = event.pos()

#             # Scroll the scene by the delta
#             self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta.x())
#             self.verticalScrollBar().setValue(self.verticalScrollBar().value() - delta.y())

#     def mouseReleaseEvent(self, event: QMouseEvent):
#         """ Handle mouse release event to stop dragging """
#         if event.button() == Qt.LeftButton:
#             self.dragging = False

# class MainWindow(QWidget):
#     def __init__(self):
#         super().__init__()

#         # Layout for the main window
#         layout = QVBoxLayout(self)

#         # Create and add the draggable view
#         self.draggableView = DraggableView()
#         layout.addWidget(self.draggableView)

#         # Create and add control buttons (e.g., play, pause)
#         self.playButton = QPushButton("Play")
#         self.playButton.clicked.connect(self.draggableView.mediaPlayer.play)
#         layout.addWidget(self.playButton)

#         self.pauseButton = QPushButton("Pause")
#         self.pauseButton.clicked.connect(self.draggableView.mediaPlayer.pause)
#         layout.addWidget(self.pauseButton)

#         self.setLayout(layout)

# def main():
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec_())

# if __name__ == "__main__":
#     main()