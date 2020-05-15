import os

DEBUG = True
SECRET_KEY = os.urandom(24)
# database set
DIALECT = 'mysql'
DRIVER = 'mysqldb'
# USERNAME = 'root'
# PASSWORD = 'mysql325'
# HOST = '127.0.0.1'
# HOST='docker03.base-fx.com'
HOST = 'db08.base-fx.com'
USERNAME = 'address_book'
PASSWORD = 'Rcvs94d~'
PORT = '3306'
DATABASE = 'contact'
# DATABASE = 'address_book'
SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT,
                                                                       DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = False
