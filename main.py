import sys
import logging
from datetime import datetime

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QPixmap, QImage

import cv2 as cv

from design import Ui_MainWindow
from database.dialog import Ui_Dialog
from database.select import select_all, delete, add, select_name
from algorithms import preprocessing

from reports import create_report


class Dialog(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.ok_btn.clicked.connect(self.click_ok)
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setHorizontalHeaderLabels(['id', 'Наименование', 'Площадь поры', 'Откл. от площади',
                                                    'Пористость', 'Откл. от пористости'])

        self.del_btn.clicked.connect(self.click_delete)
        self.add_btn.clicked.connect(self.click_add)

        self.table_update()

    def click_add(self) -> None:
        """
        Обработчик нажатия кнопки добавления записи
        :return:
        """
        name = self.name_line.text()
        square = self.square_line.text()
        square_std = self.square_std_line.text()
        density = self.density_line.text()
        density_std = self.density_std_line.text()
        add(name, square, square_std, density, density_std)
        self.table_update()

    def click_delete(self) -> None:
        """
        Обработчик нажатия кнопки удаления записи
        :return:
        """
        identity = self.delete_line.text()
        delete(identity)
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
        self.dial = Dialog()

        self.setupUi(self)
        self.edit_btn.clicked.connect(self.edit)
        self.actionOpen.triggered.connect(self.open_image)
        self.logo_label.setPixmap(QPixmap('logo.png'))

        self.contrast_slider.valueChanged['int'].connect(self.contrast_update)
        self.brightness_slider.valueChanged['int'].connect(self.brightness_update)
        self.sharpness_slider.valueChanged['int'].connect(self.sharpness_update)

        self.contrast_reset.clicked.connect(self.reset_contrast)
        self.brightness_reset.clicked.connect(self.reset_brightness)
        self.sharpness_reset.clicked.connect(self.reset_sharpness)

        self.image = None
        self.final_image = None
        self.pore_density = 0
        self.pore_is_correct = False
        self.pore_anomaly = 0
        self.contrast_value = 1
        self.brightness_value = 0
        self.sharpness_value = 0
        self.material_id = None

        self.combobox_update()
        self.material_info_update()

        self.comboBox.currentTextChanged.connect(self.material_info_update)

        self.report_name = datetime.now().strftime('reports/report_%d-%m-%Y_%H-%M-%S.csv')
        self.report_created = False
        self.save_btn.clicked.connect(self.save_report)

        self.snapshot_btn.clicked.connect(self.save_image)

    def save_image(self) -> None:
        if self.final_image is not None:
            filename, _ = QFileDialog.getSaveFileName(self, 'Save File', '', '*.jpg')
            print(filename)
            cv.imwrite(filename, self.final_image)

    def save_report(self) -> None:
        """
        Сохранение информацию в табличном виде
        :return:
        """
        print('Saving report ...')
        if self.report_created:
            create_report.add(self.report_name, (self.comboBox.currentText(), self.contrast_value,
                                                 self.brightness_value, self.sharpness_value, self.square_label.text(),
                                                 self.square_label.text(), self.density_label.text(),
                                                 self.density_std_label.text(), self.pore_density, self.pore_is_correct,
                                                 self.pore_anomaly))
        else:
            create_report.write_header(self.report_name)
            self.report_created = True
            self.save_report()

    def material_info_update(self) -> None:
        """
        Обновление информирующих лейблов на основе данных о материале
        :return:
        """
        info = select_all()[self.comboBox.currentIndex()]
        self.material_id = int(info[0])
        print(self.material_id)
        self.square_label.setText(str(info[-4]))
        self.square_std_label.setText(str(info[-3]))
        self.density_label.setText(str(info[-2]))
        self.density_std_label.setText(str(info[-1]))
        if self.image is not None:
            self.update_image()

    def combobox_update(self) -> None:
        """
        Обновление комбо-бокса
        :return:
        """
        req = select_name()
        self.comboBox.clear()
        for r in req:
            print(r[0])
            self.comboBox.addItem(r[0])

    def reset_contrast(self) -> None:
        """
        Обработчик нажатия кнопки Reset
        :return:
        """
        self.contrast_value = 1
        self.contrast_slider.setValue(0)

    def reset_brightness(self) -> None:
        """
        Обработчик нажатия кнопки Reset
        :return:
        """
        self.brightness_value = 0
        self.brightness_slider.setValue(0)

    def reset_sharpness(self) -> None:
        """
        Обработчик нажатия кнопки Reset
        :return:
        """
        self.sharpness_value = 0
        self.sharpness_slider.setValue(0)

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
        self.update_image()
        self.area_update(self.image)

    def contrast_update(self, value) -> None:
        """
        Метод для преобразования значений контрастности и обновления изображения
        :param value:
        :return:
        """
        self.contrast_value = value / 20 + 1
        if self.image is not None:
            self.update_image()

    def brightness_update(self, value) -> None:
        """
        Метод для преобразования значений контрастности и обновления изображения
        :param value:
        :return:
        """
        self.brightness_value = value
        if self.image is not None:
            self.update_image()

    def sharpness_update(self, value) -> None:
        """
        Метод для преобразования значений резкости и обновления изображения
        :param value:
        :return:
        """
        self.sharpness_value = value / 10
        if self.image is not None:
            self.update_image()

    def area_update(self, image) -> None:
        """
        Главный алгоритм определения пористости
        :param image:
        :return:
        """
        img, self.pore_density, self.pore_anomaly = preprocessing.explore(image,
                                                                          float(self.square_label.text()) -
                                                                          float(self.square_std_label.text()),
                                                                          float(self.square_label.text()) +
                                                                          float(self.square_std_label.text()))
        self.pore_density = round(self.pore_density, 2)
        self.density_info.setText(f'Пористость: {self.pore_density}')
        self.anomaly_label.setText(f'Количество пор, \nпревышающих норму: {self.pore_anomaly}')
        self.set_image(img, 'close')
        self.final_image = img
        print(float(self.density_label.text()) - float(self.density_std_label.text()))
        if (float(self.density_label.text()) - float(self.density_std_label.text()) <= self.pore_density
                <= float(self.density_label.text()) + float(self.density_std_label.text())):
            self.is_normal_label.setText('Пористость в норме')
        else:
            self.is_normal_label.setText('Пористость не в норме')

    def update_image(self):
        """
        Метод обновляет все значения изображения
        :return:
        """
        img = preprocessing.linear_change(self.image, self.contrast_value, self.brightness_value)
        img = preprocessing.change_sharpness(img, self.sharpness_value)
        self.area_update(img)
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
        Функция-обработчик диалогового окна
        :return:
        """
        self.setEnabled(False)
        self.dial.show()
        result = self.dial.exec()
        if result == 1:
            print("Нажата кнопка ОК")
        else:
            print("Нажата кнопка Cancel")
        self.setEnabled(True)
        self.combobox_update()


if __name__ == '__main__':
    logging.basicConfig(level='INFO')
    app = QtWidgets.QApplication(sys.argv)

    win = Window()
    win.show()
    sys.exit(app.exec())
