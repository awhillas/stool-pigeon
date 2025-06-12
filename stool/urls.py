from django.urls import path
from . import views

app_name = 'stool'

urlpatterns = [
    path('', views.home, name='home'),
    path('stats/', views.stool_stats, name='stool_stats'),
]
