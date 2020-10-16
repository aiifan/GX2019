from django.urls import path
from . import views


urlpatterns = [
    path('', views.save_server, name='save_server'),
    path('list/',views.lists, name='lists'),
    path('is_connet/',views.exists_connect, name='exists_connect'),
]
