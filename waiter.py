import sys
import random
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import mysql.connector as connector
from productTableModel import *


headers = ["UUID", "Tableno", "Itemcode", "Status", "ordertime"] #For more columns just adjust the headers all depends  on the data you give
class waiterView(QWidget):
    def __init__(self, call_handler) -> None:
        self.call_handler = call_handler
        font = QFont("arial", 17)
        font.setLetterSpacing(QFont.SpacingType.PercentageSpacing, 115.0);
        font.setWordSpacing(5)
        super().__init__()
        self.mainlayout = QVBoxLayout()
        self.Font = font
        self.ui()
        self.setLayout(self.mainlayout)
        self.setFont(font)
        self.items = []

    def ui(self):
        self.label = QLabel()
        self.label.setText("WAITER")
        self.label.setFont(QFont("arial", 40))
        self.label.setMaximumHeight(50)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mainlayout.addWidget(self.label)
        self.sideLayout = QHBoxLayout()

        self.ItemNameLayout = QVBoxLayout()
        self.ItemNameLabel = QLabel()
        self.ItemNameLabel.setText("Item name")
        self.ItemNameLayout.addWidget(self.ItemNameLabel)
        self.itemNameComboBox = QComboBox()
        self.itemNameComboBox.addItems(self.call_handler.get_item_names())
        self.itemNameTable = QTableWidget()
        self.itemNameTable.setMaximumWidth(300)
        self.itemNameTable.verticalHeader().hide()
        self.itemNameTable.horizontalHeader().hide()
        self.itemNameTable.setColumnCount(1)
        self.itemNameTable.setAlternatingRowColors(True)
        self.itemNameTable.verticalHeader().setDefaultSectionSize(65)
        self.ItemNameLayout.addWidget(self.itemNameComboBox)
        self.ItemNameLayout.addWidget(self.itemNameTable)
        self.sideLayout.addLayout(self.ItemNameLayout)

        self.ItemCodeLayout = QVBoxLayout()
        self.ItemCodeLabel = QLabel()
        self.ItemCodeLabel.setText("Item Code")
        self.itemCodeComboBox = QComboBox()
        item_codes = [str(i) for i in self.call_handler.get_item_codes()]
        self.itemCodeComboBox.addItems(item_codes)
        self.itemCodeTable = QTableWidget()
        self.itemCodeTable.setMaximumWidth(300)
        self.itemCodeTable.verticalHeader().hide()
        self.itemCodeTable.setAlternatingRowColors(True)
        self.itemCodeTable.horizontalHeader().hide()
        self.itemCodeTable.verticalHeader().setDefaultSectionSize(65)
        self.itemCodeTable.setColumnCount(1)
        self.ItemCodeLayout.addWidget(self.ItemCodeLabel)
        self.ItemCodeLayout.addWidget(self.itemCodeComboBox)
        self.ItemCodeLayout.addWidget(self.itemCodeTable)
        self.itemCodeComboBox.currentIndexChanged.connect(self.codeComboBoxWasClicked)
        self.itemNameComboBox.currentIndexChanged.connect(self.nameComboBoxWasClicked)
        self.sideLayout.addLayout(self.ItemCodeLayout)

        self.quanitityLayout = QVBoxLayout() #change the spelling
        self.quanitityLabel = QLabel()
        self.quanitityLabel.setText("Quantity")
        self.quanitityLayout.addWidget(self.quanitityLabel)
        self.quantityInput = QComboBox()
        self.quantityInput.addItems([str(i) for i in range(1, 21)])
        self.itemQuantityTable = QTableWidget()
        self.itemQuantityTable.setMaximumWidth(300)
        self.itemQuantityTable.verticalHeader().setDefaultSectionSize(65)
        self.itemQuantityTable.setAlternatingRowColors(True)
        self.itemQuantityTable.verticalHeader().hide()
        self.itemQuantityTable.horizontalHeader().hide()
        self.itemQuantityTable.setColumnCount(1)
        self.quanitityLayout.addWidget(self.quantityInput)
        self.sideLayout.addLayout(self.quanitityLayout)
        self.quanitityLayout.addWidget(self.itemQuantityTable)
        self.mainlayout.addLayout(self.sideLayout)

        self.addButton = QPushButton()
        self.addButton.setText("Add item")
        self.addButton.clicked.connect(self.addButtonClicked)
        self.addButton.setMinimumHeight(80)
        self.addButton.setStyleSheet(BUTTONSTYLE)
        self.mainlayout.addWidget(self.addButton)

        self.placeOrderButton = QPushButton()
        self.placeOrderButton.setText("Place Order")
        self.placeOrderButton.setMinimumHeight(80)
        self.placeOrderButton.setStyleSheet(BUTTONSTYLE)
        self.placeOrderButton.clicked.connect(self.ordered)
        self.mainlayout.addWidget(self.placeOrderButton)

    def addButtonClicked(self):
        row = self.itemCodeTable.rowCount()
        self.itemCodeTable.insertRow(row)
        self.itemCodeTable.setItem(row, 0, QTableWidgetItem(self.itemCodeComboBox.currentText()))
        self.itemNameTable.insertRow(row)
        self.itemNameTable.setItem(row, 0, QTableWidgetItem(self.itemNameComboBox.currentText()))
        self.itemQuantityTable.insertRow(row)
        self.itemQuantityTable.setItem(row, 0, QTableWidgetItem(self.quantityInput.currentText()))

        self.items.append([int(self.itemCodeComboBox.currentText()), int(self.quantityInput.currentText())])

    def codeComboBoxWasClicked(self):
        index = self.getItemNameWithItemCode(self.itemCodeComboBox.currentText())
        self.itemNameComboBox.setCurrentIndex(index)
    
    def nameComboBoxWasClicked(self):
        index = self.getItemCodeWithItemName(self.itemNameComboBox.currentText())
        self.itemCodeComboBox.setCurrentIndex(index)
    
    def getItemNameWithItemCode(self, itemCode:str):
        itemCodes = self.call_handler.get_item_codes()
        index = itemCodes.index(int(itemCode))
        return index #return the index of the itemname in the result of getItemNames

    def getItemCodeWithItemName(self, itemName:str):
        itemNames = self.call_handler.get_item_names()
        index = itemNames.index(itemName)
        return index #return the index of the itemcode in the result of getItemCodes



    def ordered(self):
        items_dict = {}
        for pair in self.items:
            if pair[0] in items_dict:
                items_dict[pair[0]] += pair[1]
            else: items_dict[pair[0]] = pair[1]
        self.call_handler.on_order_placed(items_dict)
        self.items = []
        self.itemNameTable.setRowCount(0)
        self.itemCodeTable.setRowCount(0)
        self.itemQuantityTable.setRowCount(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwidget = QMainWindow()
    connection = None
    widget = waiterView()
    widget.setMaximumWidth(1000)
    widget.setMinimumHeight(800)
    mainwidget.setCentralWidget(widget)
    mainwidget.show()
    sys.exit(app.exec())
