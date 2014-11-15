#!/usr/bin/env python
# coding=utf8
# Author: Archer Reilly
# File: app.py
# Date: 07/Dec/2014
# Desc: main flask file
#
# Produced By CSRGXTU
import sys
# from os import getcwd
from os.path import dirname

sys.path.insert(0, dirname(__file__) + '/lib')
print "Debug: " + dirname(__file__)
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
from GoogleSearchResultParser import GoogleSearchResultParser
# from flask import Flask, render_template
# from flask import request
# from flask import redirect
# from urllib import quote, unquote

# import urllib2

# import httplib
# import re
# import urllib
# import urlparse
# import json

# from flask import Blueprint, Response, url_for
# from werkzeug.datastructures import Headers
# from werkzeug.exceptions import NotFound

app = Flask(__name__)
app.debug = True

# / or /index
# the home page of the gps search
@app.route("/")
@app.route("/index")
def index():
  return render_template('web-search-index.html', jsonData={})

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
    # print jsonData
    jsonData['q'] = request.args.get('q', '')
    jsonData['start'] = start
    return render_template('web-search-result.html', jsonData=jsonData)

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

# /jsf
# just for fun gags
# play videos
@app.route("/jsf")
def jsf():
  return render_template('justforfun.html')

@app.route('/about')
def about():
  return render_template('about.html', jsonData={})

@app.errorhandler(404)
def notFound(error):
  return render_template('notFound.html')

@app.errorhandler(500)
def notImplemented(error):
    return render_template('error.html')

@app.route('/proxy')
def proxy():
  q = unicode(request.args.get('q', '')).encode('utf8')
  content = utilities.proxy(q, request.headers['Accept'])
  if content == None:
    return None
  else:
    return content

""" here define proxy functionality """
proxy = Blueprint('proxy', __name__)

# Filters.
# HTML_REGEX = re.compile(r'((?:src|action|href)=["\'])/')
# JQUERY_REGEX = re.compile(r'(\$\.(?:get|post)\(["\'])/')
# JS_LOCATION_REGEX = re.compile(r'((?:window|document)\.location.*=.*["\'])/')
# CSS_REGEX = re.compile(r'(url\(["\']?)/')
HTML_REGEX = compile(r'((?:src|action|href)=["\'])/')
JQUERY_REGEX = compile(r'(\$\.(?:get|post)\(["\'])/')
JS_LOCATION_REGEX = compile(r'((?:window|document)\.location.*=.*["\'])/')
CSS_REGEX = compile(r'(url\(["\']?)/')

REGEXES = [HTML_REGEX, JQUERY_REGEX, JS_LOCATION_REGEX, CSS_REGEX]

def iterform(multidict):
    for key in multidict.keys():
        for value in multidict.getlist(key):
            yield (key.encode("utf8"), value.encode("utf8"))

def parse_host_port(h):
    """Parses strings in the form host[:port]"""
    host_port = h.split(":", 1)
    if len(host_port) == 1:
        return (h, 80)
    else:
        host_port[1] = int(host_port[1])
        return host_port


# For RESTful Service
@proxy.route('/p/<host>/', methods=["GET", "POST", "PUT", "DELETE"])
@proxy.route('/p/<host>/<path:file>', methods=["GET", "POST", "PUT", "DELETE"])
def proxy_request(host, file=""):
    hostname, port = parse_host_port(host)

    print "H: '%s' P: %d" % (hostname, port)
    print "F: '%s'" % (file)
    # Whitelist a few headers to pass on
    request_headers = {}
    for h in ["Cookie", "Referer", "X-Csrf-Token"]:
        if h in request.headers:
            request_headers[h] = request.headers[h]

    if request.query_string:
        path = "/%s?%s" % (file, request.query_string)
    else:
        path = "/" + file

    if request.method == "POST" or request.method == "PUT":
        form_data = list(iterform(request.form))
        # form_data = urllib.urlencode(form_data)
        form_data = urlencode(form_data)
        request_headers["Content-Length"] = len(form_data)
    else:
        form_data = None

    # print "Debug: I am here"
    # print "Debug: host" + hostname
    # print "Debug: path " + path
    # conn = httplib.HTTPConnection("127.0.0.1", 8087)
    conn = HTTPConnection("127.0.0.1", 8087)
    # conn = httplib.HTTPConnection(hostname, port)
    conn.request(request.method, 'http://' + host + path, body=form_data, headers=request_headers)
    resp = conn.getresponse()
    # print "Debug: request"

    # Clean up response headers for forwarding
    d = {}
    response_headers = Headers()
    for key, value in resp.getheaders():
        print "HEADER: '%s':'%s'" % (key, value)
        d[key.lower()] = value
        if key in ["content-length", "connection", "content-type"]:
            continue

        if key == "set-cookie":
            cookies = value.split(",")
            [response_headers.add(key, c) for c in cookies]
        else:
            response_headers.add(key, value)

    # If this is a redirect, munge the Location URL
    if "location" in response_headers:
        redirect = response_headers["location"]
        # parsed = urlparse.urlparse(request.url)
        parsed = urlparse(request.url)
        # redirect_parsed = urlparse.urlparse(redirect)
        redirect_parsed = urlparse(redirect)

        redirect_host = redirect_parsed.netloc
        if not redirect_host:
            redirect_host = "%s:%d" % (hostname, port)

        redirect_path = redirect_parsed.path
        if redirect_parsed.query:
            redirect_path += "?" + redirect_parsed.query

        munged_path = url_for(".proxy_request",
                              host=redirect_host,
                              file=redirect_path[1:])

        url = "%s://%s%s" % (parsed.scheme, parsed.netloc, munged_path)
        response_headers["location"] = url

    # Rewrite URLs in the content to point to our URL schemt.method == " instead.
    # Ugly, but seems to mostly work.
    root = url_for(".proxy_request", host=host)
    contents = resp.read()

    # Restructing Contents.
    # print "Debug content-type: "
    # print d
    """
    if d["content-type"].find("application/json") >= 0:
        # JSON format conentens will be modified here.
        jc = json.loads(contents)
        if jc.has_key("nodes"):

            del jc["nodes"]
        contents = json.dumps(jc)

    else:
        # Generic HTTP.
        for regex in REGEXES:
           contents = regex.sub(r'\1%s' % root, contents)
    """
    for regex in REGEXES:
        contents = regex.sub(r'\1%s' % root, contents)
    
    flask_response = Response(response=contents,
                              status=resp.status,
                              headers=response_headers,
                              content_type=resp.getheader('content-type'))
    return flask_response


app.register_blueprint(proxy)
""" proxy functionality end """

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=80)
