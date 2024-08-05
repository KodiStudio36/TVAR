from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton


class SettingsScreen(QWidget):

    def __init__(self, parent=None):
        super(SettingsScreen, self).__init__(parent)
        layout = QHBoxLayout()
        layout.addWidget(QPushButton('logged in!'), 1)
        layout.addWidget(QPushButton('Not Stretching'), 0)
        self.setLayout(layout)