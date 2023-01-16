#!/usr/bin/python3
#to get file status
#Xunliang Liu
#First Created: Mar 6, 2016

import os.path
import time
from datetime import datetime as dt

def dtFormat(date_time):
    '''this function takes a datetime object and return a fomarted current day and current time as tuple''' 
    current_date = date_time.strftime('%Y-%m-%d,%a')
    current_time = date_time.strftime('%H:%M:%S')
    return current_date, current_time
    
logmtime = time.ctime(os.path.getmtime('./log/log.txt'))
logmtime = dt.strptime(logmtime, '%c')
#print(logmtime)
print('log last modified:',dtFormat(logmtime_convert)[0])
print('today:',dtFormat(logmtime_convert)[0])
if dtFormat(dt.today())[0] != dtFormat(logmtime_convert)[0]:
    with open('./log/log.txt','at') as log:
        print('writing log')
        log.write(dtFormat(dt.today())[0])
        log.write('\r\n')