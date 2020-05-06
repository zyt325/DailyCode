from django.urls import path, include
from . import views

urlpatterns = [
    # path('', views.index, name='index_article'),
    path('add/', views.add_article, name='add_article'),
    path('edit/', views.edit_article, name='edit_article'),
    # path('list/', views.list_article, name='list_article'),
    path('upload/', views.upload_file, name='upload_article'),
    # path('get/', views.get_article, name='get_article'),
    # path('v2/',views.v2,name='v2'),
]
