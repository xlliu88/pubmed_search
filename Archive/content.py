#!/usr/bin/python
#Jan 16,2016
#Xunliang

import re
import urllib2
import lxml.html
from lxml import etree
#from lxml.html import parse
from io import StringIO, BytesIO

#artURL_list=list()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
homeURL = 'http://www.cell.com'
artID = 'S0092-8674(15)01574-3'
artURL = homeURL + '/cell/fulltext/' + artID    
print artURL
art_source = opener.open(artURL).read()
#doc = lxml.html.fromstring(art_source) #doc is an instance
doc = etree.HTML(art_source)

file = open('content.txt','wb')
fulltext = ''
con = doc.xpath('//*[@id="artTabContent"]/div[3]/div[2]/div')
print con
for content in con:
    print content
    for des in content.iterdescendants():
        if des.get('id') and ('sec' in des.get('id')):
            print 'destag',des.tag
            para = des.xpath('./*[@class="content"]/section/div/p')
            for ppp in para:
                print 'ppp:',ppp
                print 'ppptag',ppp.tag
                print 'ppptext:', u''.join([t for t in ppp.itertext()]).encode('utf-8')
            # title = '\n'.join(des.xpath('//*[@class="content"]/*/p/text()'))
            # title = u'\r\n'.join([ti for ti in des.itertext()]).encode('utf-8')
            # #print 'section %s extracted' %des.get('id')
            # fulltext = '\r\n'.join([fulltext, title])
            # #print "paragraph %s: %s" % (des.tag, fulltext)
            # raw_input("=============")
            # for subdes in des.iterdescendants():
               # # print subdes.tag
                # if subdes.tag and ('p' in subdes.tag):
                    # text = u'\r\n'.join([t for t in subdes.itertext()]).encode('utf-8')
                    # fulltext = '\r\n'.join([fulltext, text])
                   # # print 'paragraph %s extrated.' % subdes.tag

#print content.iterdescendants()
#print "iterator",content.getiterator()
#print dir(content.getiterator())
#text = u''.join([t for t in content.itertext()]).encode('utf-8')
#text = re.sub('\d+?:.*?;','',text)
print '---------output of text iterate:------------'
#print text
file.write(fulltext)
raw_input('=========end of text iterate output===============')
"""
#sections = con[0].getchildren()
fulltext = list()
for section in sections:

    need to loop into subsections to find text

    id = section.get('id')
    r = doc.xpath('//*[@id="%s"]/div/*/text()' % id)
    if len(r) > 0:
        text = ''.join(r) + '\n'
        print "this is %s :\n" % id
        print text
    else:
        subsections = section.getchildren()
        print "section %s has %d subsections" % (id, len(subsections))
        print subsections
        for sub in subsections:
            print dir(sub)
            tree = sub.getroottree()
            print "method for tree"
            print dir(tree)
            raw_input("read in subsecs")
   # print text
    fulltext.append(text)
    #raw_input(id)
"""
    
"""
#//*[@id="artTabContent"]/div[3]/div[2]/div    
//*[@id="sec2"]/div
//*[@id="sec2.1"]/div/p[2]/text()[1]
#//*[@id="sec1"]
//*[@id="sec2.1"]/div/p[1]
    # print dir(content)
    # print content
    # print content.values()
    # print dir(content)
    # print content.getchildren()
    # print content.getnext()
    # print 'scendants:',content.iterdescendants()
    # print dir(content.iterdescendants())
for sec in range(1,4):
    for p in range(1,4):
        try:
            r = doc.xpath('//*[@id="sec%d"]/div/p[%d]' % (sec,p))#print lxml.html.tostring(tree) #put tree to string
            # print r[0]
            # print dir(r[0])
            print sec,p
            print r[0].text
            print r[0].next
            print r[0].extend
            # print r[0].values
            # print r[0].xpath
        except: break






"""

#art_source = open('S0092-8674(15)01574-3.txt','r').read()
#art_content = re.findall('begin.*?</style>', art_source)
# print art_content
# artcont = open('article_cotent.txt','wb')
# for para in art_content:
    # print para
    # #raw_input('div printout')
    # para = re.sub('<.*?>','',para)
    # para = re.sub('<span>.*?</span>','',para)
    # artcont.write(para)
    # artcont.write('\r\n')