from django.urls import path
from . import views

app_name = 'stool'

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_record, name='add_record'),
    path('records/', views.records_list, name='records_list'),
    path('records/count/', views.records_count, name='records_count'),
    path('stats/', views.stool_stats, name='stool_stats'),
]
