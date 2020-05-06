# _*_ codeing: utf-8 _*_

import os
import sys

pwd=os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd+"/../")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'notes.settings')

import django
django.setup()

from tools.models import ToolsCategory,ToolsUrl

from db_tools.data import tools_category_data
for c in tools_category_data.row_data:
    c_instance = ToolsCategory()
    c_instance.name=c['name']
    c_instance.type=c['type']
    c_instance.is_tab=c['is_tab']
    c_instance.save()

