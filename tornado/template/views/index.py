from tornado.web import RequestHandler


class IndexHandler(RequestHandler):
    """主路由处理类"""

    def get(self):
        """对应http的get请求方式"""
        self.write('test')


class ArgsHandler(RequestHandler):
    def initialize(self, username):
        self.username = username

    def get(self, *args, **kwargs):
        self.write(self.username)


class Args1Handler(RequestHandler):
    def get(self, username):
        self.write(username)


class JsonHandler(RequestHandler):
    def get(self, *args, **kwargs):
        test = {
            "name": "test",
            "age": 14
        }
        import json
        jsonStr = json.dumps(test)
        self.write(jsonStr)
