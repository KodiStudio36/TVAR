from PyQt5.QtWidgets import QApplication, QMainWindow, QShortcut, QStackedWidget
from PyQt5.QtGui import QPixmap, QIcon, QKeySequence
from PyQt5 import QtCore
import sys

from home_screen import HomeScreen
from settings_screen import SettingsScreen
from replay_screen import ReplayScreen


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.shortcut = QShortcut(QKeySequence("S"), self)
        self.shortcut.activated.connect(self.toggle_settings)

        self.shortcut = QShortcut(QKeySequence("R"), self)
        self.shortcut.activated.connect(self.toggle_replay)

        self.central_widget = QStackedWidget()
        # Set the central widget.
        self.setCentralWidget(self.central_widget)
        self.setMinimumSize(800, 600)
        self.showMaximized()

        self.setWindowTitle("Taekwondo Video Replay")
        self.setWindowIcon(QIcon(QPixmap("camera_2.png")))

        self.home_widget = HomeScreen(self)
        self.replay_widget = ReplayScreen(self)
        self.settings_widget = SettingsScreen(self)
        self.central_widget.addWidget(self.home_widget)
        self.central_widget.addWidget(self.replay_widget)
        self.central_widget.addWidget(self.settings_widget)

    @QtCore.pyqtSlot()
    def toggle_settings(self):
        if self.central_widget.currentWidget() == self.settings_widget:
            self.central_widget.setCurrentWidget(self.home_widget)
            self.resume_recording()
        else:
            self.pause_recording()
            self.central_widget.setCurrentWidget(self.settings_widget)

    @QtCore.pyqtSlot()
    def toggle_replay(self):
        if self.central_widget.currentWidget() == self.replay_widget:
            self.central_widget.setCurrentWidget(self.home_widget)
            self.replay_widget.stop_video()
            self.resume_recording()
        else:
            self.pause_recording()
            self.replay_widget.start_video(self.home_widget.current_camera_idx)
            self.central_widget.setCurrentWidget(self.replay_widget)

    def pause_recording(self):
        for cam in self.home_widget.cams:
            cam.CaptureIpCameraFramesWorker.pause()

    def resume_recording(self):
        for cam in self.home_widget.cams:
            cam.CaptureIpCameraFramesWorker.unpause()


def main() -> None:
    # Create a QApplication object. It manages the GUI application's control flow and main settings.
    # It handles widget specific initialization, finalization.
    # For any GUI application using Qt, there is precisely one QApplication object
    app = QApplication(sys.argv)
    # Create an instance of the class MainWindow.
    window = MainWindow()
    # Show the window.
    window.show()
    # Start Qt event loop.
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
