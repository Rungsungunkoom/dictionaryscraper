from bs4 import BeautifulSoup
import requests
import os
from pathlib import Path
import sqlite3
from sqlite3 import Error

templateLocation = "../sql_templates/"

def SqlSanitize(toSanitize):
    if toSanitize is None: return ""
    return toSanitize.replace('\'', '\'\'')

# Currently unused, because wikitionary WOTD archive is pretty lame ATM.
def WikitionaryWotd(url):
    html = None
    words = []
    with requests.get(url) as webrequest:
        html = webrequest.text
        soup = BeautifulSoup(html, 'html.parser')

        for word in soup.find_all('span', {"id": "WOTD-rss-title"}):
            words.append(word.text)

    return words

def DictionaryWotd():
    startingUrl = "https://www.dictionary.com/e/word-of-the-day/"
    url = startingUrl
    totalWords = []

    while url != None:
        with requests.get(url) as webrequest:
            html = webrequest.text
            soup = BeautifulSoup(html, 'html.parser')

            words = soup.find_all('div', {"class": "wotd-item-headword__word"})

            for word in words:
                totalWords.append(word.text.replace("\n", ""))

            nextWord = soup.find('a', {"class": "wotd-item__load-more"})

            if nextWord is None:
                break

            print(nextWord['href'])
            url = nextWord['href']

    return totalWords

def DumpToFile(relativePathToUser, words):
    filePath = os.path.join(Path.home(), relativePathToUser)
    sanitizedWords = list(map(lambda w: '\'' + SqlSanitize(w) + '\'', words))
    instatement = ','.join(sanitizedWords)
    sqlStatement = ""
    with open(templateLocation + "wotdworthy_template.sql", 'r') as file:
                sqlStatement = file.read() \
                    .replace("{words}", instatement)

    with open(filePath, 'w', encoding="utf-8") as file:
        file.write(sqlStatement)

words = DictionaryWotd()

print(len(words))
DumpToFile("wotdscrape.sql", words)

conn = None
try:
    dbFile = os.path.join(Path.home(), "dictionary.db")
    conn = sqlite3.connect(dbFile)

    with open(os.path.join(Path.home(), "wotdscrape.sql"), 'r', encoding="utf-8") as alphabetSql:
        query = alphabetSql.read()
        sqlite3.complete_statement(query)
        conn.executescript(query)
except Error as e:
    print(e)
finally:
    if conn:
        conn.close()
