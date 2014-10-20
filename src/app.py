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

app = Flask(__name__)
app.debug = True

@app.route("/")
@app.route("/index")
def index():
  return render_template('index.html')

@app.route("/search")
def search():
  q = quote(unicode(request.args.get('q', '')).encode('utf8'))
  if q == "":
    return redirect("/")
  start = request.args.get('start', '')
  if start:
    pass
  else:
    start = str(0)
  print "Debug: " + start
  utilities.log(str(request.remote_addr), str(request.headers.get('User-Agent')), request.args.get('q', ''))
  html = utilities.queryGoogle(q, start)
  if html == None:
    return render_template('error.html')
  else:
    #return utilities.replacer(html)
    """
    g = GoogleSearchResultParser(html)
    jsonData = g.getJson()
    print "what is going on"
    print jsonData
    """
    g = GoogleSearchResultParser(html)
    # print g.getJson()
    jsonData = g.getJson()
    jsonData['q'] = request.args.get('q', '')
    jsonData['start'] = start
    return render_template('result.html', jsonData=jsonData)

@app.route("/url")
def url():
  q = quote(unicode(request.args.get('q', '')).encode('utf8'))
  return redirect(unquote(q), 302)

@app.errorhandler(404)
def notFound(error):
  return render_template('notFound.html')

@app.errorhandler(500)
def notImplemented(error):
    return render_template('error.html')

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=80)