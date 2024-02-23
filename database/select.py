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


if __name__ == '__main__':
    print(select_all())
