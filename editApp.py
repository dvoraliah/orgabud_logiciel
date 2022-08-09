import requests
from PyQt6.QtWidgets import QLabel, QWidget, QPushButton, QGridLayout, \
    QSizePolicy, QComboBox
from requests.structures import CaseInsensitiveDict

import loggedApp


class EditApp(QWidget):
    def __init__(self, token, id_updated, pseudo, email):
        super().__init__()

        self.status_changed = None
        self.comboBox = None
        self.email = email
        self.pseudo = pseudo
        self.mainApp = None
        self.id_updated = id_updated
        self.users_request = 'http://5.39.76.125/dvoraliah/orgabud-website/public/index.php/api/users'
        self.token = token
        self.headers = CaseInsensitiveDict()
        self.headers["Accept"] = "application/json"
        self.headers["Authorization"] = "Bearer " + token
        self.resize(600, 200)
        self.setStyleSheet('font-size: 15px, font-')
        self.setWindowTitle("Editer l'utilisateur id " + self.id_updated)
        self.form_update()

    def after_save(self):
        api_url = 'http://5.39.76.125/dvoraliah/orgabud-website/public/index.php/api/users/' + str(self.id_updated)
        response_API = requests.put(api_url, headers=self.headers, data={'status_id': self.status_changed})
        response_statut = response_API.status_code
        response_json = response_API.json()
        if response_statut == 200:
            self.mainApp = loggedApp.MainApp(self.token)
            self.mainApp.show()
            self.close()
        else:
            print("La mise à jour du statut est impossible. Erreur " + str(response_statut))

    def form_update(self):
        self.comboBox = QComboBox()
        self.comboBox.addItems(["Selectionner","User", "Premium", "Admin"])
        self.comboBox.currentIndexChanged.connect(self.selection_change)
        layout = QGridLayout()
        self.setLayout(layout)
        labels = {}
        labels['pseudo'] = QLabel(self.pseudo)
        labels['statut'] = QLabel('statut')
        labels['email'] = QLabel(self.email)
        labels['pseudo'].setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        labels['statut'].setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        labels['email'].setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        layout.addWidget(labels['pseudo'], 0, 3, 1, 1)
        layout.addWidget(labels['email'], 1, 3, 1, 1)
        layout.addWidget(labels['statut'], 2, 0, 1, 1)
        button_save = QPushButton('&Save', clicked=self.after_save)
        layout.addWidget(self.comboBox, 2, 3, 1, 1)
        layout.addWidget(button_save, 3, 3, 1, 1)

    def selection_change(self):
        print("selection changed ", self.comboBox.currentText())
        if self.comboBox.currentText() == "Admin":
            self.status_changed = 3
        elif self.comboBox.currentText() == "Premium":
            self.status_changed = 2
        else:
            self.status_changed = 1
