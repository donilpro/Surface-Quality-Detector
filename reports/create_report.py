import csv
from datetime import datetime


def write_header(filename) -> None:
    """
    Создание заголовков столбцов в таблице
    :param filename:
    :return:
    """
    with open(filename, 'w', encoding='utf8') as file:
        fieldnames = ['Материал', 'Контрастность', 'Яркость', 'Резкозть', 'Табличная площадь пор',
                      'Табличное отклонение от площади пор', 'Табличная пористость',
                      'Табличное отклонение от пористости', 'Зафиксированная пористость',
                      'Пористость в норме', 'Количество пор, превышающих норму']
        writer = csv.DictWriter(file, delimiter=',', fieldnames=fieldnames)
        writer.writeheader()


def add(filename, data) -> None:
    """
    Добавление новых записей в репорт
    :param filename:
    :param data:
    :return:
    """
    with open(filename, 'a', encoding='utf8') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(data)


if __name__ == '__main__':
    print(datetime.now().strftime('report_%d-%m-%Y_%H-%M-%S.csv'))
    write_header(name := datetime.now().strftime('report_%d-%m-%Y_%H-%M-%S.csv'))
    add(name, (1, 0, 1))
