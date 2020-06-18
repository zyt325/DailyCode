import os
import sys
import tornado.ioloop
import tornado.httpserver
from tornado.options import parse_command_line, options

sys.path.append(os.path.dirname(__file__))
import config
from application import Application

if __name__ == "__main__":
    app = Application()
    httpServer = tornado.httpserver.HTTPServer(app)
    httpServer.bind(port=config.options["port"], address=config.options["host"])
    httpServer.start(num_processes=config.options["processes"])
    # httpServer.start(1)  # 单进程没有问题，多进程异常(需要指定autoreload=False)
    tornado.ioloop.IOLoop.current().start()
