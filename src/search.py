#!/usr/bin/env python
# coding=utf8
# Author: Archer Reilly
# File: app.py
# Date: 07/Dec/2014
# Desc: main flask file
#
# Produced By CSRGXTU
from flask import Flask, render_template

app = Flask(__name__)
app.debug = True

# / or /index
# the home page of the gps search
@app.route("/")
@app.route("/index")
def index():
  return render_template('web-search-index.html', jsonData={})

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8080)
