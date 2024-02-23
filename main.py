import sys
import logging
import time

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QFileDialog
from PyQt5.QtGui import QPixmap, QImage

from PIL.ImageQt import ImageQt
from PIL import Image, ImageEnhance

import cv2 as cv

from design import Ui_MainWindow
from database.dialog import Ui_Dialog
from database.select import select_all
from algorithms import preprocessing


class ImageProcessing(QThread):
    finish_signal = pyqtSignal(object)

    def __init__(self):
        super().__init__()

    def run(self) -> None:
        QtImage1 = ImageQt(preprocessing.change_contrast(PilImage, 1.5))
        QtImage2 = QImage(QtImage1)
        pxmap = QPixmap.fromImage(QtImage2)
        self.finish_signal.emit(pxmap)


class Dialog(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.ok_btn.clicked.connect(self.click_ok)
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setHorizontalHeaderLabels(['id', 'Наименование', 'Площадь поры', 'Откл. от площади',
                                                    'Пористость', 'Откл. от пористости'])
        self.table_update()

    def click_ok(self) -> None:
        """
        Обработка закрытия окна
        :return:
        """
        self.accept()

    def table_update(self) -> None:
        """
        Обновление таблицы
        :return:
        """
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
        self.actionOpen.triggered.connect(self.open_image)
        self.contrast_slider.valueChanged['int'].connect(self.contrast_update)
        self.brightness_slider.valueChanged['int'].connect(self.brightness_update)
        self.image = None
        self.contrast_value = 1
        self.brightness_value = 0

    def open_image(self) -> None:
        """
        Метод открывает диалоговое окно с выбором файла и записывает изображение в атрибут класса
        :return:
        """
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open File', './', 'JPEG File (*.jpg);;PNG File (*.png)')
        print(file_path)
        if not file_path:
            return
        self.image = cv.imread(file_path)
        self.set_image(self.image, 'main')
        self.set_image(self.image, 'final')

    def contrast_update(self, value) -> None:
        """
        Метод для преобразования значений контрастности и обновления изображения
        :param value:
        :return:
        """
        self.contrast_value = value / 20 + 1
        self.update_image()

    def brightness_update(self, value) -> None:
        """
        Метод для преобразования значений контрастности и обновления изображения
        :param value:
        :return:
        """
        self.brightness_value = value
        self.update_image()

    def update_image(self):
        '''
        Метод обновляет все значения изображения
        :return:
        '''
        img = preprocessing.linear_change(self.image, self.contrast_value, self.brightness_value)
        self.set_image(img, 'final')

    def set_image(self, image, view='main') -> None:
        """
        Метод отображает изображение во фрейме
        :param view:
        :param image:
        :return:
        """
        frame = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
        if view == 'main':
            self.main_view.setPixmap(QPixmap.fromImage(image))
        elif view == 'final':
            self.final_view.setPixmap(QPixmap.fromImage(image))
        elif view == 'close':
            self.close_view.setPixmap(QPixmap.fromImage(image))
        else:
            return

    def edit(self) -> None:
        """
        Функция-обработчик закрытия диалогового окна
        :return:
        """
        dial = Dialog()
        dial.show()
        result = dial.exec()
        if result == 1:
            print("Нажата кнопка ОК")
        else:
            print("Нажата кнопка Cancel")


if __name__ == '__main__':
    logging.basicConfig(level='INFO')
    app = QtWidgets.QApplication(sys.argv)

    # PilImage = Image.open('images/photo_2024-02-19_21-45-26.jpg')
    # QtImage1 = ImageQt(PilImage)
    # QtImage2 = QImage(QtImage1)
    # pixmap = QPixmap.fromImage(QtImage2)

    win = Window()
    win.show()
    sys.exit(app.exec())
