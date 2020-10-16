from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import time
import os
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from account.models import Accounts, User, Ball, Postage, Business, DetailBall
# Create your views here.
# 完成资费管理页面的渲染
def fee_list(request):
    return render(request,'app1/fee_list.html')
#完成资费添加页面的渲染
def fee_add(request):
    return render(request,'app1/fee_add.html')
#完成资费管理修改的渲染
def fee_modi(request,id):
    poss = Postage.objects.get(id=id)
    return render(request,'app1/fee_modi.html',locals())
#完成资费detail的渲染
def fee_detail(request, id):
    pos = Postage.objects.get(id=id)
    return render(request,'app1/fee_detail.html',locals())

#定义增加内容功能
@csrf_exempt
def pg_Add(request):
    # 获取增加的内容
    pg_name = request.POST.get('pg_name')
    pg_type = request.POST.get('pg_type')
    base_length = request.POST.get('base_length')
    base_cost = request.POST.get('base_cost')
    company_cost = request.POST.get('company_cost')
    pg_explain = request.POST.get('pg_explain')
    pg_code = '暂停'
    create_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    res = Postage.objects.filter(pg_name=pg_name)
    print(pg_type)
    if res:
        msg = {'code': 400, 'infor': '业务名已存在，请重新你输入'}
    else:
        if base_length != '':
            base_length = int(base_length)
        else:
            base_length = 0
        if base_cost != '':
            base_cost = int(base_cost)
        else:
            base_cost = 0
        Postage(pg_name=pg_name, pg_type=pg_type, base_length=base_length, base_cost=base_cost,
                company_cost=company_cost, pg_explain=pg_explain, pg_code=pg_code, create_time=create_time).save()
        msg = {'code': 200, 'pg_type': pg_type}

    return HttpResponse(json.dumps(msg))

#定义修改更新内容
@csrf_exempt
def updata_pg_Add(request):
    pg_id = request.POST.get('id')
    pg_name = request.POST.get('pg_name')
    pg_type = request.POST.get('pg_type')
    base_length = request.POST.get('base_length')
    base_cost = request.POST.get('base_cost')
    company_cost = request.POST.get('company_cost')
    pg_explain = request.POST.get('pg_explain')
    try:
        if base_length != '':
            base_length = int(base_length)
        else:
            base_length = 0
        if base_cost != '':
            base_cost = int(base_cost)
        else:
            base_cost = 0
        Postage.objects.filter(id=pg_id).update(pg_name=pg_name, pg_type=pg_type, base_length=base_length, base_cost=base_cost, company_cost=company_cost,pg_explain=pg_explain)
        msg = {'code': 200}
    except:
        msg = {'code': 400}
    return HttpResponse(json.dumps(msg))


#完成删除操作
@csrf_exempt
def del_id(request):
    id = request.POST.get('id')
    pg_code = '删除'
    try:
        Postage.objects.filter(id=id).update(pg_code=pg_code)
        msg = {'code': 200}
    except:
        msg = {'code': 300}
    return HttpResponse(json.dumps(msg))

#完成启用操作
@csrf_exempt
def usetime_id(request):
    id = request.POST.get('id')
    use_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    pg_code = '开通'
    try:
        Postage.objects.filter(id=id).update(use_time=use_time,pg_code=pg_code)
        msg = {'code':200}
    except:
        pass
    return HttpResponse(json.dumps(msg))


#完成资费页面的渲染
def fee_list(request):
    date = Postage.objects.all()
    # 生成paginator对象,定义每页显示10条记录
    paginator = Paginator(date, 3)
    # 从前端获取当前的页码数,默认为1
    page = request.GET.get('page', 1)
    # 把当前的页码数转换成整数类型
    currentPage = int(page)
    try:
        print(page)
        date = paginator.page(page)  # 获取当前页码的记录
    except PageNotAnInteger:
        date = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        date = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
    return render(request, 'app1/fee_list.html', locals())


#基费升序降序
def jifei_sort_desc(request):
    date = Postage.objects.all().order_by('-base_cost')
    return render(request, 'app1/sec.html', locals())

def jifei_sort_asc(request):
    date = Postage.objects.all().order_by('base_cost')
    return render(request, 'app1/sec.html', locals())

#时长升序降序
def shichang_sort_desc(request):
    date = Postage.objects.all().order_by('-base_length')
    return render(request, 'app1/sec.html', locals())

def shichang_sort_asc(request):
    date = Postage.objects.all().order_by('base_length')
    return render(request, 'app1/sec.html', locals())

