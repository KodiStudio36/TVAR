from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QFormLayout, QVBoxLayout, QPushButton

# class SettingsScreen(QWidget):

#     def __init__(self, parent=None, home_widget=None):
#         super(SettingsScreen, self).__init__(parent)

#         layout = QHBoxLayout(self)

#         vboxLayout = QVBoxLayout(self)

#         vboxLayout.addWidget(QPushButton('logged in!'), 0)
#         vboxLayout.addWidget(QPushButton('logged in!'), 0)
#         vboxLayout.addWidget(QPushButton('logged in!'), 1)

#         layout.addLayout(vboxLayout, 1)
#         layout.addWidget(QPushButton('Not Stretching'), 0)

#         self.setLayout(layout)
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QFormLayout, QVBoxLayout, QPushButton
from PyQt5.QtCore import pyqtSignal

class SettingsScreen(QWidget):
    settings_saved = pyqtSignal(list)  # Define a signal that emits a dictionary of settings

    def __init__(self, parent=None):
        super(SettingsScreen, self).__init__(parent)

        # Main Layout
        main_layout = QVBoxLayout(self)

        # Camera Settings Form
        self.camera_forms = []
        for i in range(1, 5):  # 4 cameras
            camera_form = self.create_camera_form(f"Camera {i}")
            main_layout.addLayout(camera_form[0])
            self.camera_forms.append(camera_form[1])  # Store the input fields reference

        # Save Button
        save_button = QPushButton("Save Settings")
        save_button.clicked.connect(self.save_settings)
        main_layout.addWidget(save_button)

        self.setLayout(main_layout)

    def create_camera_form(self, camera_name):
        """Creates a form layout for each camera with inputs for URL, width, height, and FPS."""
        form_layout = QFormLayout()

        # Camera Label
        form_layout.addRow(QLabel(camera_name))

        # URL Input
        url_input = QLineEdit()
        form_layout.addRow("URL:", url_input)

        # Width Input
        width_input = QLineEdit()
        form_layout.addRow("Width:", width_input)

        # Height Input
        height_input = QLineEdit()
        form_layout.addRow("Height:", height_input)

        # FPS Input
        fps_input = QLineEdit()
        form_layout.addRow("FPS:", fps_input)

        # Return both layout and data dictionary
        return form_layout, {
            "url": url_input,
            "width": width_input,
            "height": height_input,
            "fps": fps_input
        }
    
    def load_settings(self, cams):
        for i, cam in enumerate(cams):
            if cam.url is not None:
                self.camera_forms[i]["url"].setText(str(cam.url))

            if cam.size is not None:
                self.camera_forms[i]["width"].setText(str(cam.size[0]))
                self.camera_forms[i]["height"].setText(str(cam.size[1]))

            if cam.fps is not None:
                self.camera_forms[i]["fps"].setText(str(cam.fps))

    def save_settings(self):
        """Handles the save button click, retrieving values from all input fields."""
        preferences = []
        for i, inputs in enumerate(self.camera_forms):
            if inputs["url"].text() != "":
                if inputs["url"].text().isdigit():
                    url = int(inputs["url"].text())

                else:
                    url = inputs["url"].text()

            else:
                url = None

            width = int(inputs["width"].text()) if inputs["width"].text().isdigit() else None
            height = int(inputs["height"].text()) if inputs["height"].text().isdigit() else None
            size = [width, height] if width != None and height != None else None

            preferences.append({
                "url": url,
                "id": i,
                "size": size,
                "fps": int(inputs["fps"].text()) if inputs["fps"].text().isdigit() else None
            })

        # Emit the signal with the settings dictionary
        self.settings_saved.emit(preferences)
