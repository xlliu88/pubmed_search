#!/usr/bin/python3
#to get artical information 
#Xunliang Liu
#March 10, 2016

import re
import os
import sys
from Bio import Entrez as Ez
import itertools as it
from datetime import datetime as dt
from lxml import etree as ET
from lxml.builder import E
#import lxml.builder

def update_search_summary():
    print('#search summary updated')
def authorInfo(authorList):
    '''it cleans up the author information from function artical_parse'''
    '''Add 'author type' into author information. Types: First, Corresponding, Other'''
    '''If there's co-first author, only the first one will be labeled as first author'''
    '''It can label multiple corresponding author, only if the email address is in author information'''
    newauthList = list()
    newauthInfo = dict()
    for au in authorList:
        newauthInfo['LastName'] = au['LastName']
        newauthInfo['ForeName'] = au['ForeName']
        if au['AffiliationInfo']:
            newauthInfo['affi'] = au['AffiliationInfo'][0]['Affiliation']  #if an author has multiple affiliation, only take the first.
        if len(authorList) > 1:
            if authorList.index(au) == 0:
                newauthInfo['type'] = 'First'
            elif (authorList.index(au) == len(authorList)-1) or ('@' in newauthInfo['affi']):
                newauthInfo['type'] = 'Corresponding'
            else:
                newauthInfo['type'] = 'other'
        else:
            newauthInfo['type'] = 'Corresponding'
        newauthList.append(dict(newauthInfo))
    return newauthList
def update_authorList(article = ''):
    '''write author information into a csv file'''
    '''takes a list of dictionaries as argument'''
    if article == '':
        file_title = '%s,%s,%s,%s,%s,%s,%s'%('Name','Author Type', 'Article Type',
                                            'Journal','Year','Article title',
                                            'Author affiliation')
        with open('./results/authors.csv','wt') as authors:
            authors.write(file_title)
            authors.write('\r\n')
    else:
        with open('./results/authors.csv','at') as authors:
            for au in article['authors']:
                au['affi'] = re.sub(',',';',au['affi'])
                auInfo = '%s %s,%s,%s,%s,%s,%s,%s'%(au['ForeName'],au['LastName'],
                                                au['type'],article['type'],
                                                article['jour'],article['year'],article['title'],
                                                au['affi'])  
                authors.write(auInfo)
                authors.write('\r\n')

def update_search_result(article):
    '''takes the result from article_parse and write it into html file'''
    
    from lxml import etree as ET
    from lxml.builder import E

    jourInfo = '%s(%s).%s(%s):%s. %s'%(article['jour'],article['year'],
                                        article['vol'],article['issue'],article['pages'],
                                        article['doi'])
    
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
    with open('./results/output.html','ab') as output:
        output.write(html)

def logupdate():
    print('#log updated')

def get_article(pubmed_id):
    ''' this function takes pubmed_id list and retrieves artical information from PubMed.'''
    Ez.email = 'xunliangliu@email.arizona.edu'
    handle = Ez.efetch(db = 'pubmed', id = pubmed_id, retmode = 'xml')
    records = Ez.parse(handle)   #records is a generator.
    return records
    
def article_parse(record):
    article = dict()
    journal_home = {'Nature':'http://www.nature.com/journal', 
                    'Science':'http://science.sciencemag.org/content', 
                    'Cell':'http://www.cell.com/cell/full',
                    'PlantCell':'http://www.plantcell.org/content',
                    'pubmed':'http://www.ncbi.nlm.nih.gov/pubmed'}
    article['title'] = record['MedlineCitation']['Article']['ArticleTitle']   #return a string
    article['abst'] = ''.join(record['MedlineCitation']['Article']['Abstract']['AbstractText']) #return a string
    article['authors'] = record['MedlineCitation']['Article']['AuthorList'] #return a list of dictionaries
    
    article['pmid'] = record['MedlineCitation']['PMID'].title()
    article['jour'] = record['MedlineCitation']['Article']['Journal']['Title']
    date_created = record['MedlineCitation']['DateCreated']   #return a dictionary e.g.{'year':'2001','month':'03','day':'03'}
    article['year'] = record['MedlineCitation']['DateCreated']['Year']
    article['month'] = record['MedlineCitation']['DateCreated']['Month']
    article['day'] = record['MedlineCitation']['DateCreated']['Day']
    article['vol'] = record['MedlineCitation']['Article']['Journal']['JournalIssue']['Volume']
    article['issue'] = record['MedlineCitation']['Article']['Journal']['JournalIssue']['Issue']
    article['pages'] = record['MedlineCitation']['Article']['Pagination']['MedlinePgn']
    
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
       article['url'] = '%s/v%s/n%s/%s.html'% (journal_home['Nature'],article['vol'],article['issue'],article['pii'])
    elif article['jour'].lower() == 'science':
        article['url'] = '%s/%s/%s/%s.full'% (journal_home['Science'],article['vol'],article['issue'],article['pages'].split('-')[0])
    elif article['jour'].lower() == 'cell':
        article['url'] = '%s/%s.html'%(journal_home['Cell'],article['pii'])
    elif article['jour'].lower() == 'the plant cell':
        article['url'] = '%s/%s/%s/%s.full'% (journal_home['PlantCell'],article['vol'],article['issue'],article['pages'].split('-')[0])
    else:
        article['url'] = '%s/%s'%(journal_home['pubmed'], article['PMID'])
    
    article['authors'] = authorInfo(article['authors'])
    return article
        
if __name__ == '__main__':
    update_authorList()
    id = ['20010603','26578700','26410302']
    records = get_article(id)
    for record in records:
        artInfo = article_parse(record)
        update_authorList(artInfo)
        update_search_summary()
        update_search_result(artInfo)
        logupdate()    
