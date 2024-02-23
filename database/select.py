import sqlite3


def select_all():
    connection = sqlite3.connect('database/database.sqlite')
    cursor = connection.cursor()
    rows = None
    result = []
    print('GO')
    try:
        rows = cursor.execute('SELECT * FROM Materials')
        connection.commit()
        for row in rows:
            print(row)
            result.append(row)
        rows = result
        print(rows)
    except Exception as ex:
        print(ex)
    finally:
        connection.close()
        return rows


if __name__ == '__main__':
    print(select_all())
