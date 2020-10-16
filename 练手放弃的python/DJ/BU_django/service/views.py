from django.shortcuts import render
from django.http import HttpResponse
import time
import json
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from account.models import Accounts, User, Postage, Business

# Create your views here.

def service_list(request):
    business = Business.objects.all()
    paginator = Paginator(business, 3)
    # 从前端获取当前的页码数,默认为1
    page = request.GET.get('page', 1)
    # 把当前的页码数转换成整数类型
    currentPage = int(page)
    try:
        print(page)
        business = paginator.page(page)  # 获取当前页码的记录
    except PageNotAnInteger:
        business = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        business = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
    return render(request, 'service/service_list.html', locals())

def service_detail(request, id):
    business = Business.objects.get(id=id)
    return render(request, 'service/service_detail.html', locals())

def service_add(request):
    return render(request, 'service/service_add.html')

def get_account(request):
    ident = request.POST.get('ident')
    try:
        user = User.objects.get(ident=ident)
        account = user.account.account_name
        msg = {'code': 200, 'account':account}
    except:
        msg = {'code': 400}
    return HttpResponse(json.dumps(msg))

def ser_add_run(request):
    ident = request.POST.get('ident')
    account_name = request.POST.get('account')
    pg_type = request.POST.get('type')
    osname = request.POST.get('osname')
    ospwd = request.POST.get('ospwd')
    user = User.objects.get(ident=ident)
    if user.osname == osname and user.ospwd == ospwd:
        try:
            account = Accounts.objects.get(account_name=account_name)
            postage = Postage.objects.get(pg_type=pg_type)
            statue = '开通'
            create_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            pay_cost = 0
            time_length = 0
            Business(time_length=time_length, pay_cost=pay_cost, statue=statue, create_time=create_time,\
                     user=user, account=account, postage=postage).save()
            msg = {'code': 200}
        except:
            msg = {'code': 400, 'message': '保存失败，请重新尝试'}
    else:
        msg = {'code': 300, 'message': 'os账号错误，请重新输入'}
    return HttpResponse(json.dumps(msg))

# 更新
def service_update(request, id):
    bus = Business.objects.get(id=id)
    return render(request, 'service/service_modi.html', locals())

def ser_update_run(request):
    try:
        id = request.POST.get('bus')
        pg_type = request.POST.get('type')
        print(id)
        postage = Postage.objects.get(pg_type=pg_type)
        print(postage)

        Business.objects.filter(id=id).update(postage=postage)
        msg = {'code': 200}
    except:
        msg = {'code': 300, 'message': '保存失败'}
    return HttpResponse(json.dumps(msg))

# 状态转变
@csrf_exempt
def ser_update_code(request):
    state = request.POST.get('state')
    id = request.POST.get('id')
    if (state == '开通'):
        state = '暂停'
    else:
        state = '开通'
    try:
        Business.objects.filter(id=id).update(statue=state)
        msg = {'code': 200, 'state': state}
    except:
        msg = {'code': 300}
    return HttpResponse(json.dumps(msg))

# 状态删除
def ser_delete_code(request):
    id = request.POST.get('id')
    state = '删除'
    try:
        Business.objects.filter(id=id).update(statue=state)
        msg = {'code': 200}
    except:
        msg = {'code': 300}
    return HttpResponse(json.dumps(msg))

# 搜索
@csrf_exempt
def ser_search(request):
    ident = request.POST.get('ident')
    name = request.POST.get('name')
    osname = request.POST.get('osname')
    state = request.POST.get('state')
    print(ident, name, osname, state)

    def get_dict(bus):
        dict1 = {}
        dict1['id'] = bus.id
        dict1['account_id'] = bus.account.account_id
        dict1['ident'] = bus.user.ident
        dict1['nickname'] = bus.user.nickname
        dict1['osname'] = bus.user.osname
        dict1['statue'] = bus.statue
        dict1['osip'] = bus.user.osip
        dict1['postage'] = bus.postage.pg_name
        return dict1
    # try:
    li = []
    if ident == '' and name == '' and osname == '' and state != '全部':
        business = Business.objects.all()
        for bus in business:
            if bus.statue == state:
                dict1 = get_dict(bus)
                li.append(dict1)
    elif ident != '':
        print(1234567)
        user = User.objects.get(ident=ident)
        print(user)
        print(11111111111111)
        business = Business.objects.all()
        for bus in business:
            if(bus.user.nickname==user.nickname):
                dict1 = get_dict(bus)
                li.append(dict1)
    elif name != '':
        business = Business.objects.all()
        for bus in business:
            if (bus.user.osip == name):
                dict1 = get_dict(bus)
                li.append(dict1)
    elif osname != '':
        user = User.objects.get(osname=osname)
        business = Business.objects.all()
        for bus in business:
            print(bus.user)
            if (bus.user.nickname == user.nickname):
                dict1 = get_dict(bus)
                li.append(dict1)
    # except:
    #     li = []
    msg = {'code': 200, 'buss': li}
    return HttpResponse(json.dumps(msg))
