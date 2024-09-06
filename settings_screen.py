from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QVBoxLayout


class SettingsScreen(QWidget):

    def __init__(self, parent=None):
        super(SettingsScreen, self).__init__(parent)

        layout = QHBoxLayout(self)

        vboxLayout = QVBoxLayout(self)

        vboxLayout.addWidget(QPushButton('logged in!'), 0)
        vboxLayout.addWidget(QPushButton('logged in!'), 0)
        vboxLayout.addWidget(QPushButton('logged in!'), 1)

        layout.addLayout(vboxLayout, 1)
        layout.addWidget(QPushButton('Not Stretching'), 0)

        self.setLayout(layout)