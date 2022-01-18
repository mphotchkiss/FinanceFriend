import sqlite3

class Connection:
    def __init__(self, path):
        self.db_path = path
        self.conn = None
        self.c = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self.c = self.conn.cursor()

    def disconnect(self):
        #commit and close
        self.conn.commit()
        self.conn.close()

    def execute(self, query, mapping):
        self.c.execute(query, mapping)