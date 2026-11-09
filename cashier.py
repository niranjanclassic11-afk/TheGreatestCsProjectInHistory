import sys
import mysql.connector as connector
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import pandas
from productTableModel import *

paymentsHeader = ["Order no", "Price", "Status", "Paid"]

def showReceipt(order_id, data):
    data_headers = ["Item name", "Item price", "Quantity", "Price"]
    dialog = QDialog()
    dialog.setWindowTitle("Order id:" + str(order_id))
    layout = QVBoxLayout()

    nameLabel = QLabel()
    nameLabel.setText("<h1>Hotel</h1>\n<h2>Address</h2>Receipt")
    nameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.addWidget(nameLabel)

    pandasLabel = QLabel()
    pan = pandas.DataFrame(data[0])
    pan.columns = data_headers
    pandasLabel.setText("\n"+str(pan))
    pandasLabel.setFont(QFont("consolas", 15))
    layout.addWidget(pandasLabel)

    """table = QTableView()
    table.setStyleSheet(TABLESTYLE)
    table = betterTable(table)
    table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
    tableModel = BasicTableModel(data, data_headers)
    table.setModel(tableModel)
    layout.addWidget(table)"""

    label = QLabel()
    label.setText("Total Price:"+str(data[1]))
    label.setAlignment(Qt.AlignmentFlag.AlignRight)
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
        showReceipt(order_id, self.call_handler.get_receipt_data(order_id))
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
