# coding=UTF-8

# python native module
import argparse
import binascii
import json
import os.path
from datetime import datetime
import time
import sys
from  tornado.escape import json_decode
from  tornado.escape import json_encode

# tornado module
import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado import gen

#mongodb module
import pymongo
from pymongo import MongoClient

sys.path.append("../src")

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
            (r"/schedule", ScheduleHandler),
        ]

        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            admin_path=os.path.join(os.path.dirname(__file__), "admin"),
            cookie_secret = "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
            xsrf_cookies= False,
            #login_url = '/auth/admin/login',
        )
        super(Application, self).__init__(handlers, **settings)

class BaseHandler(tornado.web.RequestHandler):
    pass

class IndexHandler(tornado.web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        super(IndexHandler, self).__init__(application, request, **kwargs)

    def get(self):
        self.render("index.html")

    def post(self):
        pass

class ScheduleHandler(tornado.web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        super(ScheduleHandler, self).__init__(application, request, **kwargs)

    def get(self):
        self.write("hello")

    def post(self):
        json_obj = json_decode(self.request.body)
        print('Post data received')

        for key in list(json_obj.keys()):
            print('key: %s , value: %s' % (key, json_obj[key]))

        # new dictionary
        response_to_send = {}
        response_to_send['newkey'] = 'hello'
        #print('Response to return')
        self.write(json.dumps(response_to_send))

if __name__ == '__main__':
    main()