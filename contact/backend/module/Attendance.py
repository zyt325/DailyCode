# coding:utf-8
from DB import DB
import Company
from datetime import timedelta, datetime


def _dates(begin_date, end_date=None):
    if not end_date: end_date = begin_date
    if type(begin_date) == type(datetime.date(datetime.now())):
        from_date = begin_date
    else:
        from_date = datetime.strptime(begin_date, '%Y-%m-%d').date()
    if type(end_date) == type(datetime.date(datetime.now())):
        to_date = end_date
    else:
        to_date = datetime.strptime(end_date, '%Y-%m-%d').date()

    return [from_date + timedelta(n) for n in range(int((to_date - from_date).days + 1))]


class Attendance:
    def __init__(self):
        self.users = {'all': {}, 'enabled': {}, 'disabled': {}}
        self.DB = DB()
        self.c = Company.Company()
        self.db_con, self.db_cur = self.DB.connect()
        self.dbd_con, self.dbd_cur = self.DB.connect(host='dbd.base-fx.com')
        query = 'select * from zknet.users'
        self.db_cur.execute(query)
        self.sources = ['zknet', 'actionlogger']
        results = self.db_cur.fetchall()
        for result in results:
            self.users['all'][result['username']] = result
            if result['department'] == '离职':
                self.users['disabled'][result['username']] = result
            else:
                self.users['enabled'][result['username']] = result

    def is_connected_db(self):
        try:
            self.db_con.ping()
        except:
            self.db_con, self.db_cur = self.DB.connect()

    def is_connected_dbd(self):
        try:
            self.db_con.ping()
        except:
            self.dbd_con, self.dbd_cur = self.DB.connect(host='dbd.base-fx.com')

    def work_minutes_in_date(self, begin_date, end_date=None, user=None, production=True):
        if user: production = self.c.employee(user, 'is_production')
        if production:
            production_string = 'production'
        else:
            production_string = 'non_production'
        work_minutes = 0
        for current_date in _dates(begin_date, end_date):
            query = '''select cal.%s_work_time from hr_new.`calendar_view` cal
                    where date_format(cal.date,'%%Y-%%m-%%d') = "%s" limit 1''' % (production_string, current_date)
            self.dbd_cur.execute(query)
            result = self.dbd_cur.fetchone()
            work_minutes += result['%s_work_time' % production_string]
        return work_minutes

    def _user_was_present(self, user, specific_date, source='zknet'):
        user = self.c.employee(user, 'username')
        if source == 'actionlogger':
            query = '''select `id` from basefx.`worktime`
                            where username = '%s'
                            and start_time between '%s 06:00:00'
                            and '%s 23:59:00'
                            limit 1''' % (user, specific_date, specific_date)
            self.db_cur.execute(query)
            result = self.db_cur.fetchone()
        elif source == 'zknet':
            # query = '''select `id` from zknet.`checkinout` c
            #                     left join zknet.users u
            #                         on u.userid = c.userid
            #                     where u.username = '%s'
            #                         and date_format(c.checktime,'%%Y-%%m-%%d') = '%s'
            #                     limit 1''' % (user, specific_date)
            query = '''select `person_id` from attendance.attendance_summary
                                where username = '%s'
                                    and date_format(last_check,'%%Y-%%m-%%d') = '%s' ''' % (user, specific_date)
            self.dbd_cur.execute(query)
            result = self.dbd_cur.fetchone()
        else:
            return False

        if result:
            return True
        else:
            return False

    def user_was_present(self, user, begin_date, end_date=None, source='all'):
        present = [True]
        self.is_connected_dbd()
        self.is_connected_db()
        for current_date in _dates(begin_date, end_date):
            if source == 'all':
                current_present = [False]
                for current_source in self.sources:
                    current_present.append(
                        bool(self._user_was_present(user, specific_date=current_date, source=current_source)))
                present.append(max(current_present))
            else:
                present.append(bool(self._user_was_present(user, specific_date=current_date, source=source)))
        return min(present)

    def date_is_workday(self, begin_date, user=None, production=True):
        # Returns true if there is any workable hours on a day
        # That means normal Saturday = True, normal Sunday or holiday = False
        if user: production = self.c.employee(user, 'is_production')
        if self.work_minutes_in_date(begin_date, production=production):
            return True
        return False

    def user_absent_time(self, user, begin_date, end_date=None, production=False):
        user = self.c.employee(user, 'username')
        minutes_absent = 0
        for current_date in _dates(begin_date, end_date):
            if not self.date_is_workday(current_date): continue
            if self.user_was_present(user, current_date): continue
            minutes_absent += self.work_minutes_in_date(current_date, production=production)
        return minutes_absent

    def _late_time(self, user, begin_date, end_date=None, expected_work_time='09:00:00', source='zknet'):
        user = self.c.employee(user, 'username')
        minutes_late = 0
        for current_date in _dates(begin_date, end_date):
            if not self.date_is_workday(current_date, user): continue
            if source == 'actionlogger':
                query = '''select timestampdiff(minute,'%s %s', start_time) as minutes_late
                from basefx.worktime
                where username = '%s'
                and start_time between '%s 06:00:00' and '%s 23:59:59' limit 1''' % (
                    current_date, expected_work_time, user, current_date, current_date)
            elif source == 'zknet':
                query = '''select min(c.checktime) as 'first_badge_swipe',timestampdiff(minute,'%s %s', min(c.checktime) ) as 'minutes_late' from zknet.checkinout c
                                 left join zknet.users u
                                     on u.userid = c.userid
                                 where u.username = '%s'
                                 and c.checktime between "%s 06:00:00" and "%s 23:59:59" ''' % (
                    current_date, expected_work_time, user, current_date, current_date)
            else:
                return 0
            self.db_cur.execute(query)
            result = self.db_cur.fetchone()
            if not result:
                return -1
            if result['minutes_late'] < 0:
                current_minutes_late = 0
            else:
                current_minutes_late = result['minutes_late']
            minutes_late += current_minutes_late
        return minutes_late

    def late_time(self, user, begin_date, end_date=None, expected_work_time='09:00:00', source='all'):
        minutes_found = []
        if source == 'all':
            for current_source in self.sources:
                current_minutes = self._late_time(user, begin_date, end_date=end_date,
                                                  expected_work_time=expected_work_time, source=current_source)
                if current_minutes > -1:
                    minutes_found.append(current_minutes)
        else:
            minutes_found.append(
                self._late_time(user, begin_date, end_date=end_date, expected_work_time=expected_work_time,
                                source=source))
        return min(minutes_found)

    def _work_time(self, user, begin_date, end_date=None, source='zknet'):
        user = self.c.employee(user, 'username')
        minutes = 0
        for current_date in _dates(begin_date, end_date):
            next_day = current_date + timedelta(days=1)
            if source == 'actionlogger':
                query = '''select `total`/60 as minutes
                    from basefx.worktime
                    where username = '%s'
                    and start_time like '%s%%' limit 1''' % (user, current_date)
            elif source == 'zknet':
                query = '''select timestampdiff(minute, min(checktime), max(checktime) ) as 'minutes', count(*) as 'records'
                                 from zknet.checkinout c
                                 left join zknet.users u
                                     on u.userid = c.userid
                                 where u.username = '%s'
                                 and c.checktime between "%s 06:00:00" and "%s 06:00:00"''' % (
                    user, current_date, next_day)
            else:
                return 0
            self.dbd_cur.execute(query)
            result = self.dbd_cur.fetchone()
            if result and 'minutes' in result and result['minutes']:
                current_minutes = result['minutes']
            else:
                current_minutes = 0
            if result and not current_minutes and result['records'] and source == 'zknet':
                current_minutes = 1
            minutes += current_minutes
        return minutes

    def work_time(self, user, begin_date, end_date=None, source='all'):
        minutes = 0
        if source == 'all':
            for current_source in self.sources:
                current_minutes = self._work_time(user, begin_date, end_date=end_date, source=current_source)
                if current_minutes > minutes:
                    minutes = current_minutes
        else:
            minutes = self._work_time(user, begin_date, end_date=end_date, source=source)
        return minutes

    def overtime(self, user, begin_date, end_date=None, source='all'):
        # Calculate time spent on Saturday past lunch, or Sunday (any time)
        minutes = 0
        for current_date in _dates(begin_date, end_date):
            workable_minutes = self.work_minutes_in_date(current_date, user=user)
            if workable_minutes <= 210:
                work_minutes = self.work_time(user=user, begin_date=current_date)
                if work_minutes > workable_minutes:
                    minutes += work_minutes - workable_minutes
        return minutes

    def long_hours(self, user, begin_date, end_date=None, source='all'):
        # Calculate over time during the week, which doesn't turn to comp
        minutes = 0
        for current_date in _dates(begin_date, end_date):
            workable_minutes = self.work_minutes_in_date(current_date, user=user)
            if workable_minutes > 210:
                work_minutes = self.work_time(user=user, begin_date=current_date)
                if work_minutes > workable_minutes:
                    minutes += work_minutes - workable_minutes
        return minutes

    def last_clocked_in(self, user, begin_date, end_date=None):
        self.is_connected_db()
        # find user last clocked in time
        if end_date:
            query = '''select `checktime` from zknet.`checkinout` c
                                left join zknet.users u
                                    on u.userid = c.userid
                                where u.username = '%s'
                                and (date_format(c.checktime,'%%Y-%%m-%%d') between '%s' and '%s')
                                order by checktime desc
                                limit 1''' % (user, begin_date, end_date)
        else:
            query = '''select `checktime` from zknet.`checkinout` c
                                left join zknet.users u
                                    on u.userid = c.userid
                                where u.username = '%s'
                                    and date_format(c.checktime,'%%Y-%%m-%%d') like '%s' order by checktime desc
                                limit 1''' % (user, begin_date)
        self.db_cur.execute(query)
        result = self.db_cur.fetchone()
        if result:
            return result['checktime']
        else:
            return False
