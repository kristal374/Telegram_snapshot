import sqlite3

class DataBase:
    def __init__(self, name):
        self.db = sqlite3.connect(name)
        self.cursor = self.db.cursor()
        self.__create()

    def __create(self):
        self.transactions("""
        CREATE TABLE IF NOT EXISTS chat(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chat_id INTEGER NOT NULL,
        name TEXT,
        class TEXT NOT NULL,
        phone INTEGER,
        tag TEXT,
        status TEXT NOT NULL);""")

    def transactions(self, requests):
        self.cursor.execute(requests)
        self.db.commit()
