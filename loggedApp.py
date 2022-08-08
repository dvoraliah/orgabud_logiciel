import requests
from PyQt6.QtWidgets import QLabel, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton
from requests.structures import CaseInsensitiveDict


class MainApp(QWidget):
    def __init__(self, token):
        super().__init__()

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
        self.resize(850, 600)
        self.setStyleSheet('font-size: 15px, font-')
        label = QLabel('', parent=self)
        self.data_users()

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)

    def data_users(self):
        self.response_API = requests.get(self.users_request, headers=self.headers)
        self.response_json = self.response_API.json()
        self.tableWidget = QTableWidget(len(self.response_json), 5)
        self.tableWidget.setHorizontalHeaderLabels(['id', 'Pseudo', 'Email', 'Editer', 'X'])
        self.tableWidget.horizontalHeader().setDefaultSectionSize(300)

        for i in range(len(self.response_json)):
            self.tableWidget.setItem(i, 0, QTableWidgetItem(str(self.response_json[i]["id"])))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(self.response_json[i]["name"]))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(self.response_json[i]["email"]))
            self.button_edit = QPushButton('edit')
            self.button_edit.button_row = i
            self.button_edit.button_column = 3
            self.button_edit.clicked.connect(self.button_update_clicked)
            self.tableWidget.setCellWidget(i, 3, self.button_edit)
            self.button_delete = QPushButton('suppr')
            self.button_delete.button_row = i
            self.button_delete.button_column = 4
            self.button_delete.clicked.connect(self.button_delete_clicked)
            self.tableWidget.setCellWidget(i, 4, self.button_delete)
        self.tableWidget.setColumnWidth(0, 20)
        self.tableWidget.setColumnWidth(3, 80)
        self.tableWidget.setColumnWidth(4, 80)

        # button.show()

    def button_update_clicked(self):
        button = self.sender()
        print(button.button_row)
        print(button.button_column)

    def button_delete_clicked(self):
        button = self.sender()
        print(button.button_row)
        print(button.button_column)
