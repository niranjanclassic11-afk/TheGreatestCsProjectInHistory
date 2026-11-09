import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from chef import chefView as chef_UI_class
from cashier import cashierView as cashier_UI_class
from waiter import waiterView as waiter_UI_class

import mysql.connector as connector

conn = connector.connect(database = "HOTEL_MANAGEMENT", host = "localhost", user = "user", password = "password")
cursor = conn.cursor()

class QT_Call_Handler:

    def __init__(self):
        self.waiter_window = None
        self.chef_window = None
        self.cashier_window = None

    def on_order_placed(self, order):
        cursor.execute("SELECT Order_ID FROM ORDERS ORDER BY Order_ID DESC LIMIT 0, 1")
        data = cursor.fetchall()
        total_price = 0
        if data: order_id = data[0][0] + 1
        else: order_id = 1
        for item_code in order:
            quantity = order[item_code]
            cursor.execute(f"SELECT Price FROM Menu WHERE ItemCode = {item_code}")
            data = cursor.fetchall()
            rate = data[0][0]
            price = quantity * rate
            total_price += price
            cursor.execute(f"INSERT INTO ORDERS VALUES({order_id}, {item_code}, {quantity}, {price}, 0)")
        cursor.execute(f"INSERT INTO payments VALUES({order_id}, {total_price}, 0, 0)")
        conn.commit()
        self.chef_window.updateTable()
        self.cashier_window.updateTable()
    def get_receipt_data(self, order_id):
        cursor.execute("select orders.item_code, menu.itemName , orders.quantity, orders.price from orders, menu where orders.item_code = menu.itemcode and orders.order_id = " + str(order_id) + ";")
        data1 =  cursor.fetchall()
        cursor.execute("select sum(orders.price) from orders where order_id="+str(order_id))
        data2 = cursor.fetchall()
        print(str(data2[0]))
        return (data1, data2)

    def get_chef_data(self):
        cursor.execute("SELECT Order_ID, Item_Code, Quantity FROM ORDERS WHERE Completed = 0")
        data = cursor.fetchall()
        data = [[i for i in j] for j in data]
        for row in data:
            row.append(False)
            cursor.execute("SELECT ItemName FROM Menu WHERE ItemCode = " + str(row[1]))
            a = cursor.fetchall()
            if a:
                row.insert(1, a[0][0])
        return data
        
    def mark_item_finished(self, order_id, item_code):
        cursor.execute(f"UPDATE ORDERS SET Completed = 1 WHERE Order_ID = {order_id} AND Item_Code = {item_code}")
        conn.commit()
        self.chef_window.updateTable()
        cursor.execute(f"SELECT Completed FROM ORDERS WHERE Order_ID = {order_id}")
        data = cursor.fetchall()
        data = [i[0] for i in data]
        if min(data) != 0:
            cursor.execute("UPDATE payments SET Completed = 1 WHERE OrderID = " + str(order_id))
            self.cashier_window.updateTable() 

    def get_item_names(self):
        cursor.execute("SELECT ItemName FROM Menu ORDER BY ItemCode ASC")
        data = cursor.fetchall()
        data = [rec[0] for rec in data]
        return data
 
    def get_item_codes(self):
        cursor.execute("SELECT ItemCode FROM Menu ORDER BY ItemCode ASC")
        data = cursor.fetchall()
        data = [rec[0] for rec in data]
        return data

    def get_cashier_data(self):
        cursor.execute("SELECT OrderID, Price, Completed FROM payments WHERE Paid = 0")
        data = cursor.fetchall()
        data = [[i for i in j] for j in data]
        for row in data:
            if row[2]: row[2] = "COOKED :-)"
            else: row[2] = "COOKING...!"
            row.append(False)
        return data

    def cash_paid(self, order_id):
        cursor.execute("UPDATE payments SET Paid = 1 WHERE OrderID = " + str(order_id))
        conn.commit()
        self.cashier_window.updateTable()

call_handler = QT_Call_Handler()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    chef_window = chef_UI_class(call_handler)
    cashier_window = cashier_UI_class(call_handler)
    waiter_window = waiter_UI_class(call_handler)

    call_handler.chef_window = chef_window
    call_handler.cashier_window = cashier_window
    call_handler.waiter_window = waiter_window

    chef_window.showMaximized()
    cashier_window.showMaximized()
    waiter_window.showMaximized()
    
    sys.exit(app.exec())
