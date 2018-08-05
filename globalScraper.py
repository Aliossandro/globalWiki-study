import urllib
from bs4 import BeautifulSoup
import pandas as pd
import os

class userGetter:

    def __init__(self, firstLink):
        self.startLink = firstLink
        self.baseUrl = 'https://en.wikipedia.org'
        self.accountList = []
        self.globalUserExtractor(self.startLink)
        self.pageNavigator(self.startLink)
        self.fileWriter()


    def pageNavigator(self, startLink):
        page = urllib.request.urlopen(self.baseUrl + startLink)

        # parse the html using beautiful soup and store in variable `soup`
        soup = BeautifulSoup(page, 'html.parser')
        nextLink = soup.find("a", class_="mw-nextlink")

        if nextLink:
            newLink = nextLink.get('href')
            print(newLink)
            self.globalUserExtractor(newLink)


    def globalUserExtractor(self, startLink):
        # parse the html using beautiful soup and store in variable `soup`
        page = urllib.request.urlopen(self.baseUrl + startLink)
        soup = BeautifulSoup(page, 'html.parser')
        name_box = soup.find('ul')

        for li in name_box:
            item = li.find('a')
            try:
                self.accountList.append(item.get('href').replace('/wiki/Special:CentralAuth/', ''))
            except AttributeError:
                print(item)

        self.pageNavigator(startLink)

    def fileWriter(self):
        with open('globalUserList.txt', 'w') as f:
            for user in self.accountList:
                f.write("%s\n" % user)
            f.close()


###

def main():
    # other_path = '/Users/alessandro/Documents/PhD/WD_ontology'
    startLink = '/w/index.php?title=Special:GlobalUsers&offset=&limit=5000'
    userGetter(startLink)


if __name__ == "__main__":
    main()
