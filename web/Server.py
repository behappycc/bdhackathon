# coding=UTF-8

# python native module
import argparse
import binascii
import json
import os.path
from datetime import datetime
import time
import sys

# tornado module
import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado import gen

#mongodb module
import pymongo
from pymongo import MongoClient

DB_IP = "localhost"
DB_PORT = 27017
DB_NAME = 'travel'

def main():
    parser = argparse.ArgumentParser(description='travel server')
    parser.add_argument('-p', type=int, help='listening port for travel server')
    args = parser.parse_args()
    port = args.p

    time_stamp = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    print("Server started at", time_stamp, 'using port', port)

    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(port)

    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        tornado.ioloop.IOLoop.instance().stop()

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", IndexHandler),
            (r"/index", IndexHandler),
        ]

        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            admin_path=os.path.join(os.path.dirname(__file__), "admin"),
            cookie_secret = "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
            xsrf_cookies= True,
            #login_url = '/auth/admin/login',
        )
        super(Application, self).__init__(handlers, **settings)

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("admin")

class IndexHandler(tornado.web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        super(IndexHandler, self).__init__(application, request, **kwargs)

    def get(self):
        self.render("index.html")

    def post(self):
        pass

if __name__ == '__main__':
    main()