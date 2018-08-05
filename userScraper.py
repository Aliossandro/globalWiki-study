import urllib
from bs4 import BeautifulSoup
import pandas as pd
import os

#specify url
# userList = ['Harmonia Amanda', 'Jura1', 'Sannita', 'Alessandro Piscopo', 'TomT0m', 'GerardM']


def userCrawler(userName):
    page_url = 'https://en.wikipedia.org/wiki/Special:CentralAuth/'
    #query url
    query_url = page_url + userName
    page = urllib.request.urlopen(query_url)

    # parse the html using beautiful soup and store in variable `soup`
    soup = BeautifulSoup(page, 'html.parser')

    # Take out the <div> of name and get its value
    name_box = soup.find('table')
    # name_box.find('<tbody>')
    table_body = name_box.find('tbody')


    rows = table_body.find_all('tr')
    data = []
    for row in rows:
        cols = row.find_all('td')
        img = row.find('img')
        homeWiki = img.get('title')
        cols = [ele.text.strip() for ele in cols]
        if homeWiki != 'created on login':
            cols[2] = homeWiki
        data.append([ele for ele in cols if ele]) # Get rid of empty values

    return data

def userDataset(userList):
    userData = pd.DataFrame(columns=['user_name', 'local_wiki', 'attached_on', 'method', 'blocked', 'edit_count', 'groups'])
    counter = 0
    for user in userList:
        user = user.replace(' ', '_')
        try:
            tempDf = pd.DataFrame(userCrawler(user))
            if tempDf.shape[1] == 5:
                tempDf['groups'] = 'NA'
            tempDf.columns = ['local_wiki', 'attached_on', 'method', 'blocked', 'edit_count', 'groups']
            tempDf['user_name'] = user
            userData = userData.append(tempDf)
            if counter == 2500:
                if os.path.isfile('./userDataWM.csv'):
                    #clean the data
                    userData['edit_count'] = userData['edit_count'].str.replace(',', '')
                    userData['edit_count'] = userData['edit_count'].astype(int)
                    userData['attached_on'] = pd.to_datetime(userData['attached_on'], format='%H:%M, %d %B %Y')
                    userData['method'] = userData['method'].str.replace('[(?)]', 'None')
                    userData['method'] = userData['method'].str.replace('NoneNoneNone', 'None')
                    userData['local_wiki'] = userData['local_wiki'].str.replace('.org', '')
                    userData['language'], userData['project'] = userData['local_wiki'].str.split('.', 1).str

                    userData.to_csv('userDataWM.csv', mode='a', index=False, header=False)
                    userData = pd.DataFrame(columns=['user_name', 'local_wiki','attached_on', 'method', 'blocked', 'edit_count', 'groups'])
                    counter = 0
                else:
                    #clean the data
                    userData['edit_count'] = userData['edit_count'].str.replace(',', '')
                    userData['edit_count'] = userData['edit_count'].astype(int)
                    userData['attached_on'] = pd.to_datetime(userData['attached_on'], format='%H:%M, %d %B %Y')
                    userData['method'] = userData['method'].str.replace('[(?)]', 'None')
                    userData['method'] = userData['method'].str.replace('NoneNoneNone', 'None')
                    userData['local_wiki'] = userData['local_wiki'].str.replace('.org', '')
                    userData['language'], userData['project'] = userData['local_wiki'].str.split('.', 1).str

                    userData.to_csv('userDataWM.csv', index=False, header=True)
                    userData = pd.DataFrame(columns=['user_name', 'local_wiki','attached_on', 'method', 'blocked', 'edit_count', 'groups'])
                    counter = 0
        except:
            print(user, 'not found')
        counter += 1

    #clean the data
    userData['edit_count'] = userData['edit_count'].str.replace(',', '')
    userData['edit_count'] = userData['edit_count'].astype(int)
    userData['attached_on'] = pd.to_datetime(userData['attached_on'], format='%H:%M, %d %B %Y')
    userData['method'] = userData['method'].str.replace('[(?)]', 'None')
    userData['method'] = userData['method'].str.replace('NoneNoneNone', 'None')
    userData['local_wiki'] = userData['local_wiki'].str.replace('.org', '')
    userData['language'], userData['project'] = userData['local_wiki'].str.split('.', 1).str

    if os.path.isfile('./userDataWM.csv'):
        userData.to_csv('userDataWM.csv', mode='a', index=False, header=False)
    else:
        userData.to_csv('userDataWM.csv', index=False, header=True)

def main():
    # other_path = '/Users/alessandro/Documents/PhD/WD_ontology'
    other_path = '/data/wpDumps'
    other_file = other_path + '/userRoles.csv'
    userRoles = pd.read_csv(other_file)
    userList = list(userRoles['username'])
    userDataset(userList)


if __name__ == "__main__":
    main()

