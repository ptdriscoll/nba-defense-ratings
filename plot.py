# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 18:51:58 2017

@author: pdriscoll

NOTES: 
--All files, including two csv files and two Python scripts used to scrape the data, can be found at:
  https://github.com/ptdriscoll/nba-defense-ratings 
--All Python files for this application are written in Python 2.7  

"""

import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.lines as mlines


'''
run ttest 
'''

df = pd.read_csv('data/ratings.csv')
print df

#check averages and statistical significance
winners = df['ratings_winners'].mean()
losers = df['ratings_losers'].mean()
print '\nWINNER AVERAGE:', winners, '\nLOSER AVERAGE:', losers

ttest = stats.ttest_ind(df['ratings_winners'], df['ratings_losers'])
print '\nTSTAT:', ttest[0], '\nPVALUE:', ttest[1] 

print '\n\n\n'


'''
plot graphs
'''

#plot averages of winners and losers
#colors from colorbrewer2.org
colors = ['#d7191c', '#3182bd']
#colors = ['#de2d26', '#2c7bb6']

text_color = '#777777'
alpha = 0.8  

fig, axes = plt.subplots(1,2, figsize=(11,4), 
      gridspec_kw = {'width_ratios': [1,3]},
      sharey=False)
ax1, ax2 = axes
   
bars = ax1.bar([1,2], [winners, losers], 
        width=0.85, color=colors, alpha=alpha, 
        linewidth=0, align='center')       

#plot timeline of winners and losers
ax2.plot(df['years'], df['ratings_winners'], 
         color=colors[0], linewidth=2)
         
ax2.plot(df['years'], df['ratings_losers'], 
         color=colors[1], linewidth=2)      


'''
customize ax1  
''' 

#remove y and x labels on ax1 
for ytick in ax1.yaxis.get_major_ticks():
    ytick.set_visible(False)

for xtick in ax1.xaxis.get_major_ticks():
    xtick.set_visible(False)
   
#add y values to bars
for bar in bars:
    ax1.text(bar.get_x() + bar.get_width()/2, 
            bar.get_height() - 12, 
            str(int(bar.get_height())), 
            ha='center', color='w', fontsize=15)
      
                 
'''
customize ax2  
''' 

#add fill
ax2.fill_between(df['years'],
                 df['ratings_losers'], 0,
                 facecolor=colors[1],
                 alpha=0.08)

ax2.fill_between(df['years'],
                 df['ratings_winners'], 0,
                 facecolor=colors[0],
                 alpha=0.08)

#set x to stretch to both sides of frame
ax2.set_xlim(xmin=1997, xmax=2016)

#make sure both subplots are on same y axis 
ax2.set_ylim(ymin=0)

#remove top and bottom y labels on ax2
yticks = ax2.yaxis.get_major_ticks()
yticks[0].set_visible(False)

#move y labels to left
ax2.tick_params(axis='y', which='both', pad=5)

#add light grid
ax2.grid(True)
gridlines = ax2.get_xgridlines() + ax2.get_ygridlines()
for line in gridlines:
    line.set_linestyle('-.')
    line.set_color('#333333')

#show more ticks 
ax2.xaxis.set_major_locator(ticker.MultipleLocator(2))

#format years to show only two digits
labels = ['96', '98','00','02','04','06','08','10','12','14','16']
ax2.set_xticklabels(labels)


'''
set title and major labels  
'''  

#add title 
title = fig.suptitle('Defense Ratings for Winning and Losing Teams in NBA Finals', 
          color=text_color, size=20, y=1.218, x=0.5) 
      
#add major y label
labelsize = 15          
ax1.set_ylabel('Defense Ratings', color=text_color, size=labelsize, y=0.66)
ax1.tick_params(axis='y', which='both', pad=-3)

#add major x labels
ax1.set_xlabel('20-Year Averages', color=text_color, size=labelsize, x=0.5)
ax2.set_xlabel('Yearly NBA Finals Matchups', color=text_color, size=labelsize)

ypad = 16
ax1.xaxis.labelpad = ypad
ax2.xaxis.labelpad = ypad


'''
add legend  
'''  

text_color_leg = '#444444'

linewidth = 8.0
win_legend = mlines.Line2D([], [], color=colors[0], alpha=alpha, 
           label='Winners', linewidth=linewidth)
los_legend = mlines.Line2D([], [], color=colors[1], alpha=alpha, 
            label='Losers', linewidth=linewidth)
legend = plt.legend(handles=[win_legend, los_legend], 
                    loc='top center', ncol=2,
                    frameon=False, bbox_to_anchor=(0.286, 1.25))

for text in legend.get_texts():
    plt.setp(text, color=text_color_leg)
            
fig.text(0.545, 1.05, 'Source: stats.nba.com',
            fontsize=12, color=text_color_leg)    
            
          
'''
more prettifying for both  
'''

#remove all tick parameters, lighten colors, and make text smaller
for ax in axes:
    ax.tick_params(top='off', right='off', bottom='off', left='off', 
                   colors=text_color, labelsize=14, which='both')
                   
    #get rid of frames
    for spine in ax.spines.values():
        spine.set_color('none')

'''
print results
'''

plt.tight_layout()
plt.savefig('nba_defense.jpg', dpi=55,
            bbox_inches='tight', bbox_extra_artist=[title]) 
plt.show()

