from note.models import NoteCategory, NoteArticle, NoteTheme
from rest_framework import serializers


# ModelSerializer , contain id
# HyperlinkedModelSerializer, not contain id
class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoteTheme
        # fields = ['id','class_name', 'upper_level']
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NoteCategory
        fields = ['id', 'name', 'type', 'parent_category', ]
        # fields = '__all__'


class CategorysSerializer(serializers.ModelSerializer):
    name = NoteCategory
    sub_cat = CategorySerializer(many=True)
    parent_category = CategorySerializer()

    class Meta:
        model = NoteCategory
        # fields = '__all__'
        fields = ('id', 'name', 'type', 'parent_category', 'sub_cat', 'name')




class ArticlesSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoteArticle
        fields = ['id', 'title', 'file_name']
        # fields = '__all__'

class Category_ArticleSerializer(serializers.ModelSerializer):
    articles = ArticlesSerializer(many=True)
    sub_cat = CategorySerializer(many=True)
    parent_category = CategorySerializer()

    class Meta:
        model = NoteCategory
        # fields = '__all__'
        fields = ('id', 'name', 'type', 'parent_category', 'sub_cat', 'articles')


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoteArticle
        fields = '__all__'
