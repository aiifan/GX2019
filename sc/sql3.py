import sqlite3

class AutoSqlite():
    def __init__(self):
        self.conn = sqlite3.connect("test.db")
        self.corsor = self.conn.cursor()
        
    def 

    def __close(self):
        self.cursor.close()
        self.conn.close()
        