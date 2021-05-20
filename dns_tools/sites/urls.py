from django.urls import path, include
from . import views

app_name='sites'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('menu/', views.zones_menu, name='menu'),
    path('rr_search/', views.rr_search, name='search'),
    path('rr_get/<int:id>/', views.rr_get, name='get'),
    path('zones/', views.zones, name='data'),
    path('rr_op/', views.rr_op, name='op'),
    path('rr_add/', views.rr_add, name='add'),
    path('rr_edit/<int:id>/', views.rr_edit, name='edit'),
    path('flush_rr/',views.flush_rr,name='flush'),
]
