import sqlite3


def select_all() -> list:
    """
    Запрос на получение всех данных из таблицы
    :return: list
    """
    connection = sqlite3.connect('database/database.sqlite')
    cursor = connection.cursor()
    rows = None
    result = []
    try:
        rows = cursor.execute('SELECT * FROM Materials')
        connection.commit()
        for row in rows:
            result.append(row)
        rows = result
    except Exception as ex:
        print(ex)
    finally:
        connection.close()
        return rows


def select_name() -> list:
    """
    Запрос на получение названий материалов из таблицы
    :return: list
    """
    connection = sqlite3.connect('database/database.sqlite')
    cursor = connection.cursor()
    rows = None
    result = []
    try:
        rows = cursor.execute('SELECT NAME FROM Materials')
        connection.commit()
        for row in rows:
            result.append(row)
        rows = result
    except Exception as ex:
        print(ex)
    finally:
        connection.close()
        return rows


def delete(identity) -> None:
    """
    Запрос на удаление из базы данных записи по id
    :return:
    """
    connection = sqlite3.connect('database/database.sqlite')
    cursor = connection.cursor()
    try:
        cursor.execute(f'DELETE FROM Materials WHERE ID = {identity}')
        connection.commit()
    except Exception as ex:
        print(ex)
    finally:
        connection.close()


def add(name, square, square_std, density, density_std) -> None:
    """
    Запрос на добавление записи в базу данных
    :return:
    """
    connection = sqlite3.connect('database/database.sqlite')
    cursor = connection.cursor()
    try:
        cursor.execute(f'INSERT INTO Materials(NAME, PORE_AREA_MEAN, PORE_AREA_STD, POROUS_MEAN, POROUS_STD) '
                       f'VALUES (?, ?, ?, ?, ?)', (name, square, square_std, density, density_std))
        connection.commit()
    except Exception as ex:
        print(ex)
    finally:
        connection.close()


if __name__ == '__main__':
    print(select_all())
