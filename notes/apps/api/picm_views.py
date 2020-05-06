from picm.models import PicmCategory, PicmPath
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from . import picm_serializers


class PicmCategoryViewSet(viewsets.ModelViewSet):
    queryset = PicmCategory.objects.all()
    serializer_class = picm_serializers.PicmCategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [OrderingFilter, SearchFilter]
    filter_fields = ['id']
    ordering_fields = ['id']


class PicmPathViewSet(viewsets.ModelViewSet):
    queryset = PicmPath.objects.all()
    serializer_class = picm_serializers.PicmPathSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [OrderingFilter, SearchFilter]
    filter_fields = ['id']
    ordering_fields = ['id']

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = PicmCategory.objects.all()
    serializer_class = picm_serializers.CategorysSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [OrderingFilter, SearchFilter]
    filter_fields = ['name','id']
    ordering_fields = ['id','name']