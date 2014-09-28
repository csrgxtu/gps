import sae

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
def search_app(environ, start_response):
  #data = readFile("./static/index.html")
  status = '200 OK'
  headers = [('Content-type', 'text/html')]
  start_response(status, headers)
  #yield environ['wsgi.input'].read()
  yield "what"

application = sae.create_wsgi_app(search_app)
#application = index
