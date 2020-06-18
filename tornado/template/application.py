import tornado.web
import config
from views import index


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", index.IndexHandler),
            (r"/args", index.ArgsHandler, {'username': 'aaa'}),
            (r"/args1/(.*)", index.Args1Handler),
            (r"/json", index.JsonHandler),
        ]
        super(Application, self).__init__(handlers, **config.settings)
