import tornado.web
import tornado.ioloop
import tornado.template


class TemplateHandler(tornado.web.RequestHandler):
    """主路由处理类"""

    def get(self):
        """对应http的get请求方式"""
        t = tornado.template.Template("<html>{{ myvalue }}</html>")
        self.write(t.generate(myvalue="Template"))


class FileTemplateHandler(tornado.web.RequestHandler):
    """主路由处理类"""

    def get(self):
        """对应http的get请求方式"""
        loader = tornado.template.Loader("./")
        self.write(loader.load('1-2.html').generate(myvalue="fileTemplate"))


if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/", TemplateHandler),
        (r'/file/', FileTemplateHandler),
    ])
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()
