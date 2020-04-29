import requests
from pathlib import Path
import os
import sqlite3
import pdb
from sqlite3 import Error
import json

url = os.getenv('DISCORD_WEBHOOK')
templateLocation = "sql_templates/"

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

def getWordOfTheDay(relativePathToUser, guild):
    conn = None
    result = None

    try:
        dbFile = os.path.join(Path.home(), relativePathToUser)
        conn = sqlite3.connect(dbFile)
        cur = conn.cursor()

        # Get word of the day that hasn't been shared in this guild yet.
        with open(templateLocation + "wotd_random_word_id.sql") as word:
            query = word.read()
            sqlite3.complete_statement(query)
            cur.execute(query, (guild,))
            record = cur.fetchall()
            result = record[0][0]

        # Record this word for this guild, so that it doesn't show up again.
        with open(templateLocation + "wotd_log.sql") as word:
            query = word.read()
            sqlite3.complete_statement(query)
            cur.execute(query, (result, guild))
            conn.commit()

        # Query the data for the word and project in JSON so that Discord can display it.
        with open(templateLocation + "wotd_random_word.sql") as word:
            query = word.read()
            sqlite3.complete_statement(query)
            cur.execute(query, (result,))
            record = cur.fetchall()
            result = record
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

    return result

if __name__ == '__main__':
    guild = os.getenv('DISCORD_GUILD')
    result = getWordOfTheDay("dictionary.db", guild)
    requests.post(url, json={"username": "WordOfTheDay", "embeds": [json.loads(result[0][0])]})
