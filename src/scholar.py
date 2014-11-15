#!/usr/bin/env python
# coding=utf8
# Author: Archer Reilly
# File: scholar.py
# Date: 07/Dec/2014
# Desc: main flask file
#
# Produced By CSRGXTU
import sys
# from os import getcwd
from os.path import dirname

sys.path.insert(0, dirname(__file__) + '/lib')
# print "Debug: " + dirname(__file__)
# sys.path.insert(0, '/home/archer/Documents/gps/src/lib')

from flask import Flask, render_template, request, redirect, Blueprint, Response, url_for
from urllib import urlencode, quote, unquote
from werkzeug.datastructures import Headers
from werkzeug.exceptions import NotFound
from urlparse import urlparse
from httplib import HTTPConnection
from re import compile
from json import loads, dumps
import config
import utilities
from GoogleScholarSearchResultParser import GoogleScholarSearchResultParser


app = Flask(__name__)

@app.route('/')
def index():
  return render_template('scholar-search-index.html', jsonData={})

# /scholar
# accept the keyword and search and return the result
@app.route("/scholar")
def scholar():
  q = quote(unicode(request.args.get('q', '')).encode('utf8'))
  if q == "":
    return redirect("/")
  start = request.args.get('start', '')
  if start:
    pass
  else:
    start = str(0)
  utilities.log(str(request.remote_addr), str(request.headers.get('User-Agent')), request.args.get('q', ''))
  html = utilities.scholarQuery(q, start)
  if html == None:
    return render_template('error.html')
  else:
    g = GoogleScholarSearchResultParser(html)
    jsonData = g.getJson()
    jsonData['q'] = request.args.get('q', '')
    jsonData['start'] = start
    # return html
    # return render_template('about.html', jsonData={})
    return render_template('scholar-search-result.html', jsonData=jsonData)

# /url
# used process the google indexed url, actually, it wont need
# but I cant remove the index encoded characters from Google
# indexed url
@app.route("/url")
def url():
  # print "Debug Headers /url"
  # print request.headers['Accept']
  q = quote(unicode(request.args.get('q', '')).encode('utf8'))
  # print "Debug: ", unquote(q)
  if ".android.com" in unquote(q):
    return redirect('/p/' + unquote(q).replace('http://', ''), 302)
  else:
    return redirect(unquote(q), 302)
  # return redirect(unquote(q), 302)

@app.route('/about')
def about():
  return render_template('about.html', jsonData={})

@app.errorhandler(404)
def notFound(error):
  return render_template('notFound.html')

@app.errorhandler(500)
def notImplemented(error):
    return render_template('error.html')



if __name__ == "__main__":
  app.run(host='0.0.0.0', port=80)
