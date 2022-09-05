import requests
from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton, QDialog, \
    QDialogButtonBox
from requests.structures import CaseInsensitiveDict

from customDialog import CustomDialog
from editApp import EditApp


class MainApp(QWidget):
    def __init__(self, token):
        super().__init__()

        self.editApp = None
        self.window = None
        self.id_obj = None
        self.button_delete = None
        self.button_edit = None
        self.tableWidget = None
        self.response_json = None
        self.response_API = None
        self.users_request = 'http://5.39.76.125/dvoraliah/orgabud-website/public/index.php/api/users'
        self.token = token
        self.headers = CaseInsensitiveDict()
        self.headers["Accept"] = "application/json"
        self.headers["Authorization"] = "Bearer " + token
        self.resize(950, 600)
        self.setStyleSheet('font-size: 15px, font-')
        self.setWindowTitle('Gestion des utilisateurs')
        label = QLabel('', parent=self)
        self.data_users()

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)

    def data_users(self):
        self.response_API = requests.get(self.users_request, headers=self.headers)
        self.response_json = self.response_API.json()
        self.tableWidget = QTableWidget(len(self.response_json), 6)
        self.tableWidget.setHorizontalHeaderLabels(['id', 'Pseudo', 'Email', 'Statut', 'Editer', 'X'])
        self.tableWidget.horizontalHeader().setDefaultSectionSize(300)

        for i in range(len(self.response_json)):
            if self.response_json[i]["status_id"] == 1:
                status = "User"
            elif self.response_json[i]["status_id"] == 2:
                status = "Premium"
            else:
                status = "Admin"

            self.tableWidget.setItem(i, 0, QTableWidgetItem(str(self.response_json[i]["id"])))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(self.response_json[i]["name"]))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(self.response_json[i]["email"]))
            self.tableWidget.setItem(i, 3, QTableWidgetItem(status))
            self.button_edit = QPushButton('edit')
            self.button_edit.id_obj = str(self.response_json[i]["id"])
            self.button_edit.pseudo_row = str(self.response_json[i]["name"])
            self.button_edit.email_row = str(self.response_json[i]["email"])
            self.button_edit.button_row = i
            self.button_edit.button_column = 4
            self.button_edit.clicked.connect(self.button_update_clicked)
            self.tableWidget.setCellWidget(i, 4, self.button_edit)
            self.button_delete = QPushButton('suppr')
            self.button_delete.id_obj = self.response_json[i]["id"]
            self.button_delete.button_row = i
            self.button_delete.button_column = 5
            self.button_delete.clicked.connect(self.button_delete_clicked)
            self.tableWidget.setCellWidget(i, 5, self.button_delete)
        self.tableWidget.setColumnWidth(0, 20)
        self.tableWidget.setColumnWidth(3, 80)
        self.tableWidget.setColumnWidth(4, 80)
        self.tableWidget.setColumnWidth(5, 80)

        # button.show()

    def button_update_clicked(self):
        """
        Fonction d'update après le click sur bouton dédié

        """
        button = self.sender()
        print(button.button_row)
        print(button.button_column)
        print(button.id_obj)
        self.editApp = EditApp(self.token, str(button.id_obj), button.pseudo_row, button.email_row)
        self.editApp.show()
        self.close()

    def button_delete_clicked(self):
        """
        Fonction de suppression après le click sur le bouton dédié
        récupère l'id pour la suppression en database
        et la row pour la suppression de la ligne
        """
        QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        dlg = CustomDialog(self)
        if dlg.exec():
            button = self.sender()
            api_url = 'http://5.39.76.125/dvoraliah/orgabud-website/public/index.php/api/users/' + str(button.id_obj)
            response_API = requests.delete(api_url, headers=self.headers)
            response_statut = response_API.status_code

            if response_statut == 200:
                self.tableWidget.removeRow(button.button_row)
                self.data_users()

