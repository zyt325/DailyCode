from django.db import models
from datetime import datetime

table_prefix = 'picm_'


# Create your models here.

class PicmCategory(models.Model):
    CLASS_TYPE = ((1, "一级类目"), (2, "二级类目"), (3, "三级类目"),)
    name = models.CharField(default="", max_length=30, verbose_name="类别名", help_text="类别名")
    desc = models.TextField(default="", null=True, blank=True, verbose_name="类别描述", help_text="类别描述")
    type = models.IntegerField(choices=CLASS_TYPE, verbose_name="类目级别", help_text="类目级别")
    parent_category = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, verbose_name="父类目级别",
                                        related_name="sub_cat")
    is_tab = models.BooleanField(default=False, verbose_name="是否导航", help_text="是否导航")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    def __str__(self):
        return "%s %s %s" % (self.name, self.type, self.parent_category)

    class Meta:
        db_table = "%scategory" % table_prefix
        app_label = 'picm'


class PicmPath(models.Model):
    name = models.CharField(default="", unique=True, max_length=120, verbose_name="图片路径", help_text="图片路径")
    category = models.ForeignKey(PicmCategory, models.CASCADE, db_column='class_id', related_name="paths",
                                 verbose_name="图片类别")
    desc = models.TextField(default="", null=True, blank=True, verbose_name="图片描述", help_text="图片描述")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    def __str__(self):
        return "%s %s %s" % (self.id, self.name, self.add_time)

    class Meta:
        db_table = "%spath" % table_prefix
        app_label = 'picm'
