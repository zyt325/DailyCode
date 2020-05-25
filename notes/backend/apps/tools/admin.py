from django.contrib import admin

# Register your models here.

from .models import ToolsCategory, ToolsUrl


class MultiDBModelAdmin(admin.ModelAdmin):
    using = 'tools'

    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

    def get_queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super().get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super().formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super().formfield_for_manytomany(db_field, request, using=self.using, **kwargs)


class ToolsUrlAdmin(MultiDBModelAdmin):
    list_filter = ['category']
    search_fields = ['name','url']

class ToolsCategoryAdmin(MultiDBModelAdmin):
    list_filter = ['type','parent_category']
    search_fields = ['name']

# forignKey
# class MultiDBTabularInline(admin.TabularInline):
#     using = 'tools'
#
#     def get_queryset(self, request):
#         # Tell Django to look for inline objects on the 'other' database.
#         return super().get_queryset(request).using(self.using)
#
#     def formfield_for_foreignkey(self, db_field, request, **kwargs):
#         # Tell Django to populate ForeignKey widgets using a query
#         # on the 'other' database.
#         return super().formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)
#
#     def formfield_for_manytomany(self, db_field, request, **kwargs):
#         # Tell Django to populate ManyToMany widgets using a query
#         # on the 'other' database.
#         return super().formfield_for_manytomany(db_field, request, using=self.using, **kwargs)
#
#
# class UrlsInline(MultiDBTabularInline):
#     model = Urls
#
#
# class UrlsAdmin(MultiDBModelAdmin):
#     inlines = [UrlsInline]

# admin.site.register(Classes,UrlsAdmin)

admin.site.register(ToolsUrl, ToolsUrlAdmin)
admin.site.register(ToolsCategory, ToolsCategoryAdmin)
