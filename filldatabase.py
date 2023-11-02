import sqlite3

# This is just for testing, or filling the database with predefined information.

conn = sqlite3.connect("bookstore.db")
cursor = conn.cursor()


cursor.execute('''
    CREATE TABLE IF NOT EXISTS Authors (
        AuthorId INTEGER PRIMARY KEY,
        FirstName TEXT NOT NULL,
        Surname TEXT NOT NULL,
        DOB TEXT,
        Nationality TEXT
    )
''')

authors_data = [
    (1, 'Joanne', 'Rowling', '1965-07-31', 'British'),
    (2, 'Eric Arthur', 'Blair', '1903-06-25', 'British'),
    (3, 'Jane', 'Austen', '1775-12-16', 'British'),
    (4, 'Charles John Huffam', 'Dickens', '1812-02-07', 'British'),
    (5, 'Agatha Mary Clarissa', 'Miller', '1890-09-15', 'British'),
    (6, 'William', 'Shakespeare', '1564-04-26', 'British (English)'),
    (7, 'Samuel Langhorne', 'Clemens', '1835-11-30', 'American'),
    (8, 'Francis Scott Key', 'Fitzgerald', '1896-09-24', 'American'),
    (9, 'Nelle Harper', 'Lee', '1926-04-28', 'American'),
    (10, 'Ernest Miller', 'Hemingway', '1899-07-21', 'American')
]

for author in authors_data:
    cursor.execute('''
        INSERT INTO Authors (AuthorId, FirstName, Surname, DOB, Nationality) 
        VALUES (?, ?, ?, ?, ?)
    ''', author)

conn.commit()
conn.close()

