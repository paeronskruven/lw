import os
import sqlite3
from collections import namedtuple

DB_FILE_NAME = 'lw.db'

ListingItem = namedtuple('ListingItem', ['id', 'title', 'desc', 'url', 'price', 'source'])


def _setup_db(connection):
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE items(
            id,
            title,
            desc,
            url,
            price,
            source,
            PRIMARY KEY(id, source)
        );
    ''')

    cursor.execute('''
        CREATE TABLE keywords(
            key,
            PRIMARY KEY(key)
        );
    ''')

    connection.commit()


class DB:

    DB_PATH = os.path.expanduser('~/.lw/{0}'.format(DB_FILE_NAME))

    def __enter__(self):
        run_setup = not os.path.exists(self.DB_PATH)
        self.connection = sqlite3.connect(self.DB_PATH)

        if run_setup:
            try:
                _setup_db(self.connection)
            except sqlite3.OperationalError:
                self.connection.close()
                os.remove(self.DB_PATH)
                raise

        return self

    def __exit__(self, *args):
        self.connection.close()

    def execute(self, sql, parameters, many=False):
        cursor = self.connection.cursor()

        if many:
            cursor.executemany(sql, parameters)
            return

        cursor.execute(sql, parameters)

    def get(self, sql, parameters=None):
        cursor = self.connection.cursor()

        if parameters:
            cursor.execute(sql, parameters)
        else:
            cursor.execute(sql)

        return cursor.fetchall()

    def commit(self):
        self.connection.commit()
