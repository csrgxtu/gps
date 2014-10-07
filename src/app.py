from flask import Flask, render_template
from flask import request
from flask import redirect
from urllib import quote, unquote
from datetime import datetime
from Download import *
from checkip import *

app = Flask(__name__)
#app.debug = True

# loadBestIP
# load the best IP host from ./static/top.txt
#
# @param filePath
# @return IP
def loadBestIP(filePath):
  with open(filePath, "r") as myFile:
    return myFile.readline().rstrip("\n")

#API_HOST = '64.15.119.167'
API_HOST = loadBestIP('/home/archer/Documents/gps/src/static/top.txt')

@app.route("/")
@app.route("/index")
def index():
  return render_template('index.html')

@app.route("/search")
def search():
  q = quote(unicode(request.args.get('q', '')).encode('utf8'))
  print "Debug: ", q
  if q == "":
    return redirect("/")
  start = request.args.get('start', '')
  log()
  return replacer(queryGoogle(q, start))

@app.route("/cron")
def cron():
  list_ping()
  return str(datetime.now())

@app.route("/url")
def url():
  q = quote(unicode(request.args.get('q', '')).encode('utf8'))
  return redirect(unquote(q), 302)


def queryGoogle(q, start):
  GOOGLE_API = 'http://' + API_HOST + '/search?q='
  dobj = Download(GOOGLE_API + q + '&start=' + start)
  if (dobj.doRequest()):
   return "Cant get content"
  else:
    return dobj.getSOURCE()

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

  return html

def log():
  timeStamp = str(datetime.utcnow())
  clientIP = str(request.remote_addr)
  userAgent = str(request.headers.get('User-Agent'))
  #keyWord = str(quote(unicode(request.args.get('q', '')).encode('utf8')))
  keyWord = unicode(request.args.get('q', '')).encode('utf8')
  csvStr = timeStamp + "," + clientIP + "," + userAgent + "," + keyWord + "\n"
  with open("./static/log.txt", "a") as myFile:
    myFile.write(csvStr)


if __name__ == "__main__":
  app.run(host='0.0.0.0', port=80)
