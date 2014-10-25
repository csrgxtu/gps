#!/usr/bin/env python
# coding=utf8
# Author: Archer Reilly
# File: app.py
# Date: 07/Dec/2014
# Desc: main flask file
#
# Produced By CSRGXTU
import sys
sys.path.insert(0, '/home/archer/Documents/gps/src/lib')

from flask import Flask, render_template
from flask import request
from flask import redirect
from urllib import quote, unquote
import config
import utilities
from GoogleSearchResultParser import GoogleSearchResultParser

import urllib2

app = Flask(__name__)
app.debug = True

# / or /index
# the home page of the gps search
@app.route("/")
@app.route("/index")
def index():
  return render_template('index.html')

# /search
# accept the keyword and search and return the result
@app.route("/search")
def search():
  # print "Debug Headers /search"
  # print request.headers['Accept']
  q = quote(unicode(request.args.get('q', '')).encode('utf8'))
  if q == "":
    return redirect("/")
  start = request.args.get('start', '')
  if start:
    pass
  else:
    start = str(0)
  utilities.log(str(request.remote_addr), str(request.headers.get('User-Agent')), request.args.get('q', ''))
  html = utilities.queryGoogle(q, start)
  if html == None:
    return render_template('error.html')
  else:
    g = GoogleSearchResultParser(html)
    jsonData = g.getJson()
    jsonData['q'] = request.args.get('q', '')
    jsonData['start'] = start
    return render_template('result.html', jsonData=jsonData)

# /url
# used process the google indexed url, actually, it wont need
# but I cant remove the index encoded characters from Google
# indexed url
@app.route("/url")
def url():
  # print "Debug Headers /url"
  # print request.headers['Accept']
  q = quote(unicode(request.args.get('q', '')).encode('utf8'))
  return redirect(unquote(q), 302)

# proxy
# when encoutered this kind of url, use goagent get the request
# content
@app.route("/proxy")
def proxy():
  q = unicode(request.args.get('q', '')).encode('utf8')
  print "Debug /proxy " + q
  # urlRoot = request.url_root
  # print "Debug urlRoot: " + urlRoot
  content = utilities.proxy(q, request.headers['Accept'])
  if content == None:
    return render_template('error.html')
  else:
    return content

@app.route("/android")
def android():
  proxy_support = urllib2.ProxyHandler({"http":"http://127.0.0.1:8087"})
  opener = urllib2.build_opener(proxy_support)
  urllib2.install_opener(opener)
  html = urllib2.urlopen("https://www.android.com").read()
  return html

@app.errorhandler(404)
def notFound(error):
  return render_template('notFound.html')

@app.errorhandler(500)
def notImplemented(error):
    return render_template('error.html')

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=80)