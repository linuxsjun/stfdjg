from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),

    path('hr/', views.hr_view),
    path('dep/', views.dep_view),

    path('gethr/', views.gethr),
    path('sync/', views.readdepartment),
]