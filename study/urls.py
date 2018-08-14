"""study URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from web import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.index, name='index'),

    path('pure_list/', views.view_pure_list),

    path('search/', views.search),
    path('search_form/', views.search_form),

    path('conf/', views.config),
    path('gettoken/', views.getToken),

    path('view/', views.hr_view),
    path('sync/', views.readdepartment),
    # path('sync/', views.readdepartment),
]
