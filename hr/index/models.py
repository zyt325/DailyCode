from django.db import models


# Create your models here.
class Calendar(models.Model):
    office = models.IntegerField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    weekday = models.CharField(max_length=9, blank=True, null=True)
    type = models.CharField(max_length=21, blank=True, null=True)
    note = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'calendar'


class CalendarWorktimes(models.Model):
    work_start = models.TimeField(blank=True, null=True)
    work_end = models.TimeField(blank=True, null=True)
    break_start = models.TimeField(blank=True, null=True)
    break_end = models.TimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'calendar_worktimes'


class Cities(models.Model):
    rank = models.IntegerField()
    province = models.ForeignKey('Provinces', models.DO_NOTHING, db_column='province')
    english_name = models.CharField(max_length=255)
    chinese_name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'cities'


class Countries(models.Model):
    code = models.CharField(unique=True, max_length=2)
    english_name = models.CharField(unique=True, max_length=125)
    chinese_name = models.CharField(unique=True, max_length=125)
    phone_code = models.IntegerField(blank=True, null=True)
    minimum_phone_length = models.PositiveIntegerField(blank=True, null=True)
    display_order = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'countries'


class DepartmentTags(models.Model):
    department = models.ForeignKey('Departments', models.DO_NOTHING, db_column='department', primary_key=True)
    tag = models.ForeignKey('Tags', models.DO_NOTHING, db_column='tag')

    class Meta:
        managed = False
        db_table = 'department_tags'
        unique_together = (('department', 'tag'),)


class DepartmentTitles(models.Model):
    department = models.ForeignKey('Departments', models.DO_NOTHING, db_column='department')
    title = models.ForeignKey('Titles', models.DO_NOTHING, db_column='title')

    class Meta:
        managed = False
        db_table = 'department_titles'
        unique_together = (('title', 'department'),)


class Departments(models.Model):
    code = models.CharField(max_length=3)
    english_name = models.CharField(unique=True, max_length=60)
    chinese_name = models.CharField(unique=True, max_length=60)
    is_rgu = models.PositiveIntegerField()
    is_production = models.PositiveIntegerField()
    directly_billed = models.PositiveIntegerField()
    vfx_order = models.PositiveIntegerField()
    production_category = models.CharField(max_length=9, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'departments'


class Levels(models.Model):
    code = models.CharField(unique=True, max_length=10)
    english_name = models.CharField(unique=True, max_length=125)

    class Meta:
        managed = False
        db_table = 'levels'


class LogicalCompanies(models.Model):
    code = models.CharField(max_length=150)
    english_name = models.CharField(max_length=255)
    chinese_name = models.CharField(max_length=255)
    description = models.CharField(max_length=1024, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'logical_companies'


class LogicalCompanyDepartments(models.Model):
    logical_company = models.ForeignKey(LogicalCompanies, models.DO_NOTHING, db_column='logical_company')
    department = models.ForeignKey(Departments, models.DO_NOTHING, db_column='department')

    class Meta:
        managed = False
        db_table = 'logical_company_departments'
        unique_together = (('department', 'logical_company'),)


class Offices(models.Model):
    code = models.CharField(unique=True, max_length=5)
    english_name = models.CharField(unique=True, max_length=125)
    chinese_name = models.CharField(unique=True, max_length=255)
    city = models.ForeignKey(Cities, models.DO_NOTHING, db_column='city')

    class Meta:
        managed = False
        db_table = 'offices'


class People(models.Model):
    bid = models.PositiveIntegerField(unique=True, blank=True, null=True)
    category = models.CharField(max_length=10)
    username = models.CharField(unique=True, max_length=55, blank=True, null=True)
    english_given_name = models.CharField(max_length=155)
    english_middle_name = models.CharField(max_length=155, blank=True, null=True)
    english_family_name = models.CharField(max_length=155)
    chinese_family_name = models.CharField(max_length=30, blank=True, null=True)
    chinese_given_name = models.CharField(max_length=30, blank=True, null=True)
    nickname = models.CharField(max_length=255, blank=True, null=True)
    logical_company = models.ForeignKey(LogicalCompanies, models.DO_NOTHING, db_column='logical_company')
    office = models.ForeignKey(Offices, models.DO_NOTHING, db_column='office')
    department = models.ForeignKey(Departments, models.DO_NOTHING, db_column='department')
    title = models.ForeignKey('Titles', models.DO_NOTHING, db_column='title')
    level = models.ForeignKey(Levels, models.DO_NOTHING, db_column='level', blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    employee_start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    mobile_country = models.IntegerField(blank=True, null=True)
    mobile = models.CharField(max_length=30, blank=True, null=True)
    public_wechat = models.CharField(max_length=125, blank=True, null=True)
    skype = models.CharField(max_length=125, blank=True, null=True)
    nationality = models.ForeignKey(Countries, models.DO_NOTHING, db_column='nationality')
    gender = models.CharField(max_length=1)
    marital_status = models.CharField(max_length=7, blank=True, null=True)
    registered_city = models.ForeignKey(Cities, models.DO_NOTHING, db_column='registered_city', blank=True, null=True)
    present_address_city = models.IntegerField(blank=True, null=True)
    has_head_photo = models.IntegerField()
    calendar_schedule = models.IntegerField(blank=True, null=True)
    disable_account_date = models.DateField(blank=True, null=True)
    backup_delete_email_date = models.DateField(blank=True, null=True)
    handover_to = models.PositiveIntegerField(blank=True, null=True)
    backup_email_to_handover = models.CharField(max_length=1, blank=True, null=True)
    student_departure_type = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'people'


class PeopleTags(models.Model):
    person = models.ForeignKey(People, models.DO_NOTHING, db_column='person')
    tag = models.ForeignKey('Tags', models.DO_NOTHING, db_column='tag')
    level = models.ForeignKey(Levels, models.DO_NOTHING, db_column='level', blank=True, null=True)
    note = models.CharField(max_length=2048, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'people_tags'


class Provinces(models.Model):
    country = models.ForeignKey(Countries, models.DO_NOTHING, db_column='country')
    english_name = models.CharField(max_length=25)
    chinese_name = models.CharField(max_length=25)

    class Meta:
        managed = False
        db_table = 'provinces'


class Recruiters(models.Model):
    person = models.ForeignKey(People, models.DO_NOTHING, db_column='person')

    class Meta:
        managed = False
        db_table = 'recruiters'


class Tags(models.Model):
    english_name = models.CharField(max_length=255, blank=True, null=True)
    chinese_name = models.CharField(max_length=255, blank=True, null=True)
    english_description = models.CharField(max_length=1024, blank=True, null=True)
    chinese_description = models.CharField(max_length=1024, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tags'


class Titles(models.Model):
    english_name = models.CharField(max_length=255)
    chinese_name = models.CharField(max_length=255)
    responsibilities_english = models.CharField(max_length=3072, blank=True, null=True)
    responsibilities_chinese = models.CharField(max_length=2048, blank=True, null=True)
    qualifications_english = models.CharField(max_length=2048, blank=True, null=True)
    qualifications_chinese = models.CharField(max_length=2048, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'titles'


class PeopleViewItd(models.Model):
    category = models.CharField(max_length=10)
    status = models.CharField(max_length=11)
    username = models.CharField(max_length=55, blank=True, null=True)
    english_given_name = models.CharField(max_length=255, blank=True, null=True)
    english_middle_name = models.CharField(max_length=155, blank=True, null=True)
    english_family_name = models.CharField(max_length=255, blank=True, null=True)
    english_full_name = models.CharField(max_length=411, blank=True, null=True)
    chinese_full_name = models.CharField(max_length=60, blank=True, null=True)
    chinese_family_name = models.CharField(max_length=30, blank=True, null=True)
    chinese_given_name = models.CharField(max_length=30, blank=True, null=True)
    nickname = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    employee_start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    mobile = models.CharField(max_length=30, blank=True, null=True)
    skype = models.CharField(max_length=125, blank=True, null=True)
    country_code = models.CharField(max_length=2, blank=True, null=True)
    local_expat = models.CharField(max_length=5)
    gender = models.CharField(max_length=1)
    has_head_photo = models.CharField(max_length=80)
    office_code = models.CharField(max_length=5, blank=True, null=True)
    office_english_name = models.CharField(max_length=125, blank=True, null=True)
    office_chinese_name = models.CharField(max_length=255, blank=True, null=True)
    office_city_english_name = models.CharField(max_length=255, blank=True, null=True)
    office_city_chinese_name = models.CharField(max_length=255, blank=True, null=True)
    office_province_english_name = models.CharField(max_length=25, blank=True, null=True)
    office_province_chinese_name = models.CharField(max_length=25, blank=True, null=True)
    office_country_english_name = models.CharField(max_length=125, blank=True, null=True)
    office_country_chinese_name = models.CharField(max_length=125, blank=True, null=True)
    office_country_code = models.CharField(max_length=2, blank=True, null=True)
    office_country_phone_code = models.IntegerField(blank=True, null=True)
    department_code = models.CharField(max_length=3, blank=True, null=True)
    department_english_name = models.CharField(max_length=60, blank=True, null=True)
    department_chinese_name = models.CharField(max_length=60, blank=True, null=True)
    is_rgu = models.CharField(max_length=60, blank=True, null=True)
    is_production = models.CharField(max_length=60, blank=True, null=True)
    level_id = models.PositiveIntegerField(blank=True, null=True)
    level_code = models.CharField(max_length=10, blank=True, null=True)
    level_english_name = models.CharField(max_length=125, blank=True, null=True)
    title_english_name = models.CharField(max_length=255, blank=True, null=True)
    title_chinese_name = models.CharField(max_length=255, blank=True, null=True)
    logical_company_code = models.CharField(max_length=150, blank=True, null=True)
    logical_company_english_name = models.CharField(max_length=255, blank=True, null=True)
    logical_company_chinese_name = models.CharField(max_length=255, blank=True, null=True)
    wechat = models.CharField(max_length=125, blank=True, null=True)
    disable_account_date = models.DateField(blank=True, null=True)
    backup_delete_email_date = models.DateField(blank=True, null=True)
    handover_to = models.PositiveIntegerField(blank=True, null=True)
    backup_email_to_handover = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'people_view_itd'
