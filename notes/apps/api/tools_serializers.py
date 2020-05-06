from tools.models import ToolsCategory, ToolsUrl, ToolsView
from rest_framework import serializers


# ModelSerializer , contain id
# HyperlinkedModelSerializer, not contain id

class ToolsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ToolsCategory
        fields = ['name', 'type', 'parent_category']
        # fields = '__all__'


class ToolsUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToolsUrl
        fields = ('name', 'url')
        # fields = '__all__'


class ToolsViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToolsView
        fields = '__all__'


class CategorysSerializer(serializers.ModelSerializer):
    urls = ToolsUrlSerializer(many=True)
    sub_cat = ToolsCategorySerializer(many=True)
    parent_category = ToolsCategorySerializer()

    class Meta:
        model = ToolsCategory
        fields = ('id', 'name', 'type', 'parent_category', 'sub_cat', 'urls')


class UrlsSerializer(serializers.ModelSerializer):
    category = ToolsCategorySerializer()

    class Meta:
        model = ToolsUrl
        fields = '__all__'
