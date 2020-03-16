from bs4 import BeautifulSoup
from pathlib import Path
import requests
import pdb
import os
import threading

website = "https://www.dictionary.com"
listWords = "/list/"
browseWord = "/browse/"

def CsvSanitize(toSanitize):
    if toSanitize is None: return ""
    return "\""+toSanitize.replace("\"", "\"\"\"")+"\""

def SqlSanitize(toSanitize):
    if toSanitize is None: return ""
    return toSanitize.replace('\'', '\'\'')

class EnglishWord:
    def __init__(self, name, url):
        if (name is None): 
            self.name = "" 
        else: 
            self.name = name
        if (url is None): 
            self.url = "" 
        else: 
            self.url = url
        self.ipa = ""
        self.definitions = []
        self.wordClass = ""

    def ScrapeWordDetails(self):
        html = ""
        with requests.get(self.url) as webRequest:
            html = webRequest.text

        soup = BeautifulSoup(html, 'html.parser')

        ipa = soup.find("div", {"class": "pron-spell-ipa-container"})
        if ipa != None:
            self.ipa = ipa.text
    
        wordClass = soup.find("span", {"class": "pos"})

        if wordClass is None:
            wordClass = soup.find("span", {"class": "luna-pos"})

        if wordClass != None:
            self.wordClass = wordClass.text

        count = 1
        while True:
            definition = soup.find("div", {"value": str(count)})
            if (definition is None):
                break
            self.definitions.append(definition.text)
            count += 1
    
    def ToCsvLine(self):
        return "" + CsvSanitize(self.name) + "," + \
        CsvSanitize(self.url) + "," + \
        CsvSanitize(self.ipa) + "," + \
        CsvSanitize(self.wordClass) + \
        ",".join(map(lambda d: CsvSanitize(d), self.definitions)) + '\n'

    def ToSqlLines(self):
        # BEGIN/END transaction decreases the amount of time 
        # to insert from 3 hours, to less than a second
        insertStatements = "BEGIN TRANSACTION;\n"

        with open("words_template.sql", 'r') as file:
            insertsqlstatement = file.read()
            insertsqlstatement = insertsqlstatement \
                .replace("{word}", SqlSanitize(self.name)) \
                .replace("{url}", SqlSanitize(self.url)) 
            insertStatements += insertsqlstatement + '\n'

        if self.wordClass != "":
            with open("classes_template.sql", 'r') as file:
                insertsqlstatement = file.read()
                insertsqlstatement = insertsqlstatement \
                    .replace("{class}", SqlSanitize(self.wordClass)) 
                insertStatements += insertsqlstatement + '\n'

        if self.ipa != "":
            with open("pronounces_template.sql", 'r') as file:
                insertsqlstatement = file.read()
                insertsqlstatement = insertsqlstatement \
                    .replace("{ipa}", SqlSanitize(self.ipa))
                insertStatements += insertsqlstatement + '\n'

        if len(self.definitions) > 0:
            with open("definition_template.sql", 'r') as file:
                defsqlstatement = file.read()
                defCount = 1
                for definition in self.definitions:
                    temp = defsqlstatement
                    temp = temp \
                        .replace("{definition}", SqlSanitize(definition)) \
                        .replace("1", str(defCount))
                    defCount += 1
                    insertStatements += temp + '\n'

        return insertStatements + "END TRANSACTION;"
        
# Gets the letter in the alphabet.
def GetLetterInAlphabet(number):
    if number < 1 or number > 26:
        raise OverflowError
    return chr(ord('a') + number-1)

# Scrapes all the words from a URL
def GetWords(url):
    wordUrls = []
    with requests.get(url) as webRequest:
                html = webRequest.text
                
                soup = BeautifulSoup(html, 'html.parser')
                
                for link in soup.find_all('a'):
                    href = link.get('href')
                    if href != None and (website+browseWord) in href:
                        wordUrls.append(EnglishWord(link.text, link.get('href')))

    return wordUrls

def DumpWordsToCsv(relativePathToUser, words):
    csvLines = list(map(lambda w: w.ToCsvLine(), words))
    filePath = os.path.join(Path.home(), relativePathToUser)
    with open(filePath, 'w', encoding="utf-8") as file:
        for line in csvLines:
            file.write(line)
    return filePath

def DumpWordsToSql(relativePathToUser, words):
    sqlLines = list(map(lambda w: w.ToSqlLines(), words))
    filePath = os.path.join(Path.home(), relativePathToUser)
    with open(filePath, 'w', encoding="utf-8") as file:
        for line in sqlLines:
            file.write(line)
    return filePath

# HTTP STATUS 200 means that the server accepted the URL.
def UrlIsValid(url):
    return requests.get(url).status_code == 200

def ScrapeWordsForLetter(letter):
    wordsForLetter = []
    page = 0

    while True:
        pageUrl = "" + website + listWords + letter

        # Add page if applicable.
        pageUrl += ("/" + str(page)) if page > 0 else ""

        if (UrlIsValid(pageUrl)):
            wordsFromPage = GetWords(pageUrl)
            wordsForLetter += wordsFromPage
            page += 1
        else:
            break

    print("Found " + str(len(wordsForLetter)) + " words that begin with " + letter)

    for i in range(0, len(wordsForLetter)):
        word = wordsForLetter[i]
        word.ScrapeWordDetails()
        print("Scraped " + str(i) + "/" + str(len(wordsForLetter)) + " for " + letter + ": " + word.name)

    print("Dumped words to: " + DumpWordsToCsv(letter + ".csv", wordsForLetter))
    print("Dumped words to: " + DumpWordsToSql(letter + ".sql", wordsForLetter))

if __name__ == '__main__':
    threads = []

    # There are 26 letters in the alphabet, range is exclusive
    for i in range(1, 27):
        letter = GetLetterInAlphabet(i)
        thread = threading.Thread(target=ScrapeWordsForLetter, args=letter)
        thread.start()
        threads.append(thread)
        print("Started scraping words for " + letter + "...")
    
    for t in threads:
        t.join()

        
