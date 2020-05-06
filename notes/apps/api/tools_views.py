from tools.models import ToolsCategory, ToolsUrl, ToolsView
from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from . import tools_serializers


class ToolsCategoryViewSet(viewsets.ModelViewSet):
    queryset = ToolsCategory.objects.all()
    serializer_class = tools_serializers.ToolsCategorySerializer
    pagination_class = LimitOffsetPagination


class ToolsUrlViewSet(viewsets.ModelViewSet):
    queryset = ToolsUrl.objects.all()
    serializer_class = tools_serializers.ToolsUrlSerializer
    pagination_class = LimitOffsetPagination


class ToolsViewViewSet(viewsets.ModelViewSet):
    queryset = ToolsView.objects.all()
    serializer_class = tools_serializers.ToolsViewSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [OrderingFilter, SearchFilter]
    filter_fields = ['category_name', 'parent_category_name']
    ordering_fields = ['category_name', 'category_id']
    search_fields = ['parent_category_name']


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = ToolsCategory.objects.all()
    serializer_class = tools_serializers.CategorysSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [OrderingFilter, SearchFilter]
    filter_fields = ['name', 'id']
    ordering_fields = ['id', 'name']


class UrlsViewSet(viewsets.ModelViewSet):
    queryset = ToolsUrl.objects.all()
    serializer_class = tools_serializers.UrlsSerializer
    pagination_class = LimitOffsetPagination
