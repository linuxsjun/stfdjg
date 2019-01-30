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
from django.urls import path, include

from web import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.index),
    path('WW_verify_nHQMbL9kxBaRLdjd.txt', views.wxtext),
    path('favicon.ico', views.wxtext),

    path('asset_kanban_board/', views.asset_kanban_board),
    path('asset_config/', views.asset_config),

    path('pure_list/', views.view_pure_list),
    path('pure_form/', views.pure_form),
    path('pure_add/', views.pure_add),
    path('pure_del/', views.pure_del),

    path('search/', views.search),
    path('sub/', views.sub),

    path('sign/', views.sign_view),
    path('signout/', views.signout),

    path('conf/', views.config),
    path('gettoken/', views.getToken),

    path('hr/', views.hr_view),
    path('gethr/', views.gethr),

    path('dep/', views.dep_view),
    path('sync/', views.readdepartment),

    path('upload/', views.uploadfile),
    path('sendmsg/', views.sendmsg),

    path('wxdoor/', views.wxdoor),
    path('wxcode/', views.wxcode),

    path('property_list/', views.asset_property_list),
    path('asset_property_sub_board/', views.asset_property_sub_board),
    path('property_form/', views.asset_property_form),
    path('property_upload/', views.property_upload),
    path('property_output_cvs/', views.asset_property_list_output_cvs),

    path('parts_list/', views.asset_parts_list),
    path('parts_form/', views.asset_parts_form),

    path('category_list/', views.asset_category_list),
    path('category_form/', views.asset_category_form),

    path('applicant_list/', views.asset_applicant_list),

    path('allot_list/', views.asset_allot_list),

    path('importdata/', views.importdata),


    path('asset/', include('appasset.urls')),
    path('task/', include('task.urls')),
]

