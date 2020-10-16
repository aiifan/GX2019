from django.contrib import admin

from .models import Servers

# Register your models here.

@admin.register(Servers)
class ServersAdmin(admin.ModelAdmin):
    # 显示字段
    list_display = ("id", 'server_ip', 'server_port', 'server_user', 'server_pwd')
    # 满50条数据就自动分页
    list_per_page = 30
    # 后台数据列表排序方式
    ordering = ('id',)
    # 设置哪些字段可以点击进入编辑界面
    list_display_links = ('id', 'server_ip', 'server_port', 'server_user', 'server_pwd')