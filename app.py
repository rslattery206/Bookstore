from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
from sqlalchemy.orm import load_only
import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookstore.db'
db = SQLAlchemy(app)
with app.app_context():
    db.create_all()


class Author(db.Model):
    AuthorId = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.Text, nullable=False)
    Surname = db.Column(db.Text, nullable=False)
    DOB = db.Column(db.Text)
    Nationality = db.Column(db.Text)
    Books = db.relationship('Book', backref='author', lazy=True)


class Publisher(db.Model):
    PublisherId = db.Column(db.Integer, primary_key=True)
    PublisherName = db.Column(db.Text, nullable=False)
    WorkingAddress = db.Column(db.Text)
    PhoneNumber = db.Column(db.Text)
    Books = db.relationship('Book', backref='publisher', lazy=True)


class Genre(db.Model):
    GenreId = db.Column(db.Integer, primary_key=True)
    GenreName = db.Column(db.Text, nullable=False)
    Books = db.relationship('Book', backref='genre', lazy=True)


class Book(db.Model):
    ISBN = db.Column(db.Text, primary_key=True)
    Title = db.Column(db.Text, nullable=False)
    AuthorId = db.Column(db.Integer, db.ForeignKey('author.AuthorId'), nullable=False)
    PublisherId = db.Column(db.Integer, db.ForeignKey('publisher.PublisherId'), nullable=False)
    GenreId = db.Column(db.Integer, db.ForeignKey('genre.GenreId'), nullable=False)
    PublishYear = db.Column(db.Integer)
    Price = db.Column(db.Float)
    Quantity = db.Column(db.Integer)


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


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/newbookorder', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        isbn = request.form['ISBN']
        title = request.form['Title']
        author_first_name = request.form['AuthorFirstName']
        author_last_name = request.form['AuthorLastName']
        publisher_id = request.form['PublisherId']
        publish_year = request.form['PublishYear']
        genre_id = request.form['GenreId']
        price = request.form['Price']
        quantity = request.form['Quantity']

        author = Author.query.filter_by(FirstName=author_first_name, Surname=author_last_name).first()
        if author:
            author_id = author.AuthorId
        else:
            new_author = Author(FirstName=author_first_name, Surname=author_last_name)
            db.session.add(new_author)
            db.session.commit()
            author_id = new_author.AuthorId

        publisher = Publisher.query.get(publisher_id)
        if publisher:
            publisher_id = publisher.PublisherId
        if not publisher:
            new_publisher = Publisher(PublisherName=f"defaultpublisherName:{str(publisher_id)}")
            db.session.add(new_publisher)
            db.session.commit()
            publisher_id = new_publisher.PublisherId

        genre = Genre.query.get(genre_id)
        if genre:
            genre_id = genre.GenreId
        if not genre:
            new_genre = Genre(GenreName=f"defaultGenreName:{str(genre_id)}")
            db.session.add(new_genre)
            db.session.commit()
            genre_id = new_genre.GenreId

        # Insert the book with the obtained author, publisher, and genre IDs
        new_book = Book(ISBN=isbn,
                        Title=title,
                        AuthorId=author_id,
                        PublisherId=publisher_id,
                        GenreId=genre_id,
                        PublishYear=publish_year,
                        Price=price,
                        Quantity=quantity)
        db.session.add(new_book)
        db.session.commit()

        book = Book.query.filter_by(ISBN=isbn).first()
        print(f"Retrieved Book: {book}")
    return render_template('newbookorder.html')


@app.route('/sale', methods=['GET', 'POST'])
def sale():
    if request.method == 'POST':
        isbn = str(request.form['ISBN'])  # Convert to string
        quantity = int(request.form['Quantity'])
        book = Book.query.filter_by(ISBN=isbn).first()

        print(f"Retrieved Book: {book}")

        if book:
            new_quantity = book.Quantity - quantity
            if new_quantity >= 0:
                book.Quantity = new_quantity
                db.session.commit()
            else:
                return render_template('sale.html', message="Not enough stock available.")
        else:
            return render_template('sale.html', message="Book not found.")

    return render_template('sale.html')


from flask import render_template
from sqlalchemy import text

from flask import render_template


@app.route('/report', methods=['GET', 'POST'])
def generate_report():
    selected_columns = []
    where_conditions = []

    if request.method == 'POST':
        selected_columns = request.form.getlist('columns')
        if selected_columns:
            base_query = db.session.query(Book).with_entities(
                *[getattr(Book, column) for column in selected_columns]
            )
            print(base_query)
            for column in selected_columns:
                filter_operator = request.form.get(f'filter_operator_{column}')
                filter_value = request.form.get(f'filter_value_{column}')
                if filter_value:
                    base_query = base_query.filter(text(f"{column} {filter_operator} {filter_value}"))
                    print(base_query)
            # Execute the query
            books = base_query.all()

        return render_template('report.html', books=books, selected_columns=selected_columns)

    return render_template('report.html', books=[], selected_columns=selected_columns)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
