from django.contrib import admin

# Register your models here.
from . import models

class DnsBindrrAdmin(admin.ModelAdmin):
    list_filter = ('type',)

class DnsBindZonesAdmin(admin.ModelAdmin):
    list_filter = ('type','city')

admin.site.register(models.DnsToolBindrr,DnsBindrrAdmin)
admin.site.register(models.DnsToolBindzones,DnsBindZonesAdmin)