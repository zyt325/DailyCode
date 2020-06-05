from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from sqlalchemy_views import CreateView, DropView
from main import app
from db.models import *
from db.sync_hrdb_info import create_database, init_database, drop_table_book_view1, create_view_book_view, \
    drop_view_book_view, \
    sync_data, update_attendance

manager = Manager(app)

migrate = Migrate(app, db)
# python manage.py db
manager.add_command('migrate', MigrateCommand)


# python manage.py runserver

@manager.command
def create_db():
    """create db address_book"""
    create_database()


@manager.command
def init_db():
    """reset db address_book"""
    init_database()


@manager.command
def init_table():
    """reset table"""
    db.drop_all()
    db.create_all()


@manager.command
def drop_table_book_view():
    """ drop table book_view"""
    drop_table_book_view1()


@manager.command
def create_book_view():
    """create view book_view"""
    create_view_book_view()


@manager.command
def drop_book_view():
    """drop view book_view"""
    drop_view_book_view()


@manager.command
def sync_data_db():
    """init table data"""
    sync_data()


@manager.command
def update_kaoqin():
    """update_attendance"""
    update_attendance()


if __name__ == "__main__":
    manager.run()
