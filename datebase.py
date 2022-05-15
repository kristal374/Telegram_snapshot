import sqlite3
import const

class DataBase:
    def __init__(self, name):
        self.db = sqlite3.connect(name)
        self.cursor = self.db.cursor()
        self.__create()

    def __create(self):
        self.transactions(const.CHANNEL_DB)

    def transactions(self, requests):
        self.cursor.execute(requests)
        self.db.commit()

    def defender_transaction(self, requests, *args):
        self.cursor.executemany(requests, [args])
        self.db.commit()
