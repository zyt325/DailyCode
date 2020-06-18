import tornado.web
import tornado.ioloop
import tornado.httpserver

from tornado.options import define, options, parse_command_line

define("port", default=8000, type=int)
define("host", default="0.0.0.0", type=str)
define('processes',default=5,type=int)


from tornado.web import RequestHandler


class IndexHandler(RequestHandler):
    """主路由处理类"""

    def get(self):
        """对应http的get请求方式"""
        self.write('test')

if __name__ == "__main__":
    print('test')
    tornado.options.options.logging=None
    app = tornado.web.Application([
        (r"/", IndexHandler),
    ])
    parse_command_line()

    # app.listen(port=options.port,address=options.host)

    # httpServer = tornado.httpserver.HTTPServer(app)
    # httpServer.listen(port=options.port, address=options.host)

    httpServer=tornado.httpserver.HTTPServer(app)
    httpServer.bind(port=options.port, address=options.host)
    httpServer.start(num_processes=options.processes)
    tornado.ioloop.IOLoop.current().start()
