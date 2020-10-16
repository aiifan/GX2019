from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('report_list/', report_list, name='report_list'),
    re_path('report_list/(.*)/', report_list, name='report_list'),
]
