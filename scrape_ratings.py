# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 10:05:40 2017

@author: pdriscoll
"""

import pandas as pd
import requests
from urllib2 import URLError
import socket
import json
import time

#Basic link settings to get defense ratings (set to most recent year)
url = 'http://stats.nba.com/stats/leaguedashteamstats?Conference=&DateFrom=&DateTo=&Division=&GameScope=&GameSegment=&LastNGames=7&LeagueID=00&Location=&MeasureType=Defense&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=2015-16&SeasonSegment=&SeasonType=Playoffs&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision='
 
#set headers
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.107 Safari/537.36','Upgrade-Insecure-Requests': '1','x-runtime': '148ms'}

#get NBA finals winners and losers    
df = pd.read_csv('finals.csv')
print '\n', df.head() 

#empty lists to store winner and loser defense ratings
ratings_winners = []
ratings_losers = []

print ''

#loop through dataframe and get defense ratings for winners and losers
for index, row in df.iterrows():
    year = row.years
    winner = row.winners
    loser = row.losers
    games = row.games

    season = 'Season=' + str(year-1) + '-' + str(year)[2:]
    Ngames = 'LastNGames=' + str(games)
    search_url = url.replace('Season=2015-16', season)
    search_url = search_url.replace('LastNGames=7', Ngames)
    #print season
    
    #get json data for each finals playoff
    try:
      response = requests.get(search_url, headers=headers, allow_redirects=True).content
      print '\nURL opened'    
    except URLError as e:
      print '\nCould not open URL:\n', search_url,'\n'
      print e.code
      print e.read()  
      response = False   
    except socket.timeout:
      print '\nSocket timed out' 
      response = False
            
    if response: 
      data = json.loads(response)
      data = data['resultSets'][0]['rowSet']
      #print json.dumps(data[1], sort_keys=True, indent=4, separators=(',', ': '))
      #print '\n',data[1][1]
      #print '\n',data[1][7]
    else: data = 'No data'
    
    #now get data from each page into dataframe
    looking_for_winner = True
    looking_for_loser = True
    
    for x in range(len(data)):
        if looking_for_winner and data[x][1] == winner: 
            ratings_winners.append(data[x][7])
            looking_for_winner = False
        if looking_for_loser and data[x][1] == loser:            
            ratings_losers.append(data[x][7])
            looking_for_loser = False
            
    if looking_for_winner: ratings_winners.append('')    
    if looking_for_loser: ratings_losers.append('')  
        
    #slow down the server requests        
    time.sleep(1)        

print '\n',len(ratings_winners), len(ratings_losers)

#add defense ratings lists to dataframe
se_ratings_winners = pd.Series(ratings_winners)
se_ratings_losers = pd.Series(ratings_losers)
df['ratings_winners'] = se_ratings_winners.values
df['ratings_losers'] = se_ratings_losers.values

print '\n',df
df.to_csv('ratings.csv', index=False, encoding='utf-8')
















