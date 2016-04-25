#!/usr/bin/python

# Plots the user logins for the past 30 days

import numpy
import matplotlib.pyplot as plt
import subprocess
import datetime

from collections import Counter

wtmp_loc = './'
history = 30
ignorenames = '[root,(unknown,system,reboot,wtmp]'
MonthMapping = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}

# calculate the furthest date we would like to see records from
today =  datetime.date.today()
today_date = datetime.datetime(today.year, today.month, today.day)
#hist_date = hist_date.strftime('%Y:%m:%d')

#hist_year = int(hist_date.split(':')[0])
#hist_month = int(hist_date.split(':')[1])
#hist_day = int(hist_date.split(':')[2])

#print hist_year
#print hist_month
#print hist_day

# get the initial data
searchresult = subprocess.Popen("last -FRf " + wtmp_loc + "wtmp*", stdout=subprocess.PIPE, shell=True)

searchresult = searchresult.communicate()[0]

login_list = []

# print searchresult
m = searchresult.split('\n')

for entry in m:
    username = entry.split(" ")[0]

    if username and username not in ignorenames:
        isuser = subprocess.Popen("getent passwd " + username, stdout=subprocess.PIPE, shell=True).communicate()[0]
        
        #print username + " " + isuser
        
        if isuser.count(':') == 6:
            #print username
            entry = ' '.join(entry.split())
        
            #print entry
            
            ent_year = entry.split(' ')[6] 
            ent_month = entry.split(' ')[3] 
            ent_day = entry.split(' ')[4] 

            #print ent_year + " " + ent_month + " " + ent_day

            ent_date = datetime.datetime.strptime(ent_month + " " + ent_day + " " + ent_year , '%b %d %Y')

            #print ent_date

            if (today_date-ent_date).days <= history:
               login_list.append(username)

print Counter(login_list).keys()
print Counter(login_list).values() 

N = len(Counter(login_list).keys())

width = 1/1.5

plt.bar(range(len(Counter(login_list).keys())), Counter(login_list).values(), width, color='black', align='center')

plt.xticks(range(len(Counter(login_list).keys())), Counter(login_list).keys())

plt.show()
