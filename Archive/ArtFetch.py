#to test the artical info retrive function
#Jan 10,2016
#Xunliang

import re
import urllib2
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
artURL_list=list()
homeURL = 'http://www.cell.com'

issueList=list()
issueInfo=dict()
with open('issue_list.csv','r') as issues:
    issList = issues.readlines()
    for line in issList:
        issTemp = line.strip().split(',')
        # print issTemp
        # raw_input('issue list')
        if 'http' in issTemp[5]:
                issueInfo['date'] = issTemp[0]
                issueInfo['year'] = issTemp[1]
                issueInfo['vol'] = issTemp[2]
                issueInfo['issue'] = issTemp[3]
                issueInfo['page'] = issTemp[4]
                issueInfo['url'] = issTemp[5]
                issueList.append(dict(issueInfo))

artInfo = dict()
artList = list()
artNum = 0
searchlist = open('searchlist.txt','r').read().split(';')
ArtListFile = open('CellarticleList.txt','wb')  
for issue in issueList:
    ln = issue['url']
    print 'issue link', ln
    iss_page = opener.open(ln).read()
    # artEntry = re.findall('<!--ENTRIES.*PDF',iss_page)
    # artChunk = ''.join(artEntry)
    artChunks = re.findall('<!--S.*?PDF',iss_page) #find individual article information
    print len(artChunks), 'articles found'
    #artChunks = artChunk.split('</span></div>')
    for art in artChunks:
        artNum += 1
        """to get article ID"""
        artID = ''.join(re.findall('<!--(S[0-9]{4}.*)-->',art))
        print 'Article ID:', artID
        artInfo['id'] = artID
        """to get article url"""
        artURL = homeURL + '/cell/fulltext/' + artID
        artInfo['url'] = artURL
        artPDF = homeURL + '/cell/pdf/' + artID + '.pdf'
        artInfo['pdf'] = artPDF
        art_source = opener.open(artURL).read() #retrieve the content of full text page
        """to get article bibliography"""
        artInfo['pagef'] = 'NA'
        artInfo['pagel'] = 'NA'
        artBio = re.findall('(Volume\s[0-9].+?Issue\s+?[0-9].*?)</div>',art_source)
        if artBio:
            artBio =''.join(artBio).split(',')
            page = re.findall('[0-9]+',artBio[2])
            #print 'artBio:',artBio
            #print 'pages:',page
            artInfo['pagef'] = page[0]  #start page
            #artInfo['pagel'] = page[1]
        else:
            print 'page code is not found'
        """to get article label"""        
        artType = re.findall('artLabel">(.*?)<', art_source)
        if len(artType) > 0:
            artInfo['type'] = artType[0].strip()
        else:
            artInfo['type'] = 'No Label Found'
        print 'Article type:', artInfo['type']
        """to get corresponding authors"""   
        artCorrAu = re.findall('Corresponding author.*?>([A-Z][^0-9</>:]+?)</div>', art_source)
        if len(artCorrAu)>0:
            artInfo['corrau'] = ';'.join(artCorrAu)
        else:
            artInfo['corrau'] = 'NA'
        print "corresponding authers", artInfo['corrau']
        """to get email of corresponding authors"""         
        artmail = re.findall('mailto:(.*?)"',art_source)
        if len(artmail)>0:
            artInfo['mail'] = ';'.join(artmail)
        else:
            artInfo['mail'] = 'NA'
        print 'contact infomation', artmail
        """to get corresponding authors Affiliations""" #return a tuple; need to join
        affi_temp = re.findall('Corresponding author.*?>Affiliations<.*?>([A-Z].*?)<.*?>([A-Z].*?)<', art_source)
        affi = list()
        if len(affi_temp)>0:
            for Ins in affi_temp:
                if not type(Ins) is str:
                    Insjoin = ';'.join(Ins)
                if Ins not in affi:
                    affi.append(Insjoin)
        else:
            affi = ['NA']
        print 'affi:',affi
        artInfo['affi'] = ';'.join(affi)
        """to get article title""" 
        artTI_raw =''.join(re.findall(re.escape(artID) + '-title".*rightTitleInfo',art))    #retrieve a raw title; re.escape() is used so that  
                                                                                            #the variate artID can be used in regular expression
        artTI = ''.join(re.findall(re.escape(artID) + '">(.*)</a>',artTI_raw)).strip()      #cleanup the title; re.escape() is used as before
        artTI = re.sub('<.*?>','',artTI)
        artInfo['title'] = artTI
        print 'Title:', artTI
        """to get article author list""" 
        artAu_raw = ''.join(re.findall(('id="' + re.escape(artID) + '-au">(.*)</.*DOI'),art))
        artAu = artAu_raw.split(',')                                                        #split authers to a list
        artInfo['authers'] = ';'.join(artAu)

        artInfo['bio'] = issue['vol'] + '(' + issue['issue'] + ')'
        artInfo['date'] = issue['date'].split()[0].strip()[:3] + ' ' + issue['date'].split()[1].strip()
        artInfo['year'] = issue['year']
        #artBio = re.findall('artBio">".*?(Volume\s[0-9]{,3}.*?)</div>',art_source)

        artList.append(dict(artInfo))
        artDate = artInfo['year'] + ' ' + artInfo['date'] 
        artSum = [artDate,artInfo['bio'],artInfo['pagef'], artInfo['type'],artInfo['authers'],artInfo['corrau'], artInfo['mail'], artInfo['affi'],artInfo['title'],artInfo['url'],artInfo['pdf']]
        ArtListFile.writelines('\t'.join(artSum))
        ArtListFile.write('\r\n')
        print 'article list updated', artNum
        
       
# with open('articleList.csv','wb') as ArtListFile:
    # for art in artList:
        # artDate = art['year'] + ' ' + art['date'] 
        # artSum = [artDate,art['vol'],art['type'],art['authers'],art['title'],art['url']]
        # ArtListFile.writelines(','.join(artSum))
        # ArtListFile.write('\r\n')
