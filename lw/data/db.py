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

    def __enter__(self):
        # todo: get installed path for db
        run_setup = not os.path.exists(DB_FILE_NAME)
        self.connection = sqlite3.connect(DB_FILE_NAME)

        if run_setup:
            try:
                _setup_db(self.connection)
            except sqlite3.OperationalError:
                self.connection.close()
                os.remove(DB_FILE_NAME)
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
