from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QShortcut, QVBoxLayout, QDialog, QLineEdit, QPushButton
from PyQt5.QtGui import QPixmap, QImage, QPalette, QKeySequence, QFont
from PyQt5.QtCore import Qt

from config import Config

class HomeScreen(QWidget):

    def __init__(self, parent=None, cams=None) -> None:
        super(HomeScreen, self).__init__(parent)

        # rtsp://<Username>:<Password>@<IP Address>:<Port>/cam/realmonitor?channel=1&subtype=0

        self.current_camera_idx = 0
        self.cams = cams
        self.is_recording = False

        self.shortcut = QShortcut(QKeySequence("1"), self)
        self.shortcut.activated.connect(lambda: self.setPage(0))

        self.shortcut = QShortcut(QKeySequence("2"), self)
        self.shortcut.activated.connect(lambda: self.setPage(1))

        self.shortcut = QShortcut(QKeySequence("3"), self)
        self.shortcut.activated.connect(lambda: self.setPage(2))

        self.shortcut = QShortcut(QKeySequence("4"), self)
        self.shortcut.activated.connect(lambda: self.setPage(3))

        self.shortcut = QShortcut(QKeySequence("E"), self)
        self.shortcut.activated.connect(self.toggle_recording)

        # Set up the main layout
        self.main_layout = QGridLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # Add camera widgets to the layout
        for cam in self.cams:
            self.main_layout.addWidget(cam.get_widget(), 0, 0)  # Assuming all cameras are displayed in the same area

        # "Not Recording" Overlay
        self.not_recording_label = QLabel("Not Recording", self)
        self.not_recording_label.setAlignment(Qt.AlignCenter)
        self.not_recording_label.setFont(QFont("Arial", 24))
        self.not_recording_label.setStyleSheet("color: red; background-color: rgba(0, 0, 0, 0.7); padding: 10px;")
        self.not_recording_label.setAttribute(Qt.WA_TransparentForMouseEvents, True)

        # Add the label to the main layout (above all other widgets)
        self.main_layout.addWidget(self.not_recording_label, 0, 0, alignment=Qt.AlignCenter)

        self.setLayout(self.main_layout)

        self.setPage(0)

    def setPage(self, id) -> None:
        for idx, cam in enumerate(self.cams):
            if cam.id == id:
                cam.show()
                self.current_camera_idx = cam.id

            else:
                cam.hide()

    def toggle_recording(self):
        if not self.is_recording:
            # Show dialog for file name input
            file_name_dialog = FileNameDialog(self)
            if file_name_dialog.exec_():
                Config.FILENAME = file_name_dialog.file_name
                self.start_recording()
        else:
            self.stop_recording()

    def start_recording(self):
        self.is_recording = True
        self.not_recording_label.hide()  # Hide "Not Recording" overlay
        # Start recording for each camera
        for i, cam in enumerate(self.cams):
            cam.start_recording()

    def stop_recording(self):
        self.is_recording = False
        self.not_recording_label.show()  # Show "Not Recording" overlay
        # Stop recording for each camera
        for cam in self.cams:
            cam.stop_recording()

    # Overwrite method closeEvent from class QMainWindow.
    def closeEvent(self, event) -> None:
        for cam in self.cams:
            cam.stop()

        # Accept the event
        event.accept()

class FileNameDialog(QDialog):
    def __init__(self, parent=None):
        super(FileNameDialog, self).__init__(parent)
        self.file_name = ""

        self.setWindowTitle("Enter FIght Number")
        self.setModal(True)

        # Dialog layout
        layout = QVBoxLayout()
        self.file_name_input = QLineEdit(self)
        layout.addWidget(self.file_name_input)

        submit_button = QPushButton("Submit", self)
        submit_button.clicked.connect(self.accept)
        layout.addWidget(submit_button)

        self.setLayout(layout)

    def accept(self):
        self.file_name = self.file_name_input.text()
        super(FileNameDialog, self).accept()