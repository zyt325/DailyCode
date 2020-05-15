#!/usr/bin/python
# coding:utf-8

from DB import DB
from datetime import datetime
from it_auto_cache.auto_cache import AutoCache
import Variables
from Logger import Logger

only_read, force_update = Variables.get_hr_cache()
cache = AutoCache('Company', only_read=only_read,
                  force_update=force_update, expire_time=300)


class Company:
    def __init__(self, include_old_employees=False, include_candidates=False, include_pre_employees=False, include_student=False,
                 include_client=False, only='all'):

        self.DB = DB()
        self.logger = Logger().logger
        # self.con, self.cur = self.DB.connect()

        if only in ['all', 'departments']:
            self.departments = self._get_departments()
            self.companies = self._get_companies()
        if only in ['all', 'positions', 'employees']:
            self.titles = self._get_titles()
        if only in ['all', 'employees']:
            self.departments = self._get_departments()
            self.companies = self._get_companies()
            self.employees = self._get_employees(include_old_employees=include_old_employees,
                                                 include_candidates=include_candidates,
                                                 include_pre_employees=include_pre_employees,
                                                 include_student=include_student,
                                                 include_client=include_client)
            self.employees_by_status = self.people(
                group_by='employment_status')
            self.employees_by_username = self.people()
        if only in ['all', 'countries']:
            self.countries = self._get_countries()
        if only in ['all', 'levels', 'employees']:
            self.levels = self._get_levels()
        if only in ['all', 'locations', 'employees']:
            self.locations, self.locations_long = self._get_locations()

    def _strip_department(self, department):
        if not department:
            return 'Unknown'
        if 'DMT' in department:
            return 'DEM'
        if 'ENV' in department:
            return 'DEM'
        try:
            return department.split()[2]
        except:
            return department.split()[0]

    @cache.decorator
    def _get_companies(self):
        cur = self.DB.cursor()
        companies = {}
        query = "select code from hr_new.logical_companies"
        cur.execute(query)
        results = cur.fetchall()
        for result in results:
            companies[result['code']] = {'employees': []}

        # self.employees_by_company_and_department = {}
        # for company in self.companies:
        #     self.employees_by_company_and_department[company] = {}
        #     for department in self.departments:
        #         self.employees_by_company_and_department[company][department] = []
        return companies

    @cache.decorator
    def _get_departments(self):
        cur = self.DB.cursor()
        departments = {}
        query = """select
                    `id`,
                    `english_name`,
                    `chinese_name`,
                    `code`,
                    `is_production`,
                    `production_category`,
                    `is_rgu`
                    from hr_new.`departments`"""
        cur.execute(query)
        results = cur.fetchall()
        for result in results:
            code = self._strip_department(result['code'])
            departments[code] = {}
            departments[code]['name'] = result['english_name']
            departments[code]['chinese_name'] = result['chinese_name']
            departments[code]['production_category'] = result['production_category']
            departments[code]['is_production'] = bool(result['is_production'])
            departments[
                code]['is_rgu'] = bool(result['is_rgu'])
            departments[code]['id'] = result['id']
            # departments[code].setdefault('employees', [])
        return departments

    @cache.decorator
    def _get_titles(self):
        cur = self.DB.cursor()
        titles = {}
        query = 'select `english_name`,`chinese_name` from hr_new.`titles`'
        cur.execute(query)
        results = cur.fetchall()
        for result in results:
            titles[result['english_name']] = {}
            titles[result['english_name']
                   ]['chinese_name'] = result['chinese_name']
        return titles

    @cache.decorator
    def _get_employees(self, include_old_employees=False, include_candidates=False, include_pre_employees=False, include_student=False,
                       include_client=False):
        # TODO it turns out that if we ignore deleted employees and null usernames, there arent' duplicate usernames
        # 1.Remove field: country id,level id,wechat,is_bmc,is_bam,date_of_birth
        # 2.hr_new database does not have a position table, so about position method and property are removed
        # 3.Email address gets aliases from the email database, and if not then use username as email address
        cur = self.DB.cursor()
        employees = {}
        # self.employees_by_level = {}
        # self.employees_by_start_date = {}
        # self.employees_by_username = {}
        # self.employees_by_status = {}
        query = """select *,
                        p.`department_code` as 'department',
                        p.`english_given_name` as 'first_name',
                        p.`english_middle_name` as 'middle_name',
                        p.`english_family_name` as 'last_name',
                        p.`english_full_name` as 'english_name',
                        p.`chinese_family_name` as 'xing',
                        p.`chinese_given_name` as 'mingzi',
                        p.`chinese_full_name` as 'chinese_name',
                        p.`category`,
                        p.status as 'employment_status',
                        p.`logical_company_code` as 'home_company',
                        p.`title_english_name` as 'position',
                        p.`title_chinese_name` as 'position_cn',
                        p.`title_english_name` as 'title',
                        p.`title_chinese_name` as 'title_cn',
                        p.`office_english_name` as 'location',
                        p.`office_code` as 'location_code',
                        p.`office_country_english_name` as 'country',
                        p.`office_country_code` as 'country_short',
                        p.`level_english_name` as 'level',
                        p.`office_code` as 'city',
                        COALESCE(m.`alias`, CONCAT(p.`username`,'@base-fx.com')) as 'email',
                        REGEXP_REPLACE(p.`title_english_name`,'Senior|Junior','') as 'wiki_title',
                        REGEXP_REPLACE(p.`title_chinese_name`,'高级|Senior|初级','') as 'wiki_title_cn',
                        s.`left` as 'seat_map_x',
                        s.`top` as 'seat_map_y'
                    from hr_new.people_view_itd p
                    left join seatmap.seat s
                        on s.`employee_id` = p.`id`
                    left join mail.sender_canonical m
                        on p.`username`= m.`name` 
                    order by p.`start_date`"""
        cur.execute(query)
        results = cur.fetchall()

        for result in results:
            if not include_old_employees and result['status'] == 'Past':
                continue
            if not include_pre_employees and result['status'] == 'Pending-In':
                continue
            if not include_candidates and result['category'] == 'candidate':
                continue
            if not include_student and result['category'] == 'student':
                continue
            if not include_client and result['category'] == 'client':
                continue
            # convert str true to bool
            for key in result:
                if str(result[key]).lower() == 'true':
                    result[key] = True
                elif str(result[key]).lower() == 'false':
                    result[key] = False
            employee_number = result['id']

            # if not result['start_date']:
            #    result['start_date'] = datetime.now().date()
            # string_date = result['start_date'].strftime('%Y-%m-%d')
            # self.employees_by_start_date.setdefault(string_date, [])
            # self.employees_by_start_date[string_date].append(employee_number)

            result['department'] = self._strip_department(result['department'])
            if result['username']:
                result['username'] = result['username'].lower().replace(' ', '')
            if not result['email']:
                result['email'] = str(result['username']) + '@base-fx.com'

            employees[employee_number] = result
            # self.employees_by_username[result['username']] = result
            # self.employees_by_status.setdefault(result['employment_status'], []).append(result['username'])

            # try:
            #     self.departments[result['department']].setdefault('employees', []).append(employee_number)
            # except:
            #     self.departments.setdefault(None, {}).setdefault('employees', []).append(employee_number)
            #
            # try:
            #     self.companies[result['home_company']]['employees'].append(employee_number)
            # except:
            #     self.companies.setdefault(None, {}).setdefault('employees', []).append(employee_number)
            #
            # self.employees_by_company_and_department[result['home_company']][result['department']].append(
            #     employee_number)
        return employees

    @cache.decorator
    def _get_countries(self):
        cur = self.DB.cursor()
        countries = {}
        query = 'select `english_name` from hr_new.`countries`'
        cur.execute(query)
        results = cur.fetchall()
        for result in results:
            countries[result['english_name']] = {}
        return countries

    @cache.decorator
    def _get_levels(self):
        cur = self.DB.cursor()
        levels = {}
        query = 'select `id`,`english_name`,`code` from hr_new.`levels`'
        cur.execute(query)
        results = cur.fetchall()
        for result in results:
            levels[result['code']] = {}
            levels[result['code']]['name'] = result['english_name']
            levels[result['code']]['id'] = result['id']
        return levels

    @cache.decorator
    def _get_locations(self):
        cur = self.DB.cursor()
        locations = {}
        locations_long = {}
        query = 'select `id`,`english_name`,`code` from hr_new.offices'
        cur.execute(query)
        results = cur.fetchall()
        for result in results:
            locations[result['code']] = {}
            locations[result['code']]['name'] = result['english_name']
            locations[result['code']]['id'] = result['id']
            locations[result['code']]['employees'] = []
            locations_long[result['english_name']] = {}
            locations_long[result['english_name']]['code'] = result['code']
            locations_long[result['english_name']]['id'] = result['id']
            locations_long[result['english_name']]['employees'] = []
            #
            # for employee in self.employees:
            #     if self.employees[employee]['location'] == result['english_name']:
            #         self.locations[result['code']]['employees'].append(employee)
            #         self.locations_long[result['english_name']]['employees'].append(employee)
        return locations, locations_long

    def employee(self, employee, item):
        for id in self.employees:
            try:
                if self.employees[id]['username'] == employee or id == employee:
                    return self.employees[id][item]
            except Exception as e:
                self.logger.error(type(e), e)

    def employee_department(self, employee):
        return self.employee(employee, 'department')

    def employee_title(self, employee):
        return self.employee(employee, 'title')

    def people(self, group_by=None, **kwargs):
        """
        get matching conditions people
        :param kwargs: use any people_view_itd field\
                group_by employees attribute ,
        :return:{'caofei':{*},'zhangcx':{*}}
        if greou_by , retrun {'group1':[],'group2':[]}
        example:
                people(group_by='employment_status')
                    return {'employee':[username],'post_employee':[username]}
        """
        filter = kwargs
        result = {}
        attr_mapping = {
            'city': 'office_code',
            'department': 'department_code',
            'startdate': 'start_date'
        }
        for e in self.employees:
            add = True
            for f in filter:
                attr = attr_mapping.get(f, f)
                if self.employees[e][attr] != filter[f]:
                    add = False
                    break
            if add:
                result[self.employees[e]['username']] = self.employees[e]
        if group_by:
            group = {}
            for e in result:
                group.setdefault(result[e][group_by], []).append(e)
            return group
        return result

    def department_employees(self, department, type='username', **kwargs):
        employees = []
        filter = {}
        filter['department_code'] = department
        filter.update(kwargs)
        people = self.people(**filter)
        for p in people:
            if type == 'username':
                employees.append(people[p]['username'])
            elif type in ['chinese_name', 'chinese']:
                employees.append(people[p][
                    'chinese_full_name'])  # employees.append("%s%s"%(self.employee(id, 'xing'),self.employee(id,'mingzi')))
            elif type in ['english_name', 'english']:
                employees.append(people[p]['english_full_name'])
        return employees

    def startdate_employees(self, startdate, type='username', **kwargs):
        employees = []
        filter = {}
        filter['start_date'] = startdate
        filter.update(kwargs)
        people = self.people(**filter)
        for p in people:
            if type == 'username':
                employees.append(people[p]['username'])
        return employees
