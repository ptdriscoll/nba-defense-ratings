# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 17:24:59 2017

@author: pdriscoll
"""

import urllib2
from bs4 import BeautifulSoup

url = 'https://en.wikipedia.org/wiki/List_of_NBA_champions'
winners = []
losers = []
years = []
games = []

try:
    html = urllib2.urlopen(url).read()
except:
    '\nURL could not be opened'
    html = ''

soup = BeautifulSoup(html, "lxml")
table = soup.find('span', id='NBA_champions').parent.find_next_sibling('table')
rows = table.find_all('tr', recursive=False)
for row in rows:
    cells = row.find_all('td')
    
    i = 0
    for cell in cells:
        if i == 0: 
            year = cell.contents[0].text.strip()
            if int(year) < 1997: break
            years.append(year)    
        if i == 1 or i == 3: 
            team = cell.contents[0].text.strip()
            attrs = cell.attrs
            if attrs and attrs['style'] == 'background:#FFFF99': 
                team = team[:-4].strip()
                winners.append(team)
            else:
                losers.append(team)    
        if i == 2:
            first = cell.contents[0].strip()[:1] 
            second = cell.contents[0].strip()[2:]
            total_games = str(int(first) + int(second))
            games.append(total_games)
        
        i += 1    

print ''
print len(years), len(winners), len(losers), len(games)
print ''

with open('finals.csv', 'w') as file:
    csv = 'years,winners,losers,games\n'
    for x in range(len(years)):
        csv += years[x] + ',' + winners[x] + ',' + losers[x] +  ',' + games[x] + '\n' 
        print years[x], ' - ', winners[x], ' - ', losers[x], ' - ', games[x]
    file.write(csv)












