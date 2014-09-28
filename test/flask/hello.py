from flask import Flask
app = Flask(__name__)

@app.route("/")
@app.route("/index")
def hello():
  return "Hello World!"

@app.route("/search")
def search():
  return "search"

if __name__ == "__main__":
  app.run()
