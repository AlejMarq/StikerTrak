-- StikerTrak Database Schema

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL
);

CREATE TABLE stickers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sticker_number TEXT NOT NULL UNIQUE,
    category TEXT NOT NULL,
    section TEXT,
    name TEXT NOT NULL,
    country TEXT
);

CREATE TABLE user_collection (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    sticker_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 0,

    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (sticker_id) REFERENCES stickers(id),

    UNIQUE (user_id, sticker_id)
);
