#for webpage content fecth
#Jan 9, 2015
#Xunliang Liu

import urllib2
import re

opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
decURL_list=list()
homeURL = 'http://www.cell.com'

for dec in range (200,202):
    decURL = homeURL + '/archive?decade=' + str(dec) + '&amp;widget=14602d51-93c2-4a08-ac06-050ec31e8707#loi_decade_' + str(dec)
    decURL_list.append(decURL)

issueList = list()
issueInfo = dict()
mo = ['January','February','March','April','May','June','July','August','September','October','November','December']
for ln in decURL_list:
    sock = opener.open(ln)
    arch_page = sock.readlines()
    for line in arch_page:
        if 'OpenArchiveIssues' in line:
            lines = line.split('issueName')
            if len(lines) >2:            
                for line in lines:
                    if 'issueLinkCon' in line:
                        alist = line.split('<')
                        for piece in alist:
                            if 'href' in piece:
                                URL = piece.split('"')[1]
                                if not 'loi_decade' in URL:
                                    issueInfo['url'] = homeURL + URL
                            elif any(word in piece for word in mo):
                                issueInfo['date'] = piece.split('>')[1].strip()
                            elif 'Issue' in piece:
                                piece = piece.split('>')[1].strip().split(',')
                                if len(piece)>1:
                                    issueInfo['issue'] = piece[0]
                                    issueInfo['page'] = piece[1]
                                    
                        issueList.append(dict(issueInfo))

with open('issues.csv','wb') as issues:                            
    for issue in issueList:
        print issue
        item = [issue['date'],issue['issue'],issue['page'],issue['url']]
        issues.write(','.join(item))
        issues.write('\n')
     
                
                    
                    
                    
