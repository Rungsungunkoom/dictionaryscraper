import sqlite3
from sqlite3 import Error
import os
from pathlib import Path

def create_tables(relativePathToUser):
    conn = None
    try:
        dbFile = os.path.join(Path.home(), relativePathToUser)
        
        if os.path.isfile(dbFile):
            os.remove(dbFile)

        conn = sqlite3.connect(dbFile)

        with open("tables.sql") as tables:
            query = tables.read()
            sqlite3.complete_statement(query)
            conn.executescript(query)

    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def load_files(relativePathToUser):
    conn = None
    try:
        dbFile = os.path.join(Path.home(), relativePathToUser)
        conn = sqlite3.connect(dbFile)

        for i in range(0, 26):
            character = chr(ord('a') + i)
            print("Running " + character + ".sql...")
            with open(os.path.join(Path.home(), character + ".sql..."), 'r', encoding="utf-8") as alphabetSql:
                query = alphabetSql.read()
                sqlite3.complete_statement(query)
                conn.executescript(query)

    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    create_tables("dictionary.db")
    load_files("dictionary.db")
