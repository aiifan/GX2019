from django.contrib import admin
from . import models
# Register your models here.

@admin.register(models.Stu)
class StuAdmin(admin.ModelAdmin):
    # 显示字段
    list_display = ("id", 'stu_name', 'stu_sex')
    # 满50条数据就自动分页
    list_per_page = 30
    # 后台数据列表排序方式
    ordering = ('id',)
    # 设置哪些字段可以点击进入编辑界面
    list_display_links = ("id", 'stu_name', 'stu_sex')

@admin.register(models.Tea)
class TeaAdmin(admin.ModelAdmin):
    # 显示字段
    list_display = ("id", 'tea_name', 'tea_sex')
    # 满50条数据就自动分页
    list_per_page = 30
    # 后台数据列表排序方式
    ordering = ('id',)
    # 设置哪些字段可以点击进入编辑界面
    list_display_links = ("id", 'tea_name', 'tea_sex')

@admin.register(models.Course)
class CourseAdmin(admin.ModelAdmin):
    # 显示字段
    list_display = ("id", 'course_name')
    # 满50条数据就自动分页
    list_per_page = 30
    # 后台数据列表排序方式
    ordering = ('id',)
    # 设置哪些字段可以点击进入编辑界面
    list_display_links = ("id", 'course_name')

@admin.register(models.Cla)
class ClaAdmin(admin.ModelAdmin):
    # 显示字段
    list_display = ("id", 'cla_name')
    # 满50条数据就自动分页
    list_per_page = 30
    # 后台数据列表排序方式
    ordering = ('id',)
    # 设置哪些字段可以点击进入编辑界面
    list_display_links = ("id", 'cla_name')