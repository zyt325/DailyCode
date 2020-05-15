from db.exts import db
from sqlalchemy.dialects.mysql.enumerated import ENUM
import pymysql
import json

pymysql.install_as_MySQLdb()
t_book_view = db.Table(
    'book_view',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('username', db.String(55)),
    db.Column('gender', ENUM('F', 'M')),
    db.Column('mobile', db.String(30)),
    db.Column('phone', db.String(125)),
    db.Column('wechat', db.String(125)),
    db.Column('email', db.String(125)),
    db.Column('attendance', db.Integer),
    db.Column('first_name', db.String(155)),
    db.Column('last_name', db.String(155)),
    db.Column('chinese_name', db.String(60)),
    db.Column('office_id', db.Integer),
    db.Column('department_id', db.Integer),
    db.Column('title_id', db.Integer),
    db.Column('logical_company_id', db.Integer),
    db.Column('dep_code', db.String(3)),
    db.Column('dep_english_name', db.String(60)),
    db.Column('dep_chinese_name', db.String(60)),
    db.Column('office_code', db.String(5)),
    db.Column('start_date', db.Date),
    db.Column('level_id', db.Integer),
    db.Column('office_english_name', db.String(125)),
    db.Column('title', db.String(255)),
    db.Column('title_cn', db.String(255)),
    db.Column('code', db.String(3))
)


def to_json(inst, cls):
    d = dict()
    '''
    获取表里面的列并存到字典里面
    '''
    for c in cls.__table__.columns:
        v = getattr(inst, c.name)
        d[c.name] = v
    # return json.dumps(d)
    return d


class Book_view(db.Model):
    # pass
    @property
    def serialize(self):
        return to_json(self, self.__class__)


Book_view().__table__ = t_book_view
