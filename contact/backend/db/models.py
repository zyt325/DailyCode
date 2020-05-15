from db.exts import db
from sqlalchemy.dialects.mysql.enumerated import ENUM
import pymysql
import json

pymysql.install_as_MySQLdb()


def to_json(inst, cls):
    d = dict()
    '''
    获取表里面的列并存到字典里面
    '''
    for c in cls.__table__.columns:
        v = getattr(inst, c.name)
        d[c.name] = v
    return d


class Office(db.Model):
    __tablename__ = 'office'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(5), nullable=False)
    english_name = db.Column(db.String(125), nullable=False)

    @property
    def serialize(self):
        return to_json(self, self.__class__)


class Department(db.Model):
    __tablename__ = 'department'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(3), nullable=False)
    english_name = db.Column(db.String(60), nullable=False)
    chinese_name = db.Column(db.String(60), nullable=False)

    @property
    def serialize(self):
        return to_json(self, self.__class__)


class Title(db.Model):
    __tablename__ = 'title'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    english_name = db.Column(db.String(255), nullable=False)
    wiki_title = db.Column(db.String(255), nullable=False)
    wiki_title_cn = db.Column(db.String(255), nullable=False)


class Logical_company(db.Model):
    __tablename__ = 'logical_company'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(3), nullable=False)


class People(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(55), nullable=False)
    gender = db.Column(ENUM('F', 'M'), nullable=False)
    mobile = db.Column(db.String(30))
    phone = db.Column(db.String(125))
    wechat = db.Column(db.String(125))
    email = db.Column(db.String(125))
    attendance = db.Column(db.Integer)
    first_name = db.Column(db.String(155), nullable=False)
    last_name = db.Column(db.String(155), nullable=False)
    chinese_name = db.Column(db.String(60), nullable=False)
    start_date = db.Column(db.Date)
    level_id = db.Column(db.Integer)
    office_id = db.Column(db.Integer, db.ForeignKey('office.id'))
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    title_id = db.Column(db.Integer, db.ForeignKey('title.id'))
    logical_company_id = db.Column(
        db.Integer, db.ForeignKey('logical_company.id'))
