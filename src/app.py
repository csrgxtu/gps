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

app = Flask(__name__)

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
  utilities.log(str(request.remote_addr), str(request.headers.get('User-Agent')), request.args.get('q', ''))
  html = utilities.queryGoogle(q, start)
  if html == None:
    return render_template('error.html')
  else:
    return utilities.replacer(html)

@app.route("/url")
def url():
  q = quote(unicode(request.args.get('q', '')).encode('utf8'))
  return redirect(unquote(q), 302)

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=80)
