from Bio import Entrez as E
import os
import re
import sys
from datetime import datetime as dt
import itertools as it
import time

def logupdate(str = ''):
    ''' update the log file'''
    logmtime = time.ctime(os.path.getmtime('./log/log.txt'))
    logmtime = dt.strptime(logmtime, '%c')
    with open('./log/log.txt','at') as log:
        if str == '':
            if dtFormat(dt.today())[0] == dtFormat(logmtime)[0]:
                print('update log date')
                log.write(dtFormat(dt.today())[0])
                log.write('\r\n')
        else:
            print ('update log info')
            log.write(str)
            log.write('\r\n')
def dtFormat(date_time):
    '''this function takes a datetime object and return a fomarted current day and current time as tuple''' 
    current_date = date_time.strftime('%Y-%m-%d,%a')
    current_time = date_time.strftime('%H:%M:%S')
    return current_date, current_time            
            
logupdate()
logupdate('%s %s'%(dtFormat(dt.today())[1], 'search term'))