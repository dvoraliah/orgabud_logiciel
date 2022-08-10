import sys
import os
import time
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QLabel, QGridLayout, QSizePolicy
from PyQt6.QtGui import QIcon
from PyQt6.QtSql import QSqlDatabase, QSqlQuery
from loggedApp import MainApp
import requests

'''
Fichier qui génère l'interface de connexion et appelle la fenêtre principale si l'utilisateur authentifié est admin
'''


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.response_json = None
        self.mainApp = None
        self.response_text = None
        self.response_statut = None
        self.response_API = None
        self.api_url = None
        self.setWindowTitle('Login')
        self.setWindowIcon(QIcon(''))
        self.window_width, self.window_height = 600, 200
        self.setFixedSize(self.window_width, self.window_height)

        layout = QGridLayout()
        self.setLayout(layout)

        labels = {}
        self.lineEdits = {}

        labels['Username'] = QLabel('Username')
        labels['Password'] = QLabel('Password')
        labels['Username'].setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        labels['Password'].setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.lineEdits['Username'] = QLineEdit()
        self.lineEdits['Password'] = QLineEdit()
        self.lineEdits['Password'].setEchoMode(QLineEdit.EchoMode.Password)

        layout.addWidget(labels['Username'], 0, 0, 1, 1)
        layout.addWidget(self.lineEdits['Username'], 0, 1, 1, 3)

        layout.addWidget(labels['Password'], 1, 0, 1, 1)
        layout.addWidget(self.lineEdits['Password'], 1, 1, 1, 3)

        button_login = QPushButton('&Log In', clicked=self.checkCredential)
        layout.addWidget(button_login, 2, 3, 1, 1)

        self.status = QLabel('')
        self.status.setStyleSheet('font-size: 25px; color: red;')
        layout.addWidget(self.status, 3, 0, 1, 3)

        self.login_generate()

    def login_generate(self):
        self.status.setText('')

    def checkCredential(self):
        username = self.lineEdits['Username'].text()
        password = self.lineEdits['Password'].text()

        self.api_url = 'http://5.39.76.125/dvoraliah/orgabud-website/public/index.php/api/login'
        self.response_API = requests.post(self.api_url, data={'email': username, 'password': password})
        # self.response_API = requests.post(self.api_url, data={'email': "admin@test.fr", 'password': "anya"})
        self.response_statut = self.response_API.status_code
        self.response_text = self.response_API.text
        self.response_json = self.response_API.json()

        if self.response_statut == 201:
            if self.response_json["user"]["status_id"] == 3:
                time.sleep(1)
                self.mainApp = MainApp(self.response_json["token"])
                self.mainApp.show()
                self.close()
            else:
                self.status.setText("Droits Insuffisants")
        else:
            self.status.setText("Email ou Mot de passe incorrect")


if __name__ == '__main__':
    # don't auto-scale when drag app to a different monitor.
    # QApplication.setAttribute(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

    app = QApplication(sys.argv)
    app.setStyleSheet('''
        QWidget {
            font-size: 25px;
        }
        QLineEdit {
            height: 200px;
        }
    ''')

    loginWindow = LoginWindow()
    loginWindow.show()

    try:
        sys.exit(app.exec())
    except SystemExit:
        print('Closing Window...')
