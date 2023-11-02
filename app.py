from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)


def connect_db():
    conn = sqlite3.connect("bookstore.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = connect_db()
    with app.open_resource('schema.sql', mode='r') as f:
        conn.cursor().executescript(f.read())
    conn.commit()
    conn.close()


@app.route('/newbookorder', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        isbn = request.form['ISBN']
        title = request.form['Title']
        author_first_name = request.form['AuthorFirstName']
        author_last_name = request.form['AuthorLastName']
        publisher_id = request.form['PublisherId']
        genre_id = request.form['GenreId']
        publish_year = request.form['PublishYear']
        price = request.form['Price']
        quantity = request.form['Quantity']
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT AuthorId FROM Authors WHERE FirstName=? AND Surname=?', (author_first_name, author_last_name))
        author_id = cursor.fetchone()
        if author_id:
            author_id = author_id[0]
        else:
            # Author does not exist
            cursor.execute('INSERT INTO Authors (FirstName, Surname) VALUES (?, ?)', (author_first_name, author_last_name))
            conn.commit()
            author_id = cursor.lastrowid
        cursor.execute('INSERT INTO Books (ISBN, Title, AuthorId, PublisherId, GenreId, PublishYear, Price, Quantity) '
                       'VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                       (isbn, title, author_id, publisher_id, genre_id, publish_year, price, quantity))
        conn.commit()
        conn.close()
    return render_template('newbookorder.html')


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
