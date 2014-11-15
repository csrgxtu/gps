#!/usr/bin/env python
# coding=utf8
# Author: Archer Reilly
# Date: 07/Dec/2014
# File: utilities.py
# Desc: some utilities that will be used in main file
#
# Produced By CSRGXTU
import config
from Download import *
import DownloadHTTPSProxy
from datetime import datetime
from random import choice
from bs4 import BeautifulSoup
from urlparse import urljoin, urlparse

# loadBestIP
# load the best IP host from ./static/top.txt
#
# @param filePath
# @return IP
def loadBestIP(filePath):
  with open(filePath, "r") as myFile:
    return myFile.readline().rstrip("\n")

# loadBestNIP
# load the best N IP host from top.txt
#
# @param filePath
# @param n
# @return IPS
def loadBestNIP(filePath, n):
  IPS = []
  with open(filePath, "r") as myFile:
    for i in range(n):
      IPS.append(myFile.readline().rstrip("\n"))
  
  return IPS

# queryGoogle
# use the IP query the Google
#
# @param q
# @param start
# @return source code of the query or string
def queryGoogle(q, start):
  API_HOST = choice(loadBestNIP(config.TOP_IP_FILE, 20))
  # print "Debug: " + API_HOST
  GOOGLE_API = 'http://' + API_HOST + '/search?q='
  dobj = Download(GOOGLE_API + q + '&start=' + start)
  if (dobj.doRequest()):
   return None
  else:
    return dobj.getSOURCE()

# searchQuery
# use the IP query the Google Search
#
# @param q
# @param start
# @return source code of the query or None
def searchQuery(q, start):
  API_HOST = choice(loadBestNIP(config.TOP_IP_FILE, 20))
  SEARCH_API = 'https://' + API_HOST + '/search?q='
  dobj = Download(SEARCH_API + q + '&start=' + start)
  if (dobj.doRequest()):
    return None
  else:
    return dobj.getSOURCE()

# scholarQuery
# use the IP query the Google scholar
#
# @param q
# @param start
# @return source code of the query string
def scholarQuery(q, start):
  API_HOST = choice(loadBestNIP(config.TOP_IP_FILE, 20))
  SCHOLAR_API = 'http://' + API_HOST + '/scholar?q='
  # dobj = Download(SCHOLAR_API + q + '&start=' + start)
  dobj = Download(SCHOLAR_API + q + '&start=' + start)
  if (dobj.doRequest()):
    return None
  else:
    return dobj.getSOURCE()

# proxy
# use the proxy get the content that cant be get by normal
# request
#
# @param url
# @param httpAcceptStr
# @return content of the query
def proxy(url, httpAcceptStr):
  # urlRoot = urlparse.urlparse(url)
  d = DownloadHTTPSProxy.Download(url)
  if (d.doRequest()):
    return None
  else:
    if 'html' in httpAcceptStr:
      # turn all url in source into abs url
      html = turnToAbsUrl(url, d.getSOURCE())
      # print "Debug turnToAbsUrl: "
      html = addProxyToUrl(html)
      #print "Debug addProxyToUrl:"
      #html2File(html, "./debug.html")
      return html
    else:
      return d.getSOURCE()
    # return d.getSOURCE()

# turnToAbsUrl
# turn all urls in the html page into abs url
#
# @param url the url of the html
# @param html
# @return html
def turnToAbsUrl(url, html):
  soup = BeautifulSoup(html)

  # change href
  for tag in soup.find_all(href=True):
    if isAbsUrl(tag['href']):
      pass
    else:
      # tag['href'] = urlRoot + tag['href']
      tag['href'] = urljoin(url, tag['href'])

  # change src
  for tag in soup.find_all(src=True):
    if isAbsUrl(tag['src']):
      pass
    else:
      # tag['src'] = urlRoot + tag['src']
      tag['src'] = urljoin(url, tag['src'])

  # html2File(html, "./debug.html")
  # print soup.prettify()
  return soup.prettify()

# addProxyToUrl
# add proxy to url
#
# @param html
# @return html
def addProxyToUrl(html):
  soup = BeautifulSoup(html)

  # change href
  for tag in soup.find_all(href=True):
    tag['href'] = "/proxy?q=" + tag['href']

  # change src
  for tag in soup.find_all(src=True):
    tag['src'] = "/proxy?q=" + tag['src']

  return soup.prettify()

# isAbsUrl
# check if url is abs or relative
#
# @param url
# @return boolean
def isAbsUrl(url):
  return bool(urlparse(url).netloc)

# replacer
# replace some text in the source code of the query result, or
# page won't load correctly in browser
#
# @param html
# @return html
def replacer(html):
  # replace favicon
  html = html.replace('<meta content="/images/google_favicon_128.png" itemprop="image">', '<link rel="shortcut icon" href="./static/favicon.ico" />')

  # replace the logo a link
  html = html.replace('/webhp?hl=en', '/')

  # replace the logo img link
  html = html.replace('/images/nav_logo176.png', 'http://' + API_HOST + '/images/nav_logo176.png')

  # replace the pagination logo img link
  html = html.replace('/images/nav_logo195.png', 'http://' + API_HOST + '/images/nav_logo195.png')

  # replace Google indexed relative link with abs
  #html = html.replace('/url?q=', 'http://' + API_HOST + '/url?q=')

  # replace /xjs/_
  html = html.replace('/xjs/', 'http://' + API_HOST + '/xjs/')
  
  # replace all google.com to csrgxtu.com
  html = html.replace('google.com', 'csrgxtu.com')

  return html

# log
# log the user behaviour, mainly used for research
#
# @param clientIP
# @param userAgent
# @param keyWord
def log(clientIP, userAgent, keyWord):
  timeStamp = str(datetime.utcnow())
  #clientIP = str(request.remote_addr)
  #userAgent = str(request.headers.get('User-Agent'))
  #keyWord = str(quote(unicode(request.args.get('q', '')).encode('utf8')))
  keyWord = unicode(keyWord).encode('utf8')
  csvStr = timeStamp + "," + clientIP + "," + userAgent + "," + keyWord + "\n"
  with open(config.LOG_FILE, "a") as myFile:
    myFile.write(csvStr)

#API_HOST = loadBestIP(config.TOP_IP_FILE)

# html2File
# save html source 2 file
#
# @param html
# @param outFile
# @return None
def html2File(html, outFile):
  html = unicode(html).encode('utf8')
  with open(outFile, "w") as myFile:
    myFile.write(html)
