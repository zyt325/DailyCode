# _*_ codeing: utf-8 _*_

import os
import sys

pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd + "/../")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'notes.settings')
import MySQLdb
import MySQLdb.cursors

mysql = MySQLdb
mysql_cursors = MySQLdb.cursors

con = mysql.connect(host='127.0.0.1', user='zyt', connect_timeout=10, use_unicode=False,
                    passwd='325', db='test', charset='utf8',
                    cursorclass=mysql_cursors.DictCursor)
cur = con.cursor()
import django

from django.core.exceptions import ObjectDoesNotExist

django.setup()
from note.models import NoteCategory,NoteArticle



def category():
    cur.execute('select * from note_class')
    for r in cur.fetchall():
        class_name = str(r['class_name'],encoding='utf-8')
        # if not r['upper_class']:
        #     c_instance = NoteCategory()
        #     c_instance.pk = r['id']
        #     c_instance.name = class_name
        #     c_instance.desc = ""
        #     c_instance.type = 1
        #     c_instance.save()
        
        if r['upper_class']:
            try:
                print(class_name)
                parent_category = NoteCategory.objects.using('notes').get(id=r['upper_class'])
                print(parent_category)
            except ObjectDoesNotExist as e:
                print(e)
                continue
            c_instance = NoteCategory()
            c_instance.pk = r['id']
            c_instance.name = class_name
            c_instance.desc = ""
            c_instance.type = 2
            c_instance.parent_category = parent_category
            c_instance.save()

def article():
    cur.execute('select * from note_article')
    for r in cur.fetchall():
        title = str(r['title'], encoding='utf-8')
        body = str(r['body'], encoding='utf-8')
        print(r['id'],title,r['class_id'])
        parent_category = NoteCategory.objects.using('notes').get(id=r['class_id'])
        c_instance = NoteArticle()
        c_instance.pk = r['id']
        c_instance.title = title
        c_instance.body = body
        c_instance.file_name = r['file_name']
        c_instance.category = parent_category
        c_instance.save()
        
article()