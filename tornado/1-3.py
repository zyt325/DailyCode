import tornado.web
import tornado.ioloop
import tornado.websocket

from tornado.options import define, options, parse_command_line

define("port", default=8000, type=int)
define("host", default="0.0.0.0", type=str)


class IndexHandler(tornado.web.RequestHandler):
    """主路由处理类"""

    def get(self):
        """对应http的get请求方式"""
        self.render('1-3-websocket.html')


if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/", IndexHandler),
    ])
    parse_command_line()
    app.listen(port=options.port,address=options.host)
    tornado.ioloop.IOLoop.current().start()
