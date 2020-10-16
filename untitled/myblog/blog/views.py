from django.shortcuts import render
from .models import Category
# Create your views here.

# def index(request):
#     sitename = 'Django中文网'
#     url = 'www.django.cn'
#     list = [
#         '开发前的准备',
#         "项目需求分析",
#         "数据库设计分析",
#         "创建项目",
#         "基础配置",
#         "欢迎页面",
#         "创建数据库模型"
#     ]
#     mydict={
#         'name': '吴秀峰',
#         'qq': '445813',
#         'wx': 'vipdjango',
#         'email': '445813@qq.com',
#         'Q群': '10218442',
#     }
#     context = {
#         'sitename': sitename,
#         "url": url,
#         "list": list,
#         "mydict": mydict
#     }
#     return render(request, 'index.html', context)

def index(request):
    allcategory = Category.objects.all()
    context = {
        'allcategory': allcategory
    }
    return render(request, 'index.html',context)
