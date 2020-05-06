from picm.models import PicmCategory, PicmPath
from rest_framework import serializers


class PicmCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PicmCategory
        fields = ['id','name', 'type', 'parent_category']
        # fields = '__all__'


class PicmPathSerializer(serializers.ModelSerializer):
    class Meta:
        model = PicmPath
        fields = '__all__'

class CategorysSerializer(serializers.ModelSerializer):
    paths = PicmPathSerializer(many=True)
    sub_cat = PicmCategorySerializer(many=True)
    parent_category=PicmCategorySerializer()
    class Meta:
        model = PicmCategory
        fields = ('id','name','type','parent_category','sub_cat','paths')