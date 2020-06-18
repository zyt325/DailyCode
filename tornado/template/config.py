import os

BASE_DIR = os.path.dirname(__file__)
options = {
    "port": 8000,
    "host": "127.0.0.1",
    "processes": 5
}
settings = {
    "debug": True,
    "autoreload": False,
    "compress_response": True,
    "static_path": os.path.join(BASE_DIR, "static"),
    "static_url_prefix": '/static/',
    "template_path": os.path.join(BASE_DIR, "templates")
}
