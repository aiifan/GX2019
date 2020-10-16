from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('service_list/', service_list, name='service_list'),
    re_path('service_list/([?=a-z0-10]*)', service_list, name='service_list'),
    path('service_detail/<id>/', service_detail, name='service_detail'),
    path('service_add/', service_add, name='service_add'),
    path('get_account/', get_account, name='get_account'),
    path('ser_add_run/', ser_add_run, name='ser_add_run'),
    path('service_update/<id>', service_update, name='service_update'),
    path('ser_update_run/', ser_update_run, name='ser_update_run'),
    path('ser_update_code/', ser_update_code, name='ser_update_code'),
    path('ser_delete_code/', ser_delete_code, name='ser_delete_code'),
    path('ser_search/', ser_search, name='ser_search'),
]
