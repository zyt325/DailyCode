from django.db import models
from datetime import datetime

table_prefix = 'tools_'


# Create your models here.
class AbstractCategory(models.Model):
    parent_category = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, verbose_name="父类目级别",
                                        related_name="sub_cat")

    class Meta:
        abstract = True

class ToolsCategory(AbstractCategory):
    CLASS_TYPE = ((1, "一级类目"), (2, "二级类目"), (3, "三级类目"),)
    name = models.CharField(default="", max_length=30, verbose_name="类别名", help_text="类别名")
    desc = models.TextField(default="", null=True, blank=True, verbose_name="类别描述", help_text="类别描述")
    type = models.IntegerField(choices=CLASS_TYPE, verbose_name="类目级别", help_text="类目级别")
    is_tab = models.BooleanField(default=False, verbose_name="是否导航", help_text="是否导航")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    def __str__(self):
        return "%s | %s" % (self.name, self.type)

    class Meta:
        db_table = "%scategory" % table_prefix
        app_label = 'tools'


class ToolsUrl(models.Model):
    name = models.CharField(default="", max_length=30, verbose_name="url名", help_text="url名")
    desc = models.TextField(default="", null=True, blank=True, verbose_name="url描述", help_text="url描述")
    url = models.URLField(default="", verbose_name="url", help_text="url")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    category = models.ForeignKey(ToolsCategory, on_delete=models.CASCADE, related_name='urls',verbose_name="url类别")

    def __str__(self):
        return '%s | %s | %s' % (self.name, self.url, self.category.name)

    class Meta:
        db_table = "%surl" % table_prefix
        app_label = 'tools'  # 指定要关联哪个数据库，该表会创建到指定的数据库

class ToolsView(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    desc = models.TextField(blank=True, null=True)
    url = models.CharField(max_length=200)
    category_id = models.IntegerField(blank=True, null=True)
    category_name = models.CharField(max_length=30, blank=True, null=True)
    parent_category_id = models.IntegerField(blank=True, null=True)
    parent_category_name = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'tools_view'
        app_label = 'tools'
