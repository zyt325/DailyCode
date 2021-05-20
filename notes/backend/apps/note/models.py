from django.db import models
from django.utils import timezone

# Create your models here.
table_prefix = 'note_'


class NoteTheme(models.Model):
    name = models.CharField(default="", max_length=50, verbose_name="主题名", help_text="主题名")
    desc = models.TextField(default="", null=True, blank=True, verbose_name="主题描述", help_text="主题描述")
    add_time = models.DateTimeField(default=timezone.now, verbose_name="添加时间")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "%stheme" % table_prefix
        app_label = 'note'


class NoteCategory(models.Model):
    CLASS_TYPE = ((1, "一级类目"), (2, "二级类目"), (3, "三级类目"),)
    name = models.CharField(default="", max_length=50, verbose_name="类名", help_text="类别名")
    desc = models.TextField(default="", null=True, blank=True, verbose_name="类别描述", help_text="类别描述")
    type = models.IntegerField(choices=CLASS_TYPE, verbose_name="类目级别", help_text="类目级别")
    parent_category = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, verbose_name="父类目级别",
                                        related_name="sub_cat")
    add_time = models.DateTimeField(default=timezone.now, verbose_name="添加时间")

    def __str__(self):
        return "%s %s" % (self.name, self.type)

    class Meta:
        db_table = "%sclass" % table_prefix
        app_label = 'note'


class NoteArticle(models.Model):
    title = models.CharField(default="", unique=True, max_length=50, verbose_name="标题", help_text="标题")
    body = models.TextField(default="", blank=True, null=True, verbose_name="内容", help_text="内容")
    file_name = models.CharField(default="", unique=True, max_length=25, verbose_name="文件名", help_text="文件名")
    create_at = models.DateTimeField(default=timezone.now, verbose_name="创建时间")
    category = models.ForeignKey(NoteCategory, models.CASCADE, db_column='class_id',
                                 related_name="articles",
                                 verbose_name="文章分类")  # Field renamed because it was a Python reserved word.
    def __str__(self):
        return "%s %s %s" % (self.title, self.file_name, self.category)

    class Meta:
        db_table = "%sarticle" % table_prefix
        app_label = 'note'

# 
# class NoteArticleBak(models.Model):
#     title = models.CharField(max_length=50)
#     body = models.TextField(blank=True, null=True)
#     file_name = models.CharField(max_length=25)
#     create_at = models.DateTimeField()
#
#     class Meta:
#         managed = False
#         db_table = "%sarticle_bak" % table_prefix
#         app_label = 'note'

class NoteMapArticleTheme(models.Model):
    theme = models.ForeignKey(NoteTheme, models.CASCADE, db_column = 'theme_id', verbose_name = "主题", null = True)
    article = models.ForeignKey(NoteArticle, models.CASCADE,db_column='article_id', verbose_name="文章",
                              null=True)
    def __str__(self):
        return "%s %s" % (self.theme, self.article)

    class Meta:
        db_table = "%sMapArticleTheme" % table_prefix
        app_label = 'note'
        unique_together = (('article', 'theme'),)

# class NoteArticleView(models.Model):
#     article_id = models.IntegerField(primary_key=True)
#     body = models.TextField(blank=True, null=True)
#     class_id = models.IntegerField(blank=True, null=True)
#     file_name = models.CharField(max_length=25)
#     article_name = models.CharField(max_length=50)
#     class_name = models.CharField(max_length=50, blank=True, null=True)
#     upper_class = models.IntegerField(blank=True, null=True)
#
#     class Meta:
#         managed = False  # Created from a view. Don't remove.
#         db_table = "%sarticle_view" % table_prefix
#         app_label = 'note'
