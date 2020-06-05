import sys

sys.path.append('/app/address_book/backend/module')
sys.path.append('/zyt/python/work/work/address_book/backend/module')
from Company import Company
from Attendance import Attendance
from datetime import datetime, timedelta
from DB import DB
from db import config
from Logger import Logger

Logger = Logger(handler='file', handler_file_dir='/app/log')
# Logger = Logger()
logger = Logger.logger
c = Company()
a = Attendance()
dbase = config.DATABASE
# These cities have no employees yet
skip_cities = []
gender_color = {'M': 'blue', 'F': 'red', 'U': 'white'}
db_con, db_cur = DB().connect()
test_con, test_cur = DB().connect(host=config.HOST, user=config.USERNAME, passwd=config.PASSWORD)


def is_connected_contact():
    global test_con, test_cur
    try:
        test_con.ping()
    except:
        test_con, test_cur = DB().connect(host=config.HOST, user=config.USERNAME, passwd=config.PASSWORD)


def is_connected_db():
    global db_con, db_cur
    try:
        db_con.ping()
    except:
        db_con, db_cur = DB().connect()


def get_ignore():
    ignore_users = []
    is_connected_db()
    query = 'select * from basefx.sync_ignore_users where service = "wiki_hr"'
    db_cur.execute(query)

    for res in db_cur.fetchall():
        ignore_users.append(res['username'])
    return ignore_users


def create_database():
    test_cur.execute("create database %s /*!40100 DEFAULT CHARACTER SET utf8mb4 */;" % dbase)
    test_con.commit()


def drop_database():
    test_cur.execute("drop database %s;" % dbase)
    test_con.commit()


def init_database():
    drop_database()
    create_database()


def drop_table_book_view1():
    test_cur.execute("drop table %s.book_view;" % dbase)
    test_con.commit()


def drop_view_book_view():
    test_cur.execute("drop view %s.book_view;" % dbase)
    test_con.commit()


def create_view_book_view():
    sql = '''CREATE VIEW %s.book_view AS SELECT p.*,d.code AS dep_code,d.english_name AS dep_english_name,d.chinese_name AS dep_chinese_name,o.code AS office_code,o.english_name AS office_english_name,t.wiki_title AS title,t.wiki_title_cn AS title_cn,l.code FROM %s.people p LEFT JOIN %s.department d ON p.department_id=d.id LEFT JOIN %s.office o ON p.office_id=o.id LEFT JOIN %s.title t ON p.title_id=t.id LEFT JOIN %s.logical_company l ON p.logical_company_id=l.id;''' % (
        dbase, dbase, dbase, dbase, dbase, dbase)
    test_cur.execute(sql)
    test_con.commit()


def sync_hrdb_office():
    logger.info("sync office")
    Logger.remove()
    for l in c.locations:
        res_src = c.locations[l]
        test_cur.execute("select id from %s.office where id=%d" % (dbase, res_src['id']))
        if test_cur.fetchone():
            test_cur.execute("update %s.office set code='%s',english_name='%s' where id=%d" % (
                dbase, l, res_src['name'], res_src['id']))
        else:
            test_cur.execute("insert into %s.office value(%d,'%s','%s')" % (dbase, res_src['id'], l, res_src['name']))
    test_con.commit()


def sync_hrdb_title():
    logger.info("sync title")
    Logger.remove()
    db_cur.execute(
        "select `id`,`english_name`,REGEXP_REPLACE(`english_name`, 'Senior|Junior', '') as 'wiki_title',REGEXP_REPLACE(`chinese_name`, '高级|Senior|初级', '') as 'wiki_title_cn' from hr_new.`titles`")
    res_src = db_cur.fetchall()
    for t in res_src:
        test_cur.execute("select id from %s.title where id=%d" % (dbase, t['id']))
        if test_cur.fetchone():
            test_cur.execute(
                "update %s.title set english_name='%s',wiki_title='%s',wiki_title_cn='%s' where id=%d" % (
                    dbase, t['english_name'], t['wiki_title'], t['wiki_title_cn'], t['id']))
        else:
            print(t)
            test_cur.execute("insert into %s.title value(%d,'%s','%s','%s')" % (
                dbase, t['id'], t['english_name'], t['wiki_title'], t['wiki_title_cn']))
    test_con.commit()


def sync_hrdb_department():
    logger.info("sync department")
    Logger.remove()
    for dep in c.departments:
        res_src = c.departments[dep]
        test_cur.execute("select id from %s.department where id=%d" % (dbase, res_src['id']))
        if test_cur.fetchone():
            test_cur.execute(
                "update %s.department set code='%s',english_name='%s',chinese_name='%s' where id=%d" % (
                    dbase, dep, res_src['name'], res_src['chinese_name'], res_src['id']))
        else:
            test_cur.execute("insert into %s.department value(%d,'%s','%s','%s')" % (
                dbase, res_src['id'], dep, res_src['name'], res_src['chinese_name']))
    test_con.commit()


def sync_hrdb_logical_company():
    logger.info("sync logical_company")
    Logger.remove()
    db_cur.execute('select id,code from hr_new.logical_companies')
    res_src = db_cur.fetchall()
    for l in res_src:
        test_cur.execute("select id from %s.logical_company where id=%d" % (dbase, l['id']))
        if test_cur.fetchone():
            test_cur.execute("update %s.logical_company set code='%s' where id=%d" % (dbase, l['code'], l['id']))
        else:
            test_cur.execute("insert into %s.logical_company value(%d,'%s')" % (dbase,
                                                                                l['id'], l['code']))
    test_con.commit()


def get_src_attendance(username):
    end_time = datetime.strptime('05-59', "%H-%M").time()
    begin_time = datetime.strptime('00-00', "%H-%M").time()
    now_time = datetime.now().time()

    if now_time > begin_time and now_time < end_time:
        clock_in_date = (
                datetime.now() + timedelta(days=-1)).strftime("%Y-%m-%d")
        result = a.user_was_present(
            username, clock_in_date, source='zknet')
        if result == False:
            clock_in_date = datetime.now().strftime("%Y-%m-%d")
    else:
        last_clocked_in_time = a.last_clocked_in(
            username, datetime.now().strftime("%Y-%m-%d"))
        if last_clocked_in_time:
            if last_clocked_in_time.time() > end_time:
                clock_in_date = datetime.now().strftime("%Y-%m-%d")
            else:
                clock_in_date = (
                        datetime.now() + timedelta(days=+1)).strftime("%Y-%m-%d")
        else:
            clock_in_date = datetime.now().strftime("%Y-%m-%d")
    return a.user_was_present(username, clock_in_date, source='zknet')


def get_office(code):
    test_cur.execute("select id from %s.office where code='%s'" % (dbase, code))
    return test_cur.fetchone()['id']


def get_dep(code):
    test_cur.execute("select id from %s.department where code='%s'" % (dbase, code))
    return test_cur.fetchone()['id']


def get_title(title):
    test_cur.execute("select id from %s.title where english_name='%s'" % (dbase, title))
    return test_cur.fetchone()['id']


def get_logical_company(code):
    test_cur.execute("select id from %s.logical_company where code='%s'" % (dbase, code))
    return test_cur.fetchone()['id']


def get_hrdb_info(i):
    people_info = {}
    u_info = c.employees[i]
    if u_info['city'] not in ['LA']:
        attendance = 0
        office_id = get_office(u_info['location_code'])
        dep_id = get_dep(u_info['department'])
        title_id = get_title(u_info['title'])
        logical_company_id = get_logical_company(u_info['logical_company_code'])
        people_info = {'id': i, 'username': u_info['username'], 'gender': u_info['gender'], 'mobile': u_info['mobile'],
                       'phone': u_info['office_phone'],
                       'wechat': u_info['wechat'], 'email': u_info['email'], 'attendance': attendance,
                       'first_name': u_info['first_name'],
                       'last_name': u_info['last_name'], 'chinese_name': u_info['chinese_name'],
                       'start_date': u_info['start_date'],
                       'level_id': u_info['level_id'], 'office_id': office_id, 'department_id': dep_id,
                       'title_id': title_id, 'logical_company_id': logical_company_id}
    return people_info


def insert_hrdb_people(i):
    res = get_hrdb_info(i)
    if res:
        test_cur.execute(
            "insert into %s.people value(%d,'%s','%s','%s','%s','%s','%s',%d,'%s','%s','%s','%s',%d,%d,%d,%d,%d)" % (
                dbase, i, res['username'], res['gender'], res['mobile'], res['phone'],
                res['wechat'], res['email'], res['attendance'], res['first_name'], res['last_name'],
                res['chinese_name'], res['start_date'], res['level_id'], res['office_id'], res['department_id'],
                res['title_id'], res['logical_company_id']))
        test_con.commit()


def sync_hrdb_people():
    logger.info("sync people")
    Logger.remove()
    for i in c.employees:
        ignore_users = get_ignore()
        if c.employees[i]['username'] in ignore_users: continue
        if c.employees[i]['department'] == 'RMD': continue
        test_cur.execute("select id from %s.people where id=%d" % (dbase, i))
        if test_cur.fetchone():
            res = get_hrdb_info(i)
            if res:
                update_sql = """update %s.people set username='%s',gender='%s',mobile='%s',phone='%s',
                wechat='%s',email='%s',attendance=%d,first_name='%s',last_name='%s',chinese_name='%s',start_date='%s',
                level_id=%d,office_id=%d,department_id=%d,title_id=%d,logical_company_id=%d  where id=%d"""% (
                    dbase, res['username'], res['gender'], res['mobile'], res['phone'],
                    res['wechat'], res['email'], res['attendance'], res['first_name'], res['last_name'],
                    res['chinese_name'], res['start_date'], res['level_id'], res['office_id'], res['department_id'],
                    res['title_id'], res['logical_company_id'],i)
                test_cur.execute(update_sql)
                test_con.commit()

        else:
            insert_hrdb_people(i)


def get_dest_attendance():
    test_cur.execute("select username,attendance from %s.people" % dbase)
    result = {}
    for i in test_cur.fetchall():
        # print(i)
        result[i['username']] = i['attendance']
    return result


def get_dest_people():
    test_cur.execute("select id from %s.people" % dbase)
    result = []
    for i in test_cur.fetchall():
        result.append(i['id'])
    return result


def update_attendance():
    is_connected_contact()
    is_connected_db()
    dest_attendance = get_dest_attendance()
    for k, v in dest_attendance.items():
        src_attendance = 1 if get_src_attendance(k) else 0
        if int(src_attendance) != int(v):
            logger.info("update attendance: %s %s %s" % (k, v, src_attendance))
            Logger.remove()
            test_cur.execute("update %s.people set attendance=%d where username='%s'" % (dbase, src_attendance, k))
    test_con.commit()


def update_people():
    is_connected_contact()
    is_connected_db()
    src_people = c.employees.keys()
    insert_people = set(src_people) - set(get_dest_people())
    delete_people = set(get_dest_people()) - set(src_people)
    if delete_people:
        logger.info("delete people: %s" % delete_people)
        Logger.remove()
        for i in delete_people:
            test_cur.execute("delete from %s.people where id=%d " % (dbase, i))
        test_con.commit()
    if insert_people:
        for i in insert_people:
            logger.info("insert people: %s" % delete_people)
            Logger.remove()
            insert_hrdb_people(i)


def sync_data():
    sync_hrdb_department()
    sync_hrdb_office()
    sync_hrdb_title()
    sync_hrdb_logical_company()
    sync_hrdb_people()

# if __name__ == '__main__':
#     get_dest_attendance()
#     update_attendance()
# update_people()
# sync_hrdb_department()
# sync_hrdb_office()
# sync_hrdb_logical_company()
# sync_hrdb_people()
# print(get_attendance('zhangyt'))
