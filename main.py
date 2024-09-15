from PyQt5.QtWidgets import QApplication, QMainWindow, QShortcut, QStackedWidget, QLabel
from PyQt5.QtGui import QPixmap, QIcon, QKeySequence, QFont
from PyQt5 import QtCore
from PyQt5.QtCore import QTimer
import sys

from home_screen import HomeScreen
from settings_screen import SettingsScreen
from replay_screen import ReplayScreen
from cam import load_cams


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
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.setMinimumSize(800, 600)
        self.showMaximized()

        self.setWindowTitle("Taekwondo Video Replay")
        self.setWindowIcon(QIcon(QPixmap("camera_2.png")))

        self.cams = load_cams()

        self.home_widget = HomeScreen(self, self.cams)
        self.replay_widget = ReplayScreen(self)
        self.settings_widget = SettingsScreen(self)
        self.settings_widget.settings_saved.connect(self.apply_settings)
        self.central_widget.addWidget(self.home_widget)
        self.central_widget.addWidget(self.replay_widget)
        self.central_widget.addWidget(self.settings_widget)

        self.toast_label = QLabel("", self)
        self.toast_label.setAlignment(QtCore.Qt.AlignCenter)
        self.toast_label.setFont(QFont("Arial", 14))
        self.toast_label.setStyleSheet("color: white; background-color: rgba(0, 0, 0, 0.7); padding: 10px;")
        self.toast_label.setVisible(False)

    @QtCore.pyqtSlot()
    def toggle_settings(self):
        if self.home_widget.is_recording:
            self.show_toast_message("Settings can't be open while recording")
            return

        if self.central_widget.currentWidget() == self.settings_widget:
            self.central_widget.setCurrentWidget(self.home_widget)
            self.resume_recording()
        else:
            self.pause_recording()
            self.settings_widget.load_settings(self.cams)
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
        for cam in self.cams:
            cam.pause()

    def resume_recording(self):
        for cam in self.cams:
            cam.unpause()

    def apply_settings(self, settings):
        print("Applying new settings:", settings)

        # Update cameras based on settings
        for i, cam in enumerate(self.cams):
            cam.set_url(settings[i]['url'])
            cam.set_size(settings[i]['size'])
            cam.set_fps(settings[i]['fps'])

            print("here", i, settings[i]['url'])
            cam.stop()
            cam.start()

        print("here")
        self.toggle_settings()

    def show_toast_message(self, message):
        """Show a temporary toast message."""
        self.toast_label.setText(message)
        self.toast_label.adjustSize()
        self.toast_label.move(
            (self.width() - self.toast_label.width()) // 2,
            (self.height() - self.toast_label.height()) // 2
        )
        self.toast_label.setVisible(True)

        # Hide the toast after 2 seconds
        QTimer.singleShot(2000, lambda: self.toast_label.setVisible(False))


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
