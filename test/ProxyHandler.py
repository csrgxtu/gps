import os
import urlparse

import requests

import tornado.ioloop
import tornado.web
from tornado import template

ROOT = os.path.dirname(os.path.abspath(__file__))
path = lambda *a: os.path.join(ROOT, *a)

loader = template.Loader(path(ROOT, 'templates'))


class ProxyHandler(tornado.web.RequestHandler):
    def get(self, slug):
        if slug.startswith("http://") or slug.startswith("https://"):
            if self.get_argument("start", None) == "true":
                parsed = urlparse.urlparse(slug)
                self.set_cookie("scheme", value=parsed.scheme)
                self.set_cookie("netloc", value=parsed.netloc)
                self.set_cookie("urlpath", value=parsed.path)
            #external resource
            else:
                response = requests.get(slug)
                headers = response.headers
                if 'content-type' in headers:
                    self.set_header('Content-type', headers['content-type'])
                if 'length' in headers:
                    self.set_header('length', headers['length'])
                for block in response.iter_content(1024):
                    self.write(block)
                self.finish()
                return
        else:
            slug = "{scheme}://{netloc}/{original_slug}".format(
                scheme=self.get_cookie('scheme'),
                netloc=self.get_cookie('netloc'),
                original_slug=slug,
            )
            print self.get_cookie('scheme')
            print self.get_cookie('netloc')
            print self.get_cookie('urlpath')
            print slug

            """
            #absolute
            if slug.startswith('/'):
                slug = "{scheme}://{netloc}{original_slug}".format(
                    scheme=self.get_cookie('scheme'),
                    netloc=self.get_cookie('netloc'),
                    original_slug=slug,
                )
            #relative
            else:
                slug = "{scheme}://{netloc}{path}{original_slug}".format(
                    scheme=self.get_cookie('scheme'),
                    netloc=self.get_cookie('netloc'),
                    path=self.get_cookie('urlpath'),
                    original_slug=slug,
                )
            """
        response = requests.get(slug)
        #get the headers
        headers = response.headers
        #get doctype
        doctype = None
        if '<!doctype' in response.content.lower()[:9]:
            doctype = response.content[:response.content.find('>')+1]
        if 'content-type' in headers:
           self.set_header('Content-type', headers['content-type'])
        if 'length' in headers:
            self.set_header('length', headers['length'])
        self.write(response.content)


application = tornado.web.Application([
    (r"/(.+)", ProxyHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()