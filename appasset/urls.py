from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),

    path('assetlist/', views.assetlist),
    path('assetform/', views.assetform),
    path('assetappl/', views.assetappl),
    path('assetprolist/', views.assetprolist),
]