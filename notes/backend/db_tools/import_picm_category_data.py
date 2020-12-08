# _*_ codeing: utf-8 _*_

import os
import sys

pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd + "/../")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'notes.settings')

import django

django.setup()

from picm.models import PicmCategory

picm_category_data = [
    {
        'name': '默认',
        'type': 1,
        'is_tab': True,
    }
]
for c in picm_category_data:
    c_instance = PicmCategory()
    c_instance.pk = -1
    c_instance.name = c['name']
    c_instance.type = c['type']
    c_instance.is_tab = c['is_tab']
    c_instance.save()
