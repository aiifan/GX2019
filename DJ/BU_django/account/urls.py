from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('account_list/', account_list, name='account_list'),
    re_path('account_list/([?=a-z0-10]*)', account_list, name='account_list'),
    path('ac_detail/', ac_detail, name='ac_detail'),
    path('detail/<nickname>', account_detail, name='account_detail'),
    path('account_add/', account_add, name='account_add'),
    path('account_update/<nickname>', account_update, name='account_update'),
    path('update/', update, name='update'),
    path('update_code/', update_code, name='update_code'),
    path('delete_code/', delete_code, name='delete_code'),
    path('account_search/', account_search, name='account_search'),
]
