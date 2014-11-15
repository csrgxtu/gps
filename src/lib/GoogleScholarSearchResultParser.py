#!/usr/bin/env python
# coding = utf8
# Author: Archer Reilly
# Date: 26/Oct/2014
# File: GoogleScholarSearchResultParser.py
# Desc: a parser for google search result. well, translate.cn still works
# and I found if you configure your host file with a useable Google IP, 
# then you can use translate.com, I mean this only in China, other
# countries should not need host config. uh, whatever, just write this
# parser here.
#
# {
#   'resultStats': '256000',
#   'results': [
#     {
#       'mime': 'pdf',
#       'title': 'maximum entropy approach to bregman co-clustering and matrix approximation',
#       'unescapedUrl': 'http://www.researchgate.net/publication/2936920_A_Generalized_Maximum_Entropy_Approach_to_Bregman_Co-clustering_and_Matrix_Approximation/file/50463521fe3b57326b.pdf',
#       'escapedUrl': 'http://dl.acm.org/citation.cfm?id=1014111',
#       'content': 'Abstract Co-clustering is a powerful data mining technique with varied applications such',
#       'authors': [
#         {'name': ' J Ghosh', 'citationLink': 'http://scholar.google.com/citations?user=Xnk4W5cAAAAJ&hl=en&oi=sra'},
#         ...
#       ],
#       'year': '2004',
#       'from': 'dl.acm.org',
#       'meeting': 'The Mathematical',
#       'cited': {'quantity': '303', 'citeLink': 'http://scholar.google.com/scholar?cites=7649748373716329368&as_sdt=2005&sciodt=0,5&hl=en'},
#       'related': 'http://scholar.google.com/scholar?q=related:mON7pJ1dKWoJ:scholar.google.com/&hl=en&as_sdt=0,5',
#       'versions': {'quantity': '20', 'versionLink': 'http://scholar.google.com/scholar?cluster=7649748373716329368&hl=en&as_sdt=0,5'},
#     },
#     ...
#   ]
# }
#
# Produced By CSRGXTU
from bs4 import BeautifulSoup
from os.path import splitext

class GoogleScholarSearchResultParser(object):
  # hold the original html source code
  html = None

  # soup object
  soup = None

  # result sets
  resultSets = None

  # json data
  jsonData = {}

  def __init__(self, html):
    self.html = html
    self.soup = BeautifulSoup(self.html)
    self.resultSets = self.soup.find_all("div", class_="gs_r")

  def getResultStats(self):
    statsStr = self.soup.select("#gs_ab_md")[0].get_text()
    start = statsStr.find("out")
    end = statsStr.find("res")
    return statsStr[start:end][4:-1].replace(",", "")
    # pass

  def getMime(self, item):
    tmpItem = item.find('div', class_='gs_md_wp gs_ttss')
    if tmpItem is None:
      # default to html
      return 'HTML'
    else:
      return splitext(tmpItem.find('a')['href'])[1][1:]
    # mimeUrl = item.find('div', class_='gs_md_wp gs_ttss').find('a')['href']
    # return splitext(mimeUrl)[1][1:]
    # pass

  def getTitle(self, item):
    return item.find('h3', class_='gs_rt').get_text()
    # pass

  def getUnescapedUrl(self, item):
    tmpItem = item.find('div', class_='gs_md_wp gs_ttss')
    if tmpItem is None:
      return None
    else:
      return tmpItem.find('a')['href']
    # return item.find('div', class_='gs_md_wp gs_ttss').find('a')['href']
    # pass

  def getEscapedUrl(self, item):
    return item.find('h3', class_='gs_rt').find('a')['href']
    # pass

  def getContent(self, item):
    return item.find('div', class_='gs_rs').get_text()
    # pass

  def getAuthors(self, item):
    res = []
    tmpres = {}
    tmpnames = []
    names = item.find('div', class_='gs_a').get_text().split('-')[0].split(', ')
    for i in item.find('div', class_='gs_a').find_all('a'):
      if i.get_text() in names:
        tmpres['name'] = i.get_text
        tmpres['citationLink'] = i['href']
        res.append(tmpres)
        tmpnames.append(i.get_text())

    for name in names:
      if name in tmpnames:
        continue
      else:
        tmpres['name'] = name
        tmpres['citationLink'] = None
        res.append(tmpres)

    return res


  def getYear(self, item):
    return item.find('div', class_='gs_a').get_text().split(' - ')[1].split(', ')[-1].rstrip()
    # pass

  def getFrom(self, item):
    return item.find('div', class_='gs_a').get_text().split('-')[2].replace(' ', '')
    # pass

  def getMeeting(self, item):
    return item.find('div', class_='gs_a').get_text().split('-')[1].split(', ')[0].lstrip()

  def getCited(self, item):
    res = {}
    res['quantity'] = item.find('div', class_='gs_ri').find('div', class_='gs_fl').find_all('a')[0].get_text().replace('Cited by ', '')
    res['citeLink'] = item.find('div', class_='gs_ri').find('div', class_='gs_fl').find_all('a')[0]['href']
    return res
    # pass

  def getRelated(self, item):
    return item.find('div', class_='gs_ri').find('div', class_='gs_fl').find_all('a')[1]['href']
    # pass

  def getVersions(self, item):
    return item.find('div', class_='gs_ri').find('div', class_='gs_fl').find_all('a')[2]['href']
    # pass

  def getJson(self):
    tmpLst = []
    self.jsonData['resultStats'] = self.getResultStats()
    # self.jsonData['results'] = []
    for item in self.resultSets:
      # print "Title: " + self.getTitle(item)
      tmpDict = {}
      tmpDict['mime'] = self.getMime(item)
      tmpDict['title'] = self.getTitle(item)
      tmpDict['unescapedUrl'] = self.getUnescapedUrl(item)
      tmpDict['escapedUrl'] = self.getEscapedUrl(item)
      tmpDict['content'] = self.getContent(item)
      tmpDict['authors'] = self.getAuthors(item)
      tmpDict['year'] = self.getYear(item)
      tmpDict['From'] = self.getFrom(item)
      tmpDict['meeting'] = self.getMeeting(item)
      tmpDict['cited'] = self.getCited(item)
      tmpDict['related'] = self.getRelated(item)
      tmpDict['versions'] = self.getVersions(item)
      
      tmpLst.append(tmpDict)

    self.jsonData['results'] = tmpLst
    return  self.jsonData
    # pass