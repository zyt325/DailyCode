from flask import Flask, url_for, redirect, render_template, request, jsonify
from db import config
from db.models import *
from db.models_view import *
from cron.apscheduler import *

config.SCHEDULER_TIMEZONE = SCHEDULER_TIMEZONE
config.SCHEDULER_API_ENABLED = SCHEDULER_API_ENABLED
config.JOBS = JOBS
app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)

# scheduler.init_app(app)
# scheduler.start()
import atexit
import fcntl


def register_scheduler(app):
    f = open("scheduler.lock", "wb")
    try:
        fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        scheduler = APScheduler()
        scheduler.init_app(app)
        scheduler.start()
    except:
        pass

    def unlock():
        fcntl.flock(f, fcntl.LOCK_UN)
        f.close()

    atexit.register(unlock)


register_scheduler(app)


@app.route('/')
def index():
    return jsonify(json_list=[i.serialize for i in Book_view.query.filter(Book_view.dep_code == 'RLO').all()])
    # return render_template('index.html')


@app.route('/api/city/')
def get_city():
    return jsonify([i[0] for i in Office.query.with_entities(Office.code).order_by(Office.code)])


@app.route('/api/city_dep/')
def get_city_dep():
    """get dep of have menber,and by city"""
    office_code = request.args.get('city', 'all')
    return jsonify(
        [i[0] for i in Book_view.query.filter(Book_view.office_code == office_code).with_entities(
            Book_view.dep_code).distinct().order_by(Book_view.dep_code)])


@app.route('/api/dep/')
def get_dep():
    """get dep of have menber"""
    # return jsonify([i.serialize for i in Department.query.all()])
    return jsonify(
        [i[0] for i in Book_view.query.with_entities(Book_view.dep_code).distinct().order_by(Book_view.dep_code)])


@app.route('/api/people_city_dep/')
def get_people_by_city_dep():
    office_code = request.args.get('city', 'all')
    dep_code = request.args.get('dep', 'all')
    result = []
    if dep_code == 'all':
        for l in [i for i in
                  Book_view.query.filter_by(office_code=office_code).with_entities(Book_view.code, Book_view.dep_code,
                                                                                   Book_view.dep_english_name,
                                                                                   Book_view.dep_chinese_name).distinct().order_by(
                      Book_view.dep_code, Book_view.code)]:
            result.append({'key': l[0], 'dep': {'code': l[1], 'english_name': l[2], 'chinese_name': l[3]},
                           'value': [i.serialize for i in Book_view.query.filter_by(office_code=office_code, code=l[0],
                                                                                    dep_code=l[1]).order_by(
                               Book_view.dep_code, Book_view.code, Book_view.level_id.desc(),
                               Book_view.start_date).all()]})
        return jsonify(result)
    else:
        for l in [i for i in
                  Book_view.query.filter_by(office_code=office_code, dep_code=dep_code).with_entities(Book_view.code,
                                                                                                      Book_view.dep_code,
                                                                                                      Book_view.dep_english_name,
                                                                                                      Book_view.dep_chinese_name).distinct().order_by(
                      Book_view.code)]:
            # print(l)
            result.append({'key': l[0], 'dep': {'code': l[1], 'english_name': l[2], 'chinese_name': l[3]},
                           'value': [i.serialize for i in
                                     Book_view.query.filter_by(office_code=office_code, dep_code=dep_code,
                                                               code=l[0]).order_by(Book_view.level_id.desc(),
                                                                                   Book_view.start_date).all()]})
        return jsonify(result)


@app.route('/api/people_dep/')
def get_people_by_dep():
    dep_code = request.args.get('dep', 'all')
    result = []
    if dep_code == 'all':
        for l in [i for i in
                  Book_view.query.with_entities(Book_view.office_code, Book_view.dep_code, Book_view.dep_english_name,
                                                Book_view.dep_chinese_name).distinct().order_by(Book_view.office_code)]:
            result.append({'key': l[0], 'dep': {'code': l[1], 'english_name': l[2], 'chinese_name': l[3]},
                           'value': [i.serialize for i in
                                     Book_view.query.filter_by(office_code=l[0]).order_by(Book_view.level_id.desc(),
                                                                                          Book_view.start_date).all()]})
        return jsonify(result)
    else:
        for l in [i for i in
                  Book_view.query.filter(Book_view.dep_code == dep_code).with_entities(Book_view.office_code,
                                                                                       Book_view.dep_code,
                                                                                       Book_view.dep_english_name,
                                                                                       Book_view.dep_chinese_name).distinct().order_by(
                      Book_view.office_code)]:
            result.append({'key': l[0], 'dep': {'code': l[1], 'english_name': l[2], 'chinese_name': l[3]},
                           'value': [i.serialize for i in
                                     Book_view.query.filter_by(dep_code=dep_code, office_code=l[0]).order_by(
                                         Book_view.level_id.desc(), Book_view.start_date).all()]})
        return jsonify(result)


if __name__ == "__main__":
    # app.run(host="0.0.0.0", debug=True)
    app.run()

if __name__ != "__main__":
    import logging

    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
