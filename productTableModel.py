from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

DEFAULT_SECTION_SIZE = 80

BUTTONSTYLE = """
QPushButton{
    background-color: #525c5e;
    font-family:arial;
    font-size: 20px;
    font-weight:bold;
}
QPushButton:hover{
    background-color: #32484d;
}
"""
# In the 18th line ther is "checkmark.png" u can change that to any other image
TABLESTYLE = """
QTableView::indicator {
    width: 30;
    height: 30;
    border: 3px solid #555555;
    border-radius: 20px;
    background-color: #525c5e;
}
QTableView::indicator:hover {
    background-color: #32484d;
}
QTableView::indicator:checked {
 /*   background-color: #0078d7;*/
    /*border-color: #005a9e;*/
    image: url(checkmark.png);
}


QTableWidget {
    background-color: #161a23;
    alternate-background-color: #1b202b;

    color: #e8ecf3;

    border: 1px solid #2a3040;
    border-radius: 20px;       /* Pill shape */

    gridline-color: #292f3d;

    selection-background-color: #3b82f6;

    outline: none;

}


QTableCornerButton::section {
    background-color: #202633;
    border: none;
    border-bottom: 1px solid #2a3040;
    border-right: 1px solid #2a3040;
}


QHeaderView::section {
    background-color: #98909a;

    color: #ebeceb;

    border: none;
    border-bottom: 1px solid #303747;

    padding: 12px 14px;

    font-size: 20px;
    font-weight: 600;
}

QHeaderView::section:hover {
    background-color: #272e3c;
    color: #ffffff;
}

QHeaderView::section:first {
    border-top-left-radius: 10px;
}

/* Last header cell */
QHeaderView::section:last {
    border-top-right-radius: 10px;
}
QPushButton#primaryButton {
    background-color: #000000; /* Dark black background */
    color: #ffffff;            /* High-contrast white text */
    border: 1px solid #3c4043;  /* Subtle dark border for structure */
    font-family:arial;
    font-size:15px;
    border-radius: 20px;       /* Pill shape */
    padding: 8px 20px;
    min-height: 20px;
}

QPushButton#primaryButton:hover {
    background-color: #202124; /* Dark gray highlight on hover */
    border-color: #5f6368;
}

QPushButton#primaryButton:pressed {
    background-color: #303134; /* Slightly lighter gray when pressed */
}

QPushButton#primaryButton:disabled {
    background-color: #121212;
    color: #5f6368;
    border-color: #202124;
}


QHeaderView::section:vertical {
    background-color: #1c212c;

    color: #7f8a9d;

    border: none;
    border-right: 1px solid #292f3d;

    padding: 8px;
}


QTableWidget::item {
    padding: 10px 12px;

    border-radius: 20px;
    border-bottom: 1px solid #252b38;
}

QTableWidget::item:hover {
    background-color: #252c3a;
}

QTableWidget::item:selected {
    background-color: #2563eb;
    color: #ffffff;
}

/* Selected row while inactive */
QTableWidget::item:selected:!active {
    background-color: #334155;
    color: #e8ecf3;
}
        """

def betterTable(table:QTableView):
    table.setStyleSheet(TABLESTYLE)
    font = QFont("corbel", 18)
    table.setFont(font)
    table.horizontalHeader().setDefaultSectionSize(400)
    table.verticalHeader().setDefaultSectionSize(DEFAULT_SECTION_SIZE)
    table.setAlternatingRowColors(True)
    return table

class ProductTableModel(QAbstractTableModel):
    IDIndex = 1 # the id which u want to get when the checkbox is checked. Don;t change it here
    def __init__(self, data, headers, func, checkBoxColumnNumber = 2):
        super().__init__()
        self._data = data
        self.checkBoxColumnNumber = checkBoxColumnNumber
        self._headers = headers
        self.clickFunc = func
        self.Index1 = 0

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self._headers)

    def flags(self, index):
        base_flags = super().flags(index)
        if not index.isValid():
            return base_flags

        if index.column() == self.checkBoxColumnNumber:
            return base_flags | Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled

        return base_flags

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None

        if index.column() == self.checkBoxColumnNumber:
            if role == Qt.ItemDataRole.CheckStateRole:
                return Qt.CheckState.Checked  if self._data[index.row()][self.checkBoxColumnNumber] else Qt.CheckState.Unchecked
            if role == Qt.ItemDataRole.DisplayRole:
                return None

        if role == Qt.ItemDataRole.DisplayRole:
            return self._data[index.row()][index.column()]

        return None

    def setData(self, index, value, role=Qt.ItemDataRole.EditRole):
        if not index.isValid():
            return False

        if index.column() == self.checkBoxColumnNumber and role == Qt.ItemDataRole.CheckStateRole:
            self._data[index.row()][self.checkBoxColumnNumber] = (value == Qt.CheckState.Checked.value)
            self.dataChanged.emit(index, index, [role])
            self.clickFunc(self._data[index.row()][self.IDIndex], self._data[index.row()][self.Index1]) # Here 1 is the index of the id u want
            return True

        return False

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self._headers[section]
        return None

    def update_all_data(self, new_data):
        if new_data is None:
            print("Function does not return proper data, returns NOne")
            return
        self.beginResetModel()
        self._data = new_data
        self.endResetModel()
