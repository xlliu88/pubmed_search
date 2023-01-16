#for webpage content fecth
#Jan 9, 2015
#Xunliang Liu

import urllib2
import re
import datetime

today = datetime.datetime.today()
now = datetime.datetime.now()
#log = open('log.txt','a')

opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
decURL_list=list()
homeURL = 'http://www.cell.com'

for dec in range (200,202):
    decURL = homeURL + '/archive?decade=' + str(dec) + '&amp;widget=14602d51-93c2-4a08-ac06-050ec31e8707#loi_decade_' + str(dec)
    print decURL
    decURL_list.append(decURL)

issueList = list()
issueInfo = dict()
#mo = ['January','February','March','April','May','June','July','August','September','October','November','December']

#retrive a list of issues
for ln in decURL_list:
    sock = opener.open(ln)
    arch_page = sock.read()
    #issList = re.findall('volume-header.*?(Volume\s[0-9]+?)<.*?(ref.*?p[0-9]+?\D[0-9]+?)\D',arch_page) #find issue information and put them into a list,
                                                                                                        #doesn't work
    issBlock = re.findall('>Open Archive<.*p[0-9]+?-[0-9]{0,4}', arch_page)                                                 
    if len(issBlock) > 0:
        issList = issBlock[0].split('</a>')
        print len(issList), 'issue found'                               
        for issue in issList:
            #print issue
            #raw_input('this is one issue\n')
            volName = re.findall('Volume\s[0-9]{1,3}',issue)
            if len(volName)==1:
                vol=volName[0]
            issURL = re.findall('href="(.*X[0-9]+-[X0-9])',issue)
            issDate = re.findall('<strong>\s(.*,\s[0-9]{4})',issue)
            issNo = re.findall('Issue\s.+p.+-[0-9]{1,4}',issue)
            if len(issURL)==1 and len(issDate)==1 and len(issNo)==1:
                issDate = issDate[0].strip().split(',')
                issNo = issNo[0].strip().split(',')
                issueInfo['vol']=vol.split()[1].strip()
                issueInfo['num']=issNo[0].split()[1].strip()
                issueInfo['page']=issNo[1].strip()
                issueInfo['date']=issDate[0].split()[0].strip()[:3] + ' ' + issDate[0].split()[1].strip()
                issueInfo['year']=issDate[1].strip()
                issueInfo['url']=homeURL+issURL[0]
                issueList.append(dict(issueInfo))

#write issue list to file issue_list.csv            
with open('issue_list.csv','wb') as issues:
    title = ['Date','Year','Volume','Issue','page','URL']
    issues.write(','.join(title))
    issues.write('\n')
    for issue in issueList:
        iss = [issue['date'],issue['year'],issue['vol'],issue['num'],issue['page'],issue['url']] 
        issues.write(','.join(iss))
        issues.write('\n')




