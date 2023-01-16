#!/usr/bin/python
#This script is aim to fetch articals from PubMed via Entrez
#Xunliang
#start date: March 3, 2016
#Last modified: March 3, 2016

from Bio import Entrez as Ez
import itertools as it
from datetime import datetime as dt
import time
import os
import re
import sys
import shutil

def help():
    '''it prints some help information'''
    print ('==== search parameters =============================================')
    print ('-f  search full field')
    print ('    * -f can be omitted')
    print ('    * when it is omitted, it has to be put as the first argument')
    print ('-t  search title')
    print ('-b  search abstract')
    print ('-a  search authors')
    print ('-j  search journals')
    print ('-d  limit the publish data')
    print ('    * date format: -d yyyy/mm:yyyy/mm')
    print ('    * month can be ommitted')
    print ('    * if ":" is ommitted, it will only take the first yyyy/mm for search')
    print ('    * when the start year is ommitted (e.g. -d :2010), it will start from 1900/1')
    print ('    * when the end year is ommitted (e.g. -d 2010:), it will end at the current month')
    print ('-h  print help infomation')
    print ('search example:')
    print ('-f arabidopsis -t LORELEI -a palanivelu -j plant journal -d 2008:2010')
    print ('=== help info END ====================================================')
def logupdate(str = ''):
    ''' update the log file'''
    logmtime = time.ctime(os.path.getmtime('./log/log.txt'))
    logmtime = dt.strptime(logmtime, '%c')
    if logmtime.year != dt.today().year:    #backup log to archive every year.
        shutil.copy2('./log/log.txt','./Archive/%s-log.txt'%logmtime.year)
        with open ('./log/log.txt','wt') as log:
            log.write('### %s'%dtFormat(dt.today())[0])
            log.write('\r\n')            
    with open('./log/log.txt','at') as log:
        if str == '':
            if dtFormat(dt.today())[0] != dtFormat(logmtime)[0]:    #if the last modified date is not today, add a date line
                log.write('### %s'%dtFormat(dt.today())[0])
                log.write('\r\n')
        else:
            log.write(str)
            log.write('\r\n')
def dRemove(rawList):
    '''this function removes duplicates in a list
    '''
    unique_list= list()
    for item in rawList:
        if not item in unique_list:
            unique_list.append(item)
    return sorted(unique_list,reverse = True)
def dtFormat(date_time):
    '''this function takes a datetime object and return a fomarted current day and current time as tuple''' 
    current_date = date_time.strftime('%Y-%m-%d,%a')
    current_time = date_time.strftime('%H:%M:%S')
    return current_date, current_time
def take_terms():
    '''
    this function promp user to enter search terms
    '''
    search_terms = dict()
    help()
    term = input('Search: ')
    return term
def dic_split(dic):
    '''this function generate all combinations of list values of a dict, 
        and return a list of dicts
    '''
    dic_list = list()
    dic_sorted = sorted(dic)
    dic_list = [ [{key: val} for key, val in zip(dic_sorted, prod)] 
                for prod in it.product(*(dic[key] for key in dic_sorted))]
    
    dic_list_merged = list()
    for i in dic_list:
        dic_temp = dict()
        for j in i:
            dic_temp.update(j)
        dic_list_merged.append(dict(dic_temp))
    return dic_list_merged
def file_parse():
    '''this function takes settings from file ./config/quary_keys.txt and   
            take search settings into a dictionary.
        it will call function dict_split() to split the dictionary to a list of dictionaries
            if any of its value is a list
    '''
    search_terms = dict()
    with open('./config/quary_keys.txt','rt') as quary_keys:
        for line in quary_keys:
            if not line.startswith('#',0,1):  #ignore lines start with '#'
                line = line.split('=')
                if len(line) >= 2 and line[1].strip():  #take values only if it's not empty on the right side of '='
                    v = [text.strip() for text in line[1].split(',')]   #strip white space flanking each search term
                    search_terms[line[0].strip()] = v
   
    return search_terms
def term_parse(usrInput):
    '''this function parse user's input and return it as a dict()'''
    '''when print help, it will return 0 '''
    current_date = '%s/%s' % (str(dt.today().year),
                    str(dt.today().month)) 
    #replace ';' and ':' to space
    #usrInput = re.sub(',', ' ', usrInput)
    usrInput = re.sub(';', ' ', usrInput)
    #usrInput = re.sub(':', ' ', usrInput)
    arguments = usrInput.split('-')
    search_term = dict()
    search_terms = list()
    if arguments[0] != '':
        if arguments[0].lower() == 'file':  #if the first parameter is 'file', call file_parse()
            return file_parse()
        else:
            search_term['word'] = arguments[0].split(',')
    for argu in arguments[1:]:
        argu_content = argu.split(' ')
        if argu_content[0].lower() == 'f':
           search_term['word'] = ' '.join(argu_content[1:]).strip().split(',')
        elif argu_content[0].lower() == 't':
            search_term['TI'] = ' '.join(argu_content[1:]).strip().split(',')
        elif argu_content[0].lower() == 'b':
            search_term['TIAB'] = ' '.join(argu_content[1:]).strip().split(',')
        elif argu_content[0].lower() == 'a':
            search_term['AU'] = ' '.join(argu_content[1:]).strip().split(',')
        elif argu_content[0].lower() == 'j':
            search_term['JOUR'] = ' '.join(argu_content[1:]).strip().split(',')
        elif argu_content[0].lower() == 'd':
            search_term['PDAT'] = ' '.join(argu_content[1:]).strip().split(',')
            for pdat in search_term['PDAT']:
                if ':' in pdat:
                    if pdat.split(':')[0] and not pdat.split(':')[1]:
                        print('set end date to current time')
                        search_term['PDAT'][search_term['PDAT'].index(pdat)] = '%s:%s'%(pdat.split(':')[0], current_date)
                    elif not pdat.split(':')[0] and pdat.split(':')[1]:
                        search_term['PDAT'][search_term['PDAT'].index(pdat)] = '%s:%s'%('1900/1',pdat.split(':')[1])
        elif argu_content[0].lower() == 'v':
            search_term['VOL'] = argu_content[1].strip().split(',')
        elif argu_content[0].lower() == 'p':
            search_term['PAGE'] = argu_content[1].strip().split(',')
        elif argu_content[0].lower() == 'o':
            search_term['AFFL'] = ' '.join(argu_content[1:]).strip().split(',')
        elif argu_content[0].lower() == 'h':
            help()
            sys.exit()
        else:
            print ('Unknown argument: %s' % argu.split(' ')[0].strip())
            print ('argument igored')

    #search_terms.append(search_term)
    for k,v in search_term.items(): #return search terms if one of the none date search key is not empty
        if not k == 'PDAT':
            if v:
                print('search term')
                return search_term
    print ('Error!!')
    print (' * NO key word found.')
    print (' * Please let me know what you are looking for.')
    exit(1)   
def get_id(search_terms, max = 5000):
    '''
    function takes search_terms and return the pubmed_ids as a list
    search_terms is a dict() generated by term_parse() function
    keys in search_terms: 'word', 'TI', 'TIAB', 'AU', 'JOUR', 'PDAT'
    '''
    term = ''    
    for k,v in search_terms.items():
        if v:
            term += '%s[%s] '%(v,k)
    print ('searching:%s'%term)
    handle = Ez.esearch(db="pubmed", term=term, retmax = max, usehistory = 'y')
    record = Ez.read(handle)
    handle.close()
    
    art_ids = []
    for id in record['IdList']:
        if id not in art_ids:
            art_ids.append(id)

    print ('Articles Found: %s\tArticles Retrieved: %d' % (record['Count'], len(art_ids)))
    logupdate('\t%s\tsearch: "%s"\tFound: %s\tRetrieved: %d'%(dtFormat(dt.today())[1], term, record['Count'],len(art_ids)))
    return art_ids
def update_search_summary():
    #print('#search summary updated')
    return 0
def authorInfo(authorList):
    '''it cleans up the author information from function artical_parse'''
    '''Add 'author type' into author information. Types: First, Corresponding, Other'''
    '''If there's co-first author, only the first one will be labeled as first author'''
    '''It can label multiple corresponding author, only if the email address is in author information'''
    newAuList = list()
    newAuInfo = {'LastName':'','ForeName':'','Initials':'','affi':'','type':''}
    for au in authorList:
        newAuInfo['LastName'] = au['LastName']
        newAuInfo['ForeName'] = au['ForeName']
        newAuInfo['Initials'] = au['Initials']
        try:
            newAuInfo['affi'] = au['AffiliationInfo'][0]['Affiliation']  #if an author has multiple affiliation, only take the first.
        except:
            pass
        if len(authorList) > 1:
            if authorList.index(au) == 0:
                newAuInfo['type'] = 'First'
            elif (authorList.index(au) == len(authorList)-1) or ('@' in newAuInfo['affi']):
                newAuInfo['type'] = 'Corresponding'
            else:
                newAuInfo['type'] = authorList.index(au) + 1
        else:
            newAuInfo['type'] = 'Corresponding'
        newAuList.append(dict(newAuInfo))
    
    #make corresponding/First author affiliation the same as First/corresponding author if it's empty
    for au in newAuList:
        if au['type'] == 'Corresponding' and not au['affi']:
            au['affi'] = newAuList[0]['affi']
        if au['type'] =='First' and not ['affi']:
            au['affi'] = newAuList[-1]['affi']
            
    return newAuList
def update_authorList(article = '', filename = ''):
    '''write author information into a csv file'''
    '''takes a list of dictionaries as argument'''
    if article == '':
        return 0
    if article == 'init':
        file_title = '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s'%('Name','Author Type', 'Article Type','pmid',
                                            'Journal','Year','Article title',
                                            'Author affiliation')
        with open('./results/authors_%s.txt'%filename,'wt') as authors:
            authors.write(file_title)
            authors.write('\r\n')
    else:
        with open('./results/authors_%s.txt'%filename,'at') as authors:
            for au in article['authors']:
                au['affi'] = re.sub(',',';',au['affi'])
                auInfo = '%s %s\t%s\t%s\t%s\t%s\t%s\t%s\t%s'%(au['ForeName'],au['LastName'],
                                                au['type'],article['type'],article['pmid'],
                                                article['jour'],article['year'],article['title'],
                                                au['affi'])  
                authors.write(auInfo)
                authors.write('\r\n')
    
        artBib = '%s %s.etal.,(%s) %s.%s:%s'%(article['authors'][0]['LastName'],article['authors'][0]['Initials'],article['year'],article['jour'],article['volume'],article['pages'])
        #print ('AUTHOR INFO UPDATED:%s'%artBib)
        logupdate('\t%s\tAUTHOR INFO UPDATED:%s'%(dtFormat(dt.today())[1],artBib))
def update_search_result(article = '', filename = ''):
    '''takes the result from article_parse and write it into html file'''
    from lxml import etree as ET
    from lxml.builder import E
    
    if article == '':
        return 0
    if not 'doi' in article.keys():
        article['doi'] = '' 
    jourInfo = '%s(%s).%s(%s):%s. doi:%s; PMID:%s'%(article['jour'],article['year'],
                                        article['volume'],article['issue'],article['pages'],
                                        article['doi'],article['pmid'])
    
    Names = ['%s %s'%(au['ForeName'],au['LastName']) for au in article['authors']]
    affiliation = [au['affi'] for au in article['authors'] if au['type'] == 'Corresponding']
    if not affiliation:
        affiliation = [au['affi'] for au in article['authors'] if au['type'] == 'First']
    affiliation = re.sub(',',';',affiliation[0])
    page = E.html(
            E.head(
                E.title('Search result')
                ),
                E.body(
                    E.span(
                        E.font(size = '4', color = '#6666FF', style = 'bold'),
                        article['type']
                        ),
                    E.br(),
                    E.font(color = '#000000',size = '3'),
                    E.span(jourInfo),
                    E.br(),
                    E.span(
                        E.font(size = '5', weight = '10'),
                        E.b(article['title'], CLASS = 'title')
                        ),
                    E.br(),
                    E.font(size = '4'),
                    E.p(
                        E.span(E.b(', '.join(Names))),
                        E.br(),
                        E.span('Affiliation: %s'% affiliation),
                        ),
                    E.p(
                        E.span(E.b('Abstract:')),E.br(),
                        article['abst']
                        ),
                    E.p(
                        E.span('URL:'),
                        E.a(article['url'],href = article['url'])
                        ),
                    ),
                E.hr(),
                #E.p('=================================================================================================================='),
            ) 
    html = ET.tostring(page, pretty_print=True)
    with open('./results/Searchresult_%s.html'%filename,'ab') as output:
        output.write(html)
        
    artBib = '%s %s.etal.,(%s) %s.%s:%s'%(article['authors'][0]['LastName'],article['authors'][0]['Initials'],
                        article['year'],article['jour'],article['volume'],article['pages'])
    #print ('SEARCH RESULT UPDATED:%s'%artBib)
    logupdate('\t%s\tSEARCH RESULT UPDATED:%s'%(dtFormat(dt.today())[1],artBib))
def get_article(pubmed_id):
    ''' this function takes pubmed_id list and retrieves artical information from PubMed.'''
    #Ez.email = 'xunliangliu@email.arizona.edu'
    handle = Ez.efetch(db = 'pubmed', id = pubmed_id, retmode = 'xml')
    return Ez.parse(handle)   #records is a generator.
def article_parse(record):
    article = {'title':'','abst':'','pmid':'','doi':'','pii':'','jour':'','year':'','month':'','day':'','volume':'','issue':'','pages':'','url':''}
    journal_home = {'Nature':'http://www.nature.com/journal', 
                    'Science':'http://science.sciencemag.org/content', 
                    'Cell':'http://www.cell.com/cell/full',
                    'PlantCell':'http://www.plantcell.org/content',
                    'pubmed':'http://www.ncbi.nlm.nih.gov/pubmed'}
    article['title'] = record['MedlineCitation']['Article']['ArticleTitle']   #return a string
    try:
        article['abst'] = ''.join(record['MedlineCitation']['Article']['Abstract']['AbstractText']) #return a string
    except:
        pass
    article['pmid'] = record['MedlineCitation']['PMID'].title()
    try:
        article['jour'] = record['MedlineCitation']['Article']['Journal']['ISOAbbreviation']
    except:
        article['jour'] = record['MedlineCitation']['Article']['Journal']['title']

    # for k,v in record['MedlineCitation']['DateCreated'].items():
        # article[k.lower()] = v
    for k,v in record['MedlineCitation']['Article']['Journal']['JournalIssue'].items():
        if k == 'PubDate':
            for subk,subv in v.items():
                article[subk.lower()] = subv
        else:
            article[k.lower()] = v
    article['pages'] = record['MedlineCitation']['Article']['Pagination']['MedlinePgn']

    try:    #get article author information
        article['authors'] = record['MedlineCitation']['Article']['AuthorList'] #return a list of dictionaries
        article['authors'] = authorInfo(article['authors'])
    except: #return an empety string if author info is not found
        return ''
    
    #get article type. 'Journal Article', 'Review'
    artTypeList = [tp.title() for tp in record['MedlineCitation']['Article']['PublicationTypeList']]
    if 'Review' in artTypeList:
        article['type'] = 'Review'
    elif 'Journal Article' in artTypeList:
        article['type'] = 'Journal Article'
    else:
        article['type'] = artTypeList[0]

    idlist = record['PubmedData']['ArticleIdList'] #return a list of ids. id types: 'pii', 'doi', 'pubmed'
    for id in idlist:
        article[id.attributes['IdType']] = id.title()
    
    #get url of the article
    if article['jour'].lower() == 'nature':
       article['url'] = '%s/v%s/n%s/%s.html'% (journal_home['Nature'],article['volume'],article['issue'],article['pii'])
    elif article['jour'].lower() == 'science':
        article['url'] = '%s/%s/%s/%s.full'% (journal_home['Science'],article['volume'],article['issue'],article['pages'].split('-')[0])
    elif article['jour'].lower() == 'cell':
        article['url'] = '%s/%s.html'%(journal_home['Cell'],article['pii'])
    elif article['jour'].lower() == 'the plant cell':
        article['url'] = '%s/%s/%s/%s.full'% (journal_home['PlantCell'],article['volume'],article['issue'],article['pages'].split('-')[0])
    else:
        article['url'] = '%s/%s'%(journal_home['pubmed'], article['pmid'])
    
    artBib = '%s %s.etal.,(%s) %s.%s:%s'%(article['authors'][0]['LastName'],article['authors'][0]['Initials'],
                        article['year'],article['jour'],article['volume'],article['pages'])
    print ('ARTICLE RETRIEVED:%s'%artBib)
    logupdate('\t%s\tARTICLE RETRIEVED:%s'%(dtFormat(dt.today())[1],artBib))
    return article

if __name__ == '__main__':

    Ez.email = 'liuxu@email.missouri.edu'
    output_file = ''.join(dtFormat(dt.today())[0].split(',')[0].split('-')) + ''.join(dtFormat(dt.today())[1].split(':'))
    logupdate()
    update_authorList(article = 'init', filename = output_file)
    
    #parse user input
    if len(sys.argv) == 1:
        user_input = take_terms()
    else:
        user_input = ' '.join(sys.argv[1:])
    
    search_term = term_parse(user_input)
    search_terms = dic_split(search_term)
    print ('Total searches:',len(search_terms))

    result_raw = list()
    for term in search_terms:
        result_raw += (get_id(term))
    ids = dRemove(result_raw)

    print ('Total retrieved:',len(ids))
    if len(ids) > 0:
        articles = get_article(ids)
        for article in articles:
            artInfo = article_parse(article)
            update_authorList(article = artInfo, filename = output_file)
            update_search_result(article = artInfo, filename = output_file)


    