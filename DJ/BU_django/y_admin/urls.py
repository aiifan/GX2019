"""y_project URL Configuration

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
from django.urls import path,re_path
from . import views

urlpatterns = [
    # 渲染页面路由
    path('show_login/', views.show_login, name="show_login"),
    path('show_index/', views.show_index, name="show_index"),
    path('user_info/', views.user_info, name="user_info"),
    path('user_pwd/', views.user_pwd, name="user_pwd"),
    path('role_list/', views.role_list, name="role_list"),
    path('role_add/', views.role_add, name="role_add"),
    path('role_modi/', views.role_modi, name="role_modi"),
    path('admin_add/', views.admin_add, name="admin_add"),
    path('admin_list/', views.admin_list, name="admin_list"),
    path('admin_modi/', views.admin_modi, name="admin_modi"),
    # 功能路由
    path('login_data/', views.login_data, name="login_data"),
    path('show_user/', views.show_user, name="show_user"),
    path('user_update/', views.user_update, name="user_update"),
    path('update_pwd/', views.update_pwd, name="update_pwd"),
    path('add_role/', views.add_role, name="add_role"),
    path('show_role/', views.show_role, name="show_role"),
    re_path('show_role/([?=a-z0-10]*)', views.show_role, name="show_role"),
    path('show_uprole/', views.show_uprole, name="show_uprole"),
    path('update_role/', views.update_role, name="update_role"),
    path('delete_role/', views.delete_role, name="delete_role"),
    path('add_admin/', views.add_admin, name="add_admin"),
    path('update_admin/', views.update_admin, name="update_admin"),
    path('show_admin/', views.show_admin, name="show_admin"),
    re_path('show_admin/([?=a-z0-10]*)', views.show_admin, name="show_admin"),
    path('show_upadmin/', views.show_upadmin, name="show_upadmin"),
    path('delete_admin/', views.delete_admin, name="delete_admin"),
    path('reset_pwd/', views.reset_pwd, name="reset_pwd"),
    path('search_admin/', views.search_admin, name="search_admin"),
]
