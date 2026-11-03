import sys
import mysql.connector as connector
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from productTableModel import *

paymentsHeader = ["Order no", "Price", "Status", "Paid"]

class cashierView(QWidget):
    def __init__(self, call_handler) -> None:
        super().__init__()
        self.call_handler = call_handler
        self.vlayout = QVBoxLayout()
        self.setLayout(self.vlayout)
        self.formUI()

    def formUI(self):
        self.label = QLabel()
        self.label.setText("CASHIER VIEW")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setFont(QFont("arial", 60))
        self.vlayout.addWidget(self.label)

        self.table = QTableView()
        self.table=betterTable(self.table)
        width = QGuiApplication.primaryScreen().size().width()
        self.table.horizontalHeader().setDefaultSectionSize(width//4 - 7)
        self.tableModel = ProductTableModel(self.call_handler.get_cashier_data(), paymentsHeader, lambda y, a:self.paid(y), checkBoxColumnNumber=3)
        self.tableModel.IDIndex = 0
        self.table.setModel(self.tableModel)

        self.vlayout.addWidget(self.table)

    def paid(self, order_id):
        ##dial = QMessageBox()
        ##dial.setText("Order was paid!!!!!!")
        ##dial.exec()
        self.call_handler.cash_paid(order_id)

    def updateTable(self):
        self.tableModel.update_all_data(self.call_handler.get_cashier_data())

if __name__ == "__main__":
    print("Execute main_manager.py instead")

