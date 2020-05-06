from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('single_upload/', views.single_upload, name='single_upload'),
    path('mult_upload/', views.mult_upload, name='mult_upload'),
    path('vue_upload/', views.vue_upload, name='vue_upload'),
]
