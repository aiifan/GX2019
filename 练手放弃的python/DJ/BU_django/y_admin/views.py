from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json

# 渲染登录页面
def show_login(request):
    return render(request, 'y_app1/login.html')
# 渲染主页面
def show_index(request):
    return render(request, 'y_app1/index.html')
# 渲染个人信息页面
def user_info(request):
    return render(request, 'y_app1/user_info.html')
# 渲染密码修改页面
def user_pwd(request):
    return render(request, 'y_app1/user_pwd.html')
# 渲染角色管理页面
def role_list(request):
    return render(request, 'y_app1/role_list.html')
# 渲染角色添加页面
def role_add(request):
    return render(request, 'y_app1/role_add.html')
# 渲染角色修改页面
def role_modi(request):
    return render(request, 'y_app1/role_modi.html')
# 渲染管理员添加页面
def admin_add(request):
    return render(request, 'y_app1/admin_add.html')
# 渲染管理员显示页面
def admin_list(request):
    return render(request, 'y_app1/admin_list.html')
# 渲染管理员修改信息页面
def admin_modi(request):
    return render(request, 'y_app1/admin_modi.html')



# 定义函数完成登录验证功能
@csrf_exempt
def login_data(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    codex = request.POST.get('codex')
    code = request.POST.get('code')
    res = Superadmin.objects.filter(username=username)
    obj = None
    for item in res:
        obj = item
    if obj is None:
        msg = {'code':400, 'error':'该管理员账号不存在'}
    else:
        if obj.password != password:
            msg = {'code': 300, 'error': '密码错误,请重新输入'}
        else:
            if codex=='':
                msg = {'code':401, 'error':'*请输入验证码'}
            elif codex!=code:
                msg = {'code':402, 'error':'*验证码错误,请重新输入'}
            else:
                msg = {'code': 200, 'error': '', 'user': username, 'role': obj.role}
    return HttpResponse(json.dumps(msg))

# 定义函数完成个人信息查看
@csrf_exempt
def show_user(request):
    username = request.POST.get('user')
    res = Superadmin.objects.filter(username=username)
    for obj in res:
        dic = {'username':obj.username,'role':obj.role,'nickname':obj.nickname,'phone':obj.phone,'email':obj.email,'ctime':obj.ctime}
        msg = {'code':200, 'infor':dic}
    return HttpResponse(json.dumps(msg))

# 定义函数完成个人信息修改
@csrf_exempt
def user_update(request):
    username = request.POST.get('user')
    new_nick = request.POST.get('nickname')
    new_phone = request.POST.get('phone')
    new_email = request.POST.get('email')
    res = Superadmin.objects.filter(username=username)
    for obj in res:
        obj.nickname = new_nick
        obj.phone = new_phone
        obj.email = new_email
        obj.save()
        msg = {'code':200, 'error':'', 'success':'修改成功'}
    return HttpResponse(json.dumps(msg))

# 定义函数完成密码页面修改
def update_pwd(request):
    old_pwd = request.POST.get('old_pwd')
    new_pwd = request.POST.get('new_pwd')
    new_pwd1 = request.POST.get('new_pwd1')
    res = Superadmin.objects.filter(password=old_pwd)
    obj = None
    for item in res:
        obj = item
    if obj is None:
        msg = {'code':400, 'error':'密码不存在,请重新输入'}
    else:
        if new_pwd == new_pwd1:
            obj.password = new_pwd
            obj.save()
            msg = {'code':200, 'error':'', 'success':'密码修改成功'}
        else:
            msg = {'code':300, 'error':'新密码两次输入不一致'}
    return HttpResponse(json.dumps(msg))

# 定义函数完成角色管理显示
def show_role(request):
    # 获取所有数据
    roles = Rolemanage.objects.all()
    # 生成paginator对象,定义每页显示10条记录
    paginator = Paginator(roles, 3)
    # 从前端获取当前的页码数,默认为1
    page = request.GET.get('page',1)
    # 把当前的页码数转换成整数类型
    currentPage = int(page)
    try:
        roles = paginator.page(page) # 获取当前页码的记录
    except PageNotAnInteger:
        roles = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        roles = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
    return render(request,'y_app1/role_list.html',locals())

# 定义函数完成角色管理添加
@csrf_exempt
def add_role(request):
    rolename = request.POST.get('rolename')
    power = request.POST.get('power')
    res = Rolemanage.objects.filter(rolename=rolename)
    obj = None
    for item in res:
        obj = item
    if obj is not None:
        msg = {'code':400, 'error':'角色名称已存在,请重新命名'}
    else:
        rolenamage = Rolemanage(rolename=rolename,power=power)
        rolenamage.save()
        msg = {'code':200, 'error':'', 'success':'角色创建成功'}
    return HttpResponse(json.dumps(msg))

#定义函数完成角色信息修改页面对应显示
@csrf_exempt
def show_uprole(request):
    roleid = request.POST.get('roleid')
    res = Rolemanage.objects.filter(roleid=roleid)
    for obj in res:
        dic = {'rolename': obj.rolename, 'power': obj.power}
        msg = {'code': 200, 'infor': dic}
    return HttpResponse(json.dumps(msg))

#定义函数完成角色信息修改
@csrf_exempt
def update_role(request):
    rolename = request.POST.get('rolename')
    power = request.POST.get('power')
    res1 = Superadmin.objects.filter(customrole=rolename)
    res = Rolemanage.objects.filter(rolename=rolename)
    obj = None
    obj1 = None
    for item1 in res1:
        obj1 = item1
    for item in res:
        obj = item
    if obj is None:
        msg = {'code': 400, 'error': '角色名称不存在,请重新输入'}
    else:
        obj.rolename = rolename
        obj.power = power
        obj.save()
        obj1.role = power
        obj1.save()
        msg = {'code': 200, 'error': '', 'success': '修改信息成功,下次登录时生效'}
    return HttpResponse(json.dumps(msg))

# 定义角色信息删除
@csrf_exempt
def delete_role(request):
    roleid = request.POST.get('roleid')
    res = Rolemanage.objects.filter(roleid=roleid)
    for obj in res:
        obj.delete()
        msg = {'code':'200', 'success':'删除成功'}
    return HttpResponse(json.dumps(msg))

# 定义函数完成管理员添加
@csrf_exempt
def add_admin(request):
    username = request.POST.get('username')
    nickname = request.POST.get('nickname')
    ctime = request.POST.get('ctime')
    password = request.POST.get('password')
    password1 = request.POST.get('password1')
    phone = request.POST.get('phone')
    email = request.POST.get('email')
    myrole = request.POST.get('myrole')
    res = Superadmin.objects.filter(username=username)
    res1 = Superadmin.objects.filter(phone=phone)
    res3 = Rolemanage.objects.filter(rolename=myrole)
    obj = None
    obj1 = None
    obj3 = None
    for item in res:
        obj = item
    for item1 in res1:
        obj1 = item1
    for item3 in res3:
        obj3 = item3
    if obj is not None:
        msg = {'code':400, 'error':'用户名已存在,请重新输入'}
    else:
        if password!=password1:
            msg = {'code':402, 'error':'密码两次输入不一致,请重新输入'}
        else:
            if obj1 is not None:
                msg = {'code': 401, 'error': '手机号已注册,请重新输入'}
            else:
                if obj3 is not None:
                    role1 = obj3.power
                    superuser1 = Superadmin(username=username, nickname=nickname, password=password, phone=phone,email=email, role=role1, ctime=ctime,customrole=myrole)
                    superuser1.save()
                    msg = {'code': 200, 'error': '', 'success': '注册成功'}
                else:
                    msg = {'code':403, 'error':'角色不存在'}
    return HttpResponse(json.dumps(msg))

# 定义函数完成管理员信息操作页面
@csrf_exempt
def show_admin(request):
    admins = Superadmin.objects.all()
    paginator = Paginator(admins, 3)
    page = request.GET.get('page', 1)
    currentPage = int(page)
    try:
        admins = paginator.page(page)
    except PageNotAnInteger:
        admins = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        admins = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
    return render(request, 'y_app1/admin_list.html', locals())

# 定义函数完成管理员信息修改页面显示信息
@csrf_exempt
def show_upadmin(request):
    adminid = request.POST.get('adminid')
    res = Superadmin.objects.filter(adminid=adminid)
    for obj in res:
        dic = {'nickname':obj.nickname,'username':obj.username,'phone':obj.phone,'email':obj.email,'customrole':obj.customrole}
        msg = {'code':200, 'infor':dic}
    return HttpResponse(json.dumps(msg))

# 定义函数完成管理员信息修改
@csrf_exempt
def update_admin(request):
    usrname = request.POST.get('username')
    nickname = request.POST.get('nickname')
    phone = request.POST.get('phone')
    email = request.POST.get('email')
    myrole = request.POST.get('myrole')
    res = Superadmin.objects.filter(phone=phone)
    res1 = Rolemanage.objects.filter(rolename=myrole)
    res2 = Superadmin.objects.filter(username=usrname)
    obj = None
    obj1 = None
    for item in res:
        obj = item
    for item1 in res1:
        obj1 = item1
    if obj is None or obj in res:
        if obj1 is not None:
            for obj2 in res2:
                obj2.nickname=nickname
                obj2.phone = phone
                obj2.email = email
                obj2.customrole = myrole
                obj2.save()
                msg = {'code': 200, 'error': '', 'success': '修改成功'}
        else:
            msg = {'code': 402, 'error':'角色名称不存在'}
    else:
        msg = {'code': 401, 'error': '手机号已注册,请重新输入'}
    return HttpResponse(json.dumps(msg))

# 定义函数完成管理员页面删除功能
@csrf_exempt
def delete_admin(request):
    adminid = request.POST.get('adminid')
    res = Superadmin.objects.filter(adminid=adminid)
    for obj in res:
        obj.delete()
        msg = {'code':200, 'success':'删除成功'}
    return HttpResponse(json.dumps(msg))

# 定义函数完成密码重置功能
@csrf_exempt
def reset_pwd(request):
    adminid = request.POST.get('adminid')
    res = Superadmin.objects.filter(adminid=adminid)
    obj = None
    for item in res:
        obj = item
    if obj is not None:
        obj.password = 123
        obj.save()
        msg = {'code':200, 'success':'密码重置成功'}
    else:
        msg = {'code': 400, 'error': '请选择起码一条数据'}
    return HttpResponse(json.dumps(msg))

# 定义函数完成搜索数据
@csrf_exempt
def search_admin(request):
    power = request.POST.get('power')
    customrole = request.POST.get('customrole')
    res = Superadmin.objects.filter(customrole=customrole)
    res1 = Superadmin.objects.all()
    ad_list=[]
    obj = None
    msg = {'code': 200, 'info': []}
    if (power!='全部' and customrole=='') or (power!='全部' and customrole!=''):
        for obj1 in res1:
            obj7 = obj1
            obj1 = obj1.role.split(',')
            if power in obj1:
                dic = {'adminid':obj7.adminid,'nickname':obj7.nickname,'username':obj7.username,'phone':obj7.phone,'email':obj7.email,'ctime':obj7.ctime,'customrole':obj7.customrole}
                ad_list.append(dic)
                msg = {'code':200, 'info':ad_list}
            else:
                dic = {'adminid': '', 'nickname': '', 'username': '',
                       'phone': '', 'email': '', 'ctime': '', 'customrole': ''}
                ad_list.append(dic)
                ad_list.pop()
                msg = {'code': 200, 'info': ad_list}
    elif power=='全部' and customrole!='':
        for item in res:
            obj = item
            if obj is None:
                msg = {'code':400, 'error':'指定数据不存在'}
            else:
                dic = {'adminid': obj.adminid, 'nickname': obj.nickname, 'username': obj.username,'phone': obj.phone, 'email': obj.email, 'ctime': obj.ctime, 'customrole': obj.customrole}
                ad_list.append(dic)
                msg = {'code':200, 'info':ad_list}
    else:
        msg = {'code':401, 'info':'不操作搜索'}
    return HttpResponse(json.dumps(msg))
