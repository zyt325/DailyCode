import logging
import logging.handlers
import tempfile


class Logger:
    def __init__(self, name='itd', level='DEBUG', handler='terminal', handler_file_dir=None):
        self.name = name
        self.level = self.Level(level)
        self.handler_file_dir = handler_file_dir
        self.handler = handler

    def logger(self):
        return self.Logger_create(self.Handler(self.handler))

    def save_log(self, log_level, message):
        logger = self.Logger_create(self.Handler(self.handler))

        logger.log(log_level, message)
        logger.removeHandler(self.Handler(self.handler)())

    def Logger_create(self, handler):
        logger = logging.getLogger(self.name)
        logger.setLevel(self.level)
        if not logger.handlers:
            logger.addHandler(handler())
        return logger

    def Logger_remove(self, handler):
        self.logger.removeHandler(handler)

    def remove(self):
        self.Logger_remove(self.Handler[self.handler])

    def Level(self, name):
        levels = {'DEBUG': logging.DEBUG, 'INFO': logging.INFO,
                  'WARNING': logging.WARNING, 'ERROR': logging.ERROR, 'CRITICAL': logging.CRITICAL}
        return levels[str(name).upper()]

    def Handler(self, type):
        handlers = {'terminal': self.Handler_terminal,
                    'email': self.Handler_email, 'file': self.Handler_file}
        return handlers[type]

    def Handler_file(self):
        handler_f = logging.FileHandler(tempfile.mkstemp(prefix='itd_', dir=self.handler_file_dir)[1])
        handler_f.setLevel(self.level)
        handler_f.setFormatter(self.Logger_format())
        return handler_f

    def Handler_email(self, mailhost='smtp.base-fx.com', fromaddr="Logger@base-fx.com", toaddrs="zhangyt@base-fx.com",
                      subject="脚本日志", credentials=('itd_mail', 'Eo8yGcdjy')):
        handler_e = logging.handlers.SMTPHandler(
            mailhost, fromaddr, toaddrs, subject, credentials=None)
        handler_e.setLevel(self.level)
        handler_e.setFormatter(self.Logger_format())
        return handler_e

    def Handler_terminal(self):
        handler_t = logging.StreamHandler()
        handler_t.setLevel(self.level)
        handler_t.setFormatter(self.Logger_format())
        return handler_t

    def Logger_format(self):
        return logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(module)s - %(message)s')
