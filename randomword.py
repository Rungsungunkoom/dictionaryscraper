import requests
from pathlib import Path
import os
import sqlite3
import pdb
from sqlite3 import Error
import json

url = os.getenv('DISCORD_WEBHOOK')

def getRandomWord(relativePathToUser):
    conn = None
    result = None
    try:
        dbFile = os.path.join(Path.home(), relativePathToUser)

        conn = sqlite3.connect(dbFile)
        cur = conn.cursor()

        with open("random_word.sql") as word:
            query = word.read()
            sqlite3.complete_statement(query)
            cur.execute(query)
            record = cur.fetchone()
            result = record[0]
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
    return result

if __name__ == '__main__':
    result = getRandomWord("dictionary.db")
    requests.post(url, json={"username": "WordOfTheDay", "embeds": [json.loads(result)]})

