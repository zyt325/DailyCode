# _*_ codeing: utf-8 _*_

import os
import sys

pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd + "/../")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'notes.settings')

import django

from django.core.exceptions import ObjectDoesNotExist

django.setup()

from tools.models import ToolsCategory, ToolsUrl

# dumpdata --database tools tools.ToolsCategory
aa = []
bb = []

#for c in aa:
#    try:
#        parent_category = ToolsCategory.objects.using('tools').get(name=c['fields']['class_type'])
#    except ObjectDoesNotExist:
#        c_instance = ToolsCategory()
#        c_instance.name = c['fields']['class_type']
#        c_instance.type = 1
#        c_instance.is_tab = True
#        c_instance.save()


#for c in aa:
#    parent_category = ToolsCategory.objects.using('tools').get(name=c['fields']['class_type'])
#    c_instance = ToolsCategory()
#    c_instance.pk = c['pk']
#    c_instance.name = c['fields']['class_name']
#    c_instance.type = 2
#    c_instance.parent_category = parent_category
#    c_instance.is_tab = True
#    c_instance.save()

# for c in bb:
#     category = ToolsCategory.objects.using('tools').get(id=c['fields']['class_field'])
#     c_instance = ToolsUrl()
#     c_instance.name=c['fields']['title']
#     c_instance.desc = c['fields']['comment']
#     c_instance.url = c['fields']['url']
#     c_instance.category = category
#     c_instance.save()
