import sqlite3

from .db import DB


def add_keyword(key):
    with DB() as db:
        db.execute('INSERT INTO keywords VALUES (?)', (key,))
        db.commit()


def remove_keyword(key):
    with DB() as db:
        db.execute('DELETE FROM keywords WHERE key = ?', (key,))
        db.commit()
        return db.connection.total_changes


def list_keywords():
    with DB() as db:
        return db.get('SELECT * FROM keywords')


def add_items(items):
    with DB() as db:
        for item in items:
            try:
                db.execute('INSERT INTO items VALUES (?, ? ,?, ?, ?, ?)', tuple(item))
                db.commit()

                yield item
            except sqlite3.IntegrityError:
                continue
