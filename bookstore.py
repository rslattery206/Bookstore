import sqlite3


def create_database():
    try:
        conn = sqlite3.connect('bookstore.db')
        cursor = conn.cursor()
        with open('schema.sql', 'r') as file:
            schema = file.read()
            cursor.executescript(schema)
        conn.commit()
        conn.close()
        print("Database created (success)")
    except sqlite3.Error as e:
        print(e)


if __name__ == '__main__':
    create_database()


