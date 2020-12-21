from note.models import NoteCategory, NoteArticle, NoteTheme
from rest_framework import viewsets, generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from .note_serializers import CategorySerializer, CategorysSerializer, Category_ArticleSerializer, \
    ThemeSerializer, ArticlesSerializer, ArticleSerializer


class ThemeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = NoteTheme.objects.all()
    serializer_class = ThemeSerializer
    pagination_class = LimitOffsetPagination


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = NoteCategory.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['id', 'type']


class CategorysViewSet(viewsets.ModelViewSet):
    queryset = NoteCategory.objects.all()
    serializer_class = CategorysSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['id', 'type']
    ordering_fields = ['id', 'name']



class ArticlesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = NoteArticle.objects.all()
    serializer_class = ArticlesSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend,SearchFilter]
    filter_fields = ['category']
    search_fields = ['title','body']

class ArticlesByTitleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = NoteArticle.objects.all()
    serializer_class = ArticlesSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend,SearchFilter]
    filter_fields = ['category']
    search_fields = ['title']

class Category_ArticleViewSet(viewsets.ModelViewSet):
    queryset = NoteCategory.objects.all()
    serializer_class = Category_ArticleSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['name', 'id']

class ArticleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = NoteArticle.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['id']
