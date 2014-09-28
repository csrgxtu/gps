import sae
from string import Template

# readFile
# read file from plain text
#
# @param filePath
# @return data string
def readFile(filePath):
  with open(filePath, "r") as myFile:
    return myFile.read()

# index
# main page
def index(environ, start_response):
  data = readFile("./static/index.html")
  status = '200 OK'
  headers = [('Content-type', 'text/html')]
  start_response(status, headers)
  #yield data
  yield "<h3>" + environ['QUERY_STRING'] + "</h3>"

# search
# search and result page
def search(environ, start_response):
  #data = readFile("./static/index.html")
  status = '200 OK'
  headers = [('Content-type', 'text/html')]
  start_response(status, headers)
  yield '<center><h3>what</h3></center>'

application = sae.create_wsgi_app(index)
#application = index
