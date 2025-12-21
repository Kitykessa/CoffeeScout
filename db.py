import sqlite3

def get_db_connection():
    db = sqlite3.connect("coffee.db")
    db.row_factory = sqlite3.Row
    return db
