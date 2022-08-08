from PyQt6.QtWidgets import QLabel, QWidget


class MainApp(QWidget):
    def __init__(self, token):
        super().__init__()
        self.token = token
        self.resize(800, 600)
        label = QLabel('Main App', parent=self)
