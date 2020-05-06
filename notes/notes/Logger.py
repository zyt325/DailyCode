import os
# LOG_PATH = os.path.join('/tmp/', 'django')
from .settings import BASE_DIR
LOG_PATH = os.path.join(BASE_DIR, 'log')

if not os.path.isdir(LOG_PATH):
    os.mkdir(LOG_PATH)
Log_level='INFO'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        }
    },
    'handlers': {
        'file': {
            'level': Log_level,
            # 'class': 'logging.FileHandler',
            # 若日志超过指定文件的大小，会再生成一个新的日志文件保存日志信息
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': "%s/log.txt" % LOG_PATH,
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': Log_level
        }
    },
}