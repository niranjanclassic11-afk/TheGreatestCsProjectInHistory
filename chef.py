import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from productTableModel import *

index1, index2 = 1,2
headers = ["Order ID", "Name", "Item code", "Quantity", "Done"]

class chefView(QWidget):
    def __init__(self, call_handler):
        super().__init__()
        self.call_handler = call_handler
        self.formUI()
        self.setMinimumWidth(1200)
        self.setMinimumHeight(600)
    def updateTable(self):
        self.table_model.update_all_data(self.call_handler.get_chef_data())

    def formUI(self):
        self.mainlayout = QVBoxLayout()
        self.table = QTableView()
        self.table = betterTable(self.table)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setFont(QFont("arial", 40))
        self.label.setText("CHEF VIEW")
        self.mainlayout.addWidget(self.label)

        self.table_model = ProductTableModel(self.call_handler.get_chef_data(), headers, lambda order_id, item_code: self.markItemFinish(order_id, item_code), checkBoxColumnNumber=4)
        self.table_model.IDIndex = 0
        self.table_model.Index1 = 2
        self.table.setModel(self.table_model)
        self.mainlayout.addWidget(self.table)
        self.setLayout(self.mainlayout)

    def markItemFinish(self, order_id, item_code):
        self.call_handler.mark_item_finished(order_id, item_code)


if __name__ == "__main__":
    print("Execute main_manager.py instead")

