import sys
import mysql.connector as connector
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from productTableModel import *

paymentsHeader = ["Order no", "Price", "Status", "Paid"]

def getReceiptData(orderid): #connect this to call handler see line 56
    return [["Dosa", "1290", "78", "Price"]]

def showReceipt(order_id, data):
    data_headers = ["Item name", "Item price", "Quantity", "Price"]
    dialog = QDialog()
    dialog.setWindowTitle("Order id:" + str(order_id))
    layout = QVBoxLayout()
    table = QTableView()
    table.setStyleSheet(TABLESTYLE)
    table = betterTable(table)
    table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
    tableModel = BasicTableModel(data, data_headers)
    table.setModel(tableModel)
    layout.addWidget(table)
    label = QLabel()
    label.setText("Total Price:"+str(780))
    label.setAlignment(Qt.AlignmentFlag.AlignLeft)
    label.setStyleSheet("QLabel{font-family:arial; font-size: 18px;}")
    layout.addWidget(label)
    dialog.setLayout(layout)
    dialog.exec()

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
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tableModel = ProductTableModel(self.call_handler.get_cashier_data(), paymentsHeader, lambda y, a:self.paid(y), checkBoxColumnNumber=3)
        self.tableModel.IDIndex = 0
        self.table.setModel(self.tableModel)

        self.vlayout.addWidget(self.table)

    def paid(self, order_id):
        ##dial = QMessageBox()
        ##dial.setText("Order was paid!!!!!!")
        ##dial.exec()
        showReceipt(order_id, getReceiptData(order_id))
        self.call_handler.cash_paid(order_id)

    def updateTable(self):
        self.tableModel.update_all_data(self.call_handler.get_cashier_data())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwidget = QMainWindow()
    widget = cashierView()
    mainwidget.setCentralWidget(widget)
    mainwidget.showMaximized()
    sys.exit(app.exec())
