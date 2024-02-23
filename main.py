import sys
from design import Ui_MainWindow
from database.dialog import Ui_Dialog
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem
from database.select import select_all


class Dialog(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.ok_btn.clicked.connect(self.click_ok)
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setHorizontalHeaderLabels(['id', 'Наименование', 'Площадь поры', 'Откл. от площади',
                                                    'Пористость', 'Откл. от пористости'])
        self.table_update()

    def click_ok(self):
        self.accept()

    def table_update(self):
        rows = select_all()
        print(rows)
        self.tableWidget.setRowCount(len(rows))
        for i, row in enumerate(rows):
            print(i, row)
            for j, value in enumerate(row):
                self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(value)))


class Window(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.edit_btn.clicked.connect(self.edit)

    def edit(self):
        dial = Dialog()
        dial.show()
        result = dial.exec()
        if result == 1:
            print("Нажата кнопка ОК")
        else:
            print("Нажата кнопка Cancel")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = Window()
    win.show()
    app.exec()
