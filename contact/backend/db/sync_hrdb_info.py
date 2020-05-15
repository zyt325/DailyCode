import sys

sys.path.append('/app/address_book/backend/module')
sys.path.append('/zyt/python/work/work/address_book/backend/module')
from Company import Company
from Attendance import Attendance
from datetime import datetime, timedelta
from DB import DB
from db import config

c = Company()
a = Attendance()
dbase = config.DATABASE
# These cities have no employees yet
skip_cities = []
gender_color = {'M': 'blue', 'F': 'red', 'U': 'white'}
db_con, db_cur = DB().connect()
test_con, test_cur = DB().connect(host=config.HOST, user=config.USERNAME, passwd=config.PASSWORD)
ignore_users = []
query = 'select * from basefx.sync_ignore_users where service = "wiki_hr"'
db_cur.execute(query)

for res in db_cur.fetchall():
    ignore_users.append(res['username'])


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
    for l in c.locations:
        test_cur.execute("insert into %s.office value(%d,'%s','%s')" % (dbase,
                                                                        c.locations[l]['id'], l,
                                                                        c.locations[l]['name']))
    test_con.commit()


def sync_hrdb_title():
    db_cur.execute(
        "select `id`,`english_name`,REGEXP_REPLACE(`english_name`, 'Senior|Junior', '') as 'wiki_title',REGEXP_REPLACE(`chinese_name`, '高级|Senior|初级', '') as 'wiki_title_cn' from hr_new.`titles`")
    for t in db_cur.fetchall():
        test_cur.execute("insert into %s.title value(%d,'%s','%s','%s')" % (dbase,
                                                                            t['id'], t['english_name'], t['wiki_title'],
                                                                            t['wiki_title_cn']))
    test_con.commit()


def sync_hrdb_department():
    for dep in c.departments:
        test_cur.execute("insert into %s.department value(%d,'%s','%s','%s')" % (dbase,
                                                                                 c.departments[dep]['id'], dep,
                                                                                 c.departments[dep]['name'],
                                                                                 c.departments[dep]['chinese_name']))
    test_con.commit()


def sync_hrdb_logical_company():
    db_cur.execute('select id,code from hr_new.logical_companies')
    for l in db_cur.fetchall():
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


def insert_hrdb_people(employees):
    for i in employees:
        if i in ignore_users: continue
        u_info = c.employees[i]
        if u_info['city'] not in ['LA']:
            print(u_info['username'])
            if u_info['department'] == 'RMD': continue
            attendance = 1 if get_src_attendance(u_info['username']) else 0
            office_id = get_office(u_info['location_code'])
            dep_id = get_dep(u_info['department'])
            title_id = get_title(u_info['title'])
            logical_company_id = get_logical_company(u_info['logical_company_code'])
            test_cur.execute(
                "insert into %s.people value(%d,'%s','%s','%s','%s','%s','%s',%d,'%s','%s','%s','%s',%d,%d,%d,%d,%d)" % (
                    dbase, i, u_info['username'], u_info['gender'], u_info['mobile'], u_info['office_phone'],
                    u_info['wechat'],
                    u_info['email'], attendance, u_info['first_name'], u_info['last_name'], u_info['chinese_name'],
                    u_info['start_date'], u_info['level_id'], office_id, dep_id, title_id, logical_company_id))
    test_con.commit()


def sync_hrdb_people():
    # print(i, c.employees[i])
    insert_hrdb_people(c.employees)


def get_dest_attendance():
    test_cur.execute("select username,attendance from %s.people " % dbase)
    result = {}
    for i in test_cur.fetchall():
        result[i['username']] = i['attendance']
    return result


def get_dest_people():
    test_cur.execute("select id from %s.people " % dbase)
    result = []
    for i in test_cur.fetchall():
        result.append(i['id'])
    return result


def update_attendance():
    dest_attendance = get_dest_attendance()
    for k, v in dest_attendance.items():
        src_attendance = 1 if get_src_attendance(k) else 0
        if int(src_attendance) != int(v):
            print(k,v,src_attendance)
            test_cur.execute("update %s.people set attendance=%d where username='%s'" % (dbase, src_attendance, k))
    test_con.commit()



def update_people():
    src_people = c.employees.keys()
    insert_people = set(src_people) - set(get_dest_people())
    delete_people = set(get_dest_people()) - set(src_people)
    if delete_people:
        print('delete', delete_people)
        for i in delete_people:
            test_cur.execute("delete from %s.people where id=%d " % (dbase, i))
        test_con.commit()
    if insert_people:
        print('insert', insert_people)
        insert_hrdb_people(insert_people)


# if __name__ == '__main__':
#     update_attendance()
#     update_attendance()
# update_people()
# sync_hrdb_department()
# sync_hrdb_office()
# sync_hrdb_logical_company()
# sync_hrdb_people()
# print(get_attendance('zhangyt'))
