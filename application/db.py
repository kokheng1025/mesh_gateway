import sqlite3
from sqlite3 import Error
from sqlite3.dbapi2 import connect



class Database(object):
    def __init__(self):
        super().__init__()

    def get_connection(self):
        connection = None
        try:
            connection = sqlite3.connect("./mesh_db.db")
            print("Connection to SQLite DB successful")
        except Error as e:
            print("SQLite DB connection error: {}".format(e))
        
        return connection
