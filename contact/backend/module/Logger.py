import logging
import logging.handlers
import tempfile


class Logger:
    def __init__(self, name='itd', level='debug', hander='terminal'):
        self.name = name
        self.level = self.Level(level)
        Hander = {'terminal': self.Hander_terminal(),
                  'email': self.Hander_email(), 'file': self.Hander_file()}
        self.logger = self.Logger_create(Hander[hander])

    def Level(self, name):
        levels = {'DEBUG': logging.DEBUG, 'INFO': logging.INFO,
                  'WARNING': logging.WARNING, 'ERROR': logging.ERROR, 'CRITICAL': logging.CRITICAL}
        return levels[str(name).upper()]

    def Logger_create(self, hander):
        logger = logging.getLogger(self.name)
        logger.setLevel(self.level)
        logger.addHandler(hander)
        return logger

    def Hander_file(self):
        hander_f = logging.FileHandler(tempfile.mkstemp(prefix='itd_')[1])
        hander_f.setLevel(self.level)
        hander_f.setFormatter(self.Logger_format())
        return hander_f

    def Hander_email(self, mailhost='smtp.base-fx.com', fromaddr="Logger@base-fx.com", toaddrs="zhangyt@base-fx.com", subject="脚本日志", credentials=('itd_mail', 'Eo8yGcdjy')):
        hander_e = logging.handlers.SMTPHandler(
            mailhost, fromaddr, toaddrs, subject, credentials=None)
        hander_e.setLevel(self.level)
        hander_e.setFormatter(self.Logger_format())
        return hander_e

    def Hander_terminal(self):
        hander_t = logging.StreamHandler()
        hander_t.setLevel(self.level)
        hander_t.setFormatter(self.Logger_format())
        return hander_t

    def Logger_format(self):
        return logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(module)s - %(message)s')
