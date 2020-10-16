from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('bill_list/', bill_list, name='bill_list'),
    re_path('bill_list/(.*)/', bill_list, name='bill_list'),
    path('bill_item/<id>/', bill_item, name='bill_item'),
    path('bill_service_detail/<id>/', bill_service_detail, name='bill_service_detail'),
    path('bill_search/', bill_search, name='bill_search'),
]
