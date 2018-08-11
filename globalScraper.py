import urllib
from bs4 import BeautifulSoup
import pandas as pd
import os
import http
import time

class userGetter:

    def __init__(self, firstLink):
        self.startLink = firstLink
        self.baseUrl = 'https://en.wikipedia.org'
        self.accountList = []
        self.globalUserExtractor(self.startLink)
        self.pageNavigator(self.startLink)
        self.fileWriter()


    def pageNavigator(self, startLink):
        try:
            page = urllib.request.urlopen(self.baseUrl + startLink)
            # parse the html using beautiful soup and store in variable `soup`
            soup = BeautifulSoup(page, 'html.parser')
            nextLink = soup.find("a", class_="mw-nextlink")

            if nextLink:
                newLink = nextLink.get('href')
                print(newLink)
                try:
                    self.globalUserExtractor(newLink)
                except RecursionError:
                    print(newLink)
                    self.fileWriter()
        except (http.client.IncompleteRead) as e:
            print(e)
            page = e.partial
            print(page)

            time.sleep(480)
            page = urllib.request.urlopen(self.baseUrl + startLink)
            # parse the html using beautiful soup and store in variable `soup`
            soup = BeautifulSoup(page, 'html.parser')
            nextLink = soup.find("a", class_="mw-nextlink")

            if nextLink:
                newLink = nextLink.get('href')
                print(newLink)
                try:
                    self.globalUserExtractor(newLink)
                except RecursionError:
                    print(newLink)
                    self.fileWriter()




    def globalUserExtractor(self, startLink):

        try:
        # parse the html using beautiful soup and store in variable `soup`
            page = urllib.request.urlopen(self.baseUrl + startLink)
            soup = BeautifulSoup(page, 'html.parser')
            name_box = soup.find('ul')

            if name_box is not None:
                for li in name_box:
                    item = li.find('a')
                    try:
                        self.accountList.append(item.get('href').replace('/wiki/Special:CentralAuth/', ''))
                        if len(self.accountList) >= 500000:
                            self.fileWriter()
                            self.accountList = []
                    except AttributeError:
                        print(item)
            else:
                print(startLink)
                self.fileWriter()
                self.accountList = []

            self.pageNavigator(startLink)

        except (http.client.IncompleteRead) as e:
            print(e)
            # page = e.partial
            print(startLink)
            self.fileWriter()

        except (urllib.error.HTTPError) as e:
            print(e)
            # page = e.partial
            print(startLink)
            self.fileWriter()
        except ConnectionResetError:
            print(startLink)
            self.fileWriter()

    def fileWriter(self):
        with open('globalUserList.txt', 'a+') as f:
            for user in self.accountList:
                f.write("%s\n" % user)
            f.close()


###

def main():
    # other_path = '/Users/alessandro/Documents/PhD/WD_ontology'
    # startLink = '/w/index.php?title=Special:GlobalUsers&offset=&limit=5000'
    # startLink = '/w/index.php?title=Special:GlobalUsers&offset=Ag2solo&limit=5000'
    # startLink = '/w/index.php?title=Special:GlobalUsers&offset=Arsh_Masroofi&limit=5000'
    #startLink = '/w/index.php?title=Special:GlobalUsers&offset=Bmemma&limit=5000'
    startLink = '/w/index.php?title=Special:GlobalUsers&offset=Ckom9000&limit=5000'

    userGetter(startLink)


if __name__ == "__main__":
    main()
