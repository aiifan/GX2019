from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
import random
import socket
import time
from .models import *

# Create your views here.
"""
账务账单管理
"""
# 账务账单列表显示
def account_list(request):
    users = User.objects.all()
    # 生成paginator对象,定义每页显示10条记录
    paginator = Paginator(users, 3)
    # 从前端获取当前的页码数,默认为1
    page = request.GET.get('page', 1)
    # 把当前的页码数转换成整数类型
    currentPage = int(page)
    try:
        print(page)
        users = paginator.page(page)  # 获取当前页码的记录
    except PageNotAnInteger:
        users = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        users = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
    return render(request, 'account/account_list.html', locals())

def ac_detail(request):
    nickname = request.POST.get('nickname')
    user = User.objects.get(nickname=nickname)
    user = {
        'nickname': user.nickname,
        'ident': user.ident,
        'osip': user.osip,
        'tel': user.tel,
        'account': user.account.account_id,
        'state': user.account.state,
        'prev_time': user.account.prev_time,
        'prev_ip': user.account.prev_ip,
        'birth': user.birth,
        'occupation':user.occupation,
        'sex': user.sex,
        'youbian': user.youbian,
        'addr': user.addr,
        'qq': user.qq
    }
    # user = serializers.serialize('json', user)
    # user = json.loads(user)
    return HttpResponse(json.dumps(user))
    # return render(request, 'account/account_detail.html', locals())
# 添加用户
def account_add(request):
    if request.method == 'POST':
        nickname = request.POST.get('name')
        ident = request.POST.get('shenfen')
        account_name = request.POST.get('osname')
        account_pwd = request.POST.get('ospwd')
        tel = request.POST.get('tel')
        birth = request.POST.get('birth')
        Email = request.POST.get('email')
        occupation = request.POST.get('zhiye')
        sex = request.POST.get('radSex')
        addr = request.POST.get('addr')
        youbian = request.POST.get('youbina')
        qq = request.POST.get('qq')
        state = '开通'
        state_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        create_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        prev_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        prev_ip = '127.0.0.1'
        account_id = yield_id()
        print(birth, prev_ip)
        Accounts(account_id=account_id, account_name=account_name, account_pwd=account_pwd,\
                 state=state, state_time=state_time, create_time=create_time,\
                 prev_time=prev_time, prev_ip=prev_ip).save()
        account = Accounts.objects.get(account_id=account_id)
        User(nickname=nickname, ident=ident, tel=tel, birth=birth, Email=Email, sex=sex, \
             occupation=occupation, addr=addr, youbian=youbian, qq=qq, osname=account_name,\
             ospwd=account_pwd, osip=prev_ip, account=account).save()
        msg = {'code': 200}
        return HttpResponse(json.dumps(msg))
    return render(request, 'account/account_add.html')
# 账务账单用户详细
def account_detail(request, nickname):
    user = User.objects.get(nickname=nickname)
    return render(request, 'account/account_detail.html', locals())

# 修改信息
def account_update(request, nickname):
    user = User.objects.get(nickname=nickname)
    return render(request, 'account/account_modi.html', locals())

def update(request):
    try:
        ident = request.POST.get('ident')
        nickname = request.POST.get('name')
        tel = request.POST.get('tel')
        Email = request.POST.get('email')
        occupation = request.POST.get('zhiye')
        addr = request.POST.get('addr')
        sex = request.POST.get('radSex')
        youbian = request.POST.get('youbian')
        qq = request.POST.get('qq')
        User.objects.filter(ident=ident).update(nickname=nickname, sex=sex, tel=tel, Email=Email, occupation=occupation,\
                                                addr=addr, youbian=youbian, qq=qq)
        msg = {'code': 200}
    except:
        msg = {'code': 400}
    return HttpResponse(json.dumps(msg))

# 更新状态
def update_code(request):
    try:
        nickname = request.POST.get('nickname')
        state = request.POST.get('state')
        if(state=='开通'):
            state='暂停'
        else:
            state='开通'
        user = User.objects.get(nickname=nickname)
        time1 = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        Accounts.objects.filter(account_id=user.account.account_id).update(state=state, state_time=time1)
        msg = {'code': 200, 'state': state, 'time': time1}
    except:
        msg = {'code': 400}
    return HttpResponse(json.dumps(msg))

# 删除
def delete_code(request):
    # try:
        nickname = request.POST.get('nickname')
        state = '删除'
        user = User.objects.get(nickname=nickname)
        time1 = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        Accounts.objects.filter(account_id=user.account.account_id).update(state=state, state_time=time1)
        # 更新所有该账务账号下的业务账号的状态
        business = Business.objects.all()
        for bus in business:
            if bus.user.nickname == nickname:
                print(111111111)
                bus.statue = state
                bus.save()
        msg = {'code': 200, 'time': time1}
    # except:
    #     msg = {'code': 400}
        return HttpResponse(json.dumps(msg))

# 查找
@csrf_exempt
def account_search(request):
    ident = request.POST.get('ident')
    nickname = request.POST.get('nickname')
    osname = request.POST.get('osname')
    state = request.POST.get('state')
    print(ident, nickname, osname, state)
    def get_dict(user):
        dict1 = {}
        dict1['id'] = user.id
        dict1['nickname'] = user.nickname
        dict1['ident'] = user.ident
        dict1['osname'] = user.osname
        dict1['state'] = user.account.state
        dict1['create_time'] = user.account.create_time
        dict1['prev_time'] = user.account.prev_time
        return dict1
    li = []
    if ident == '不验证' and nickname=='不验证' and osname=='不验证' and state != '全部':
        users = User.objects.all()
        for user in users:
            if user.account.state == state:
                dict1 = get_dict(user)
                li.append(dict1)
    elif ident != '不验证':
        user = User.objects.get(ident=ident)
        dict1 = get_dict(user)
        li.append(dict1)
    elif nickname != '不验证':
        user = User.objects.get(nickname=nickname)
        dict1 = get_dict(user)
        li.append(dict1)
    elif osname != '不验证':
        user = User.objects.get(osname=osname)
        dict1 = get_dict(user)
        li.append(dict1)
    msg = {'code': 200, 'users': li}
    return HttpResponse(json.dumps(msg))

# 生成账务账号id
def yield_id():
    a = random.randint(0,10)
    b = random.randint(0,10)
    c = random.randint(0,10)
    id = str(a)+str(b)+str(c)
    return id