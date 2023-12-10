CREATE TABLE IF NOT EXISTS Authors (
    AuthorId INTEGER PRIMARY KEY,
    FirstName TEXT NOT NULL,
    Surname TEXT NOT NULL,
    DOB TEXT,
    Nationality TEXT
);

CREATE TABLE IF NOT EXISTS Publishers (
    PublisherId INTEGER PRIMARY KEY,
    PublisherName TEXT NOT NULL,
    WorkingAddress TEXT,
    PhoneNumber TEXT
);

CREATE TABLE IF NOT EXISTS Genres (
    GenreId INTEGER PRIMARY KEY,
    GenreName TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Books (
    ISBN TEXT PRIMARY KEY,
    Title TEXT NOT NULL,
    AuthorId INTEGER,
    PublisherId INTEGER,
    GenreId INTEGER,
    PublishYear INTEGER,
    Price REAL,
    Quantity INTEGER,
    FOREIGN KEY (AuthorId) REFERENCES Authors (AuthorId),
    FOREIGN KEY (PublisherId) REFERENCES Publishers (PublisherId),
    FOREIGN KEY (GenreId) REFERENCES Genres (GenreId)
);
