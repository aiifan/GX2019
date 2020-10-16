from django.contrib import admin
from . import models
# Register your models here.

@admin.register(models.Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'title', 'tui', 'user', 'views', 'created_time')
    # 文章列表里显示想要显示的字段
    list_per_page = 50
    # 满50条数据就自动分页
    ordering = ('-created_time',)
    #后台数据列表排序方式
    list_display_links = ('id', 'title')
    # 设置哪些字段可以点击进入编辑界面

@admin.register(models.Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('id', 'text_info', 'img', 'link_url', 'is_active')

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'index')

@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(models.Tui)
class TuiAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(models.Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','linkurl')