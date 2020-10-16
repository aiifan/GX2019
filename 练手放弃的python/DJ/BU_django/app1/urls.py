from django.urls import path,re_path
from .import views
urlpatterns = [
    path('fee_list_app1/',views.fee_list, name='fl'),
    re_path('fee_list_app1/([?=a-z0-10]*)', views.fee_list, name="fl"),
    path('fee_add_app1/',views.fee_add, name='fa'),
    path('fee_modi_app1/<id>/',views.fee_modi, name='fm'),
    path('fee_detail_app1/<id>/',views.fee_detail, name='fd'),
    path('add_app1/',views.pg_Add, name='pg_add'),
    path('fee_list/',views.fee_list,name='fee_list'),
    path('updata_pg_Add/', views.updata_pg_Add, name='updata_pg_Add'),
    path('del_id/',views.del_id,name='del_id'),
    path('usetime_id/',views.usetime_id,name ='usetime_id'),
    path('jifei_sort_desc/',views.jifei_sort_desc, name='jifei_sort_desc'),
    path('jifei_sort_asc/', views.jifei_sort_asc, name='jifei_sort_asc'),
    path('shichang_sort_desc/',views.shichang_sort_desc, name='shichang_sort_desc'),
    path('shichang_sort_asc/', views.shichang_sort_asc, name='shichang_sort_asc'),

]
