from django.contrib import admin

# Register your models here.
from . import models as Models
admin.site.register(Models.PicmCategory)
admin.site.register(Models.PicmPath)
