#!/usr/bin/env python
# coding = utf8
# Author: Archer Reilly
# Date: 19/Oct/2014
# File: GoogleSearchResultParser.py
# Desc: this class is used to parse the Google search result,
# get the json representation of the search result.
# {
#   'relatedKeyWords': {
#     0: 'python beautiful',
#     1: 'beautiful soup tut',
#     ...
#   },
#   'resultStats': 'About 256,000 results',
#   'results': [
#     {
#       'title': 'Beautiful Soup: We called him ..',
#       'unescapedUrl': '',
#       'escapedUrl': '',
#       'content': ''
#     },
#     {
#       'title': 'Beautiful Soup: We called him ..',
#       'unescapedUrl': '',
#       'escapedUrl': '',
#       'content': ''
#     },
#     ...
#   ]
# }
#
# Produced By CSRGXTU
from bs4 import BeautifulSoup
from json import dumps

class GoogleSearchResultParser(object):
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
    self.resultSets = self.soup.find_all("li", class_="g")
  
  """
  def getResultSets(self):
    self.resultSets = self.soup.find_all("li", class_="g")
  """

  def getTitle(self, item):
    return item.find("h3", class_="r").find("a").get_text()

  def getUnescapedUrl(self, item):
    return item.find("h3", class_="r").find("a")["href"]

  def getEscapedUrl(self, item):
    print item
    return item.find("div", class_="s").find("cite").get_text()

  def getContent(self, item):
    return item.find("div", class_="s").find("span", class_="st").get_text()
  
  def getResultStats(self):
    return unicode(self.soup.select("#resultStats")[0].get_text()).encode('utf8')

  def getRelatedKeyWords(self):
    tmpDict = {}
    tags = self.soup.find_all("p", class_="_Bmc")
    i = 0
    for item in tags:
      tmpDict[i] = unicode(item.find("a").get_text()).encode('utf8')
      i = i + 1
    return tmpDict

  def getJson(self):
    tmpLst = []
    for item in self.resultSets:
      # some search result may contain video and image results, so
      # the upper parser wont work on it
      try:
        title = unicode(self.getTitle(item)).encode('utf8')
        unescapedUrl = unicode(self.getUnescapedUrl(item)).encode('utf8')
        escapedUrl = unicode(self.getEscapedUrl(item)).encode('utf8')
        content = unicode(self.getContent(item)).encode('utf8')
        tmpDict = {'title': title, 'unescapedUrl': unescapedUrl, 'escapedUrl': escapedUrl, 'content': content}
        tmpLst.append(tmpDict)
      except AttributeError:
        continue
    self.jsonData['results'] = tmpLst
    self.jsonData['resultStats'] = self.getResultStats()
    self.jsonData['relatedKeyWords'] = self.getRelatedKeyWords()
    return self.jsonData
