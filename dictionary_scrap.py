from bs4 import BeautifulSoup
from pathlib import Path
import requests
import pdb
import os

website = "https://dictionary.com"
listWords = "/list/"
browseWord = "/browse/"

class EnglishWord:
    def __init__(self, word, url):
        self.word = word
        self.url = url
    
    def ToCsvLine(self):
        return "" + self.word + "," + self.url + os.linesep

    # TODO
    #def ToSqlInsert(self):
        

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
                    if href != None and browseWord in href:
                        wordUrls.append(EnglishWord(link.text, link.get('href')))
    return wordUrls

def DumpLettersToCsv(relativePathToUser, words):
    csvLines = list(map(lambda w: w.ToCsvLine(), words))
    filePath = os.path.join(Path.home(), relativePathToUser)
    with open(filePath, 'w', encoding="utf-8") as file:
        for line in csvLines:
            file.write(line)
    return filePath

# HTTP STATUS 200 means that the server accepted the URL.
def UrlIsValid(url):
    return requests.get(pageUrl).status_code == 200

# There are 26 letters in the alphabet, range is exclusive
for i in range(1, 27):
    letter = GetLetterInAlphabet(i)
    wordsForLetter = []
    page = 0

    while True:

        pageUrl = "" + website + listWords + letter

        # Add page if applicable.
        pageUrl += ("/" + str(page)) if page > 0 else ""

        if (UrlIsValid(pageUrl)):
            print("Visiting: " + pageUrl)
            wordsFromPage = GetWords(pageUrl)
            wordsForLetter += wordsFromPage
            page += 1
        else:
            print("Reached the end of pages for letter: " + letter)
            break

    print("Found " + str(len(wordsForLetter)) + " words that begin with " + letter)
    print("Dumped letters to: " + DumpLettersToCsv(letter + ".csv", wordsForLetter))


