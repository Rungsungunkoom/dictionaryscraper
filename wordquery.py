import requests
from pathlib import Path
import os
import sqlite3
import pdb
from sqlite3 import Error
import json

url = os.getenv('DISCORD_WEBHOOK')
templateLocation = "../sql_templates/"

def getRandomWord(relativePathToUser, number, startswith, endswith):
    conn = None
    result = None

    if number <= 0 or number > 10:
        raise Exception("No! You can only give me a number between 1 and 10 :)")

    try:
        dbFile = os.path.join(Path.home(), relativePathToUser)

        conn = sqlite3.connect(dbFile)
        cur = conn.cursor()

        with open(templateLocation + "random_word.sql") as word:
            query = word.read()
            sqlite3.complete_statement(query)
            cur.execute(query, (startswith+"%", "%"+endswith, number))
            record = cur.fetchall()
            result = record
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

    return result

if __name__ == '__main__':
    result = getRandomWord("dictionary.db", 1, "", "")
    requests.post(url, json={"username": "WordOfTheDay", "embeds": [json.loads(result)]})