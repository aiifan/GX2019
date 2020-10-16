from django.shortcuts import render
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from account.models import Accounts, User, Ball, Postage, Business, DetailBall

# Create your views here.
def bill_list(request):
    balls = Ball.objects.all()
    # 生成paginator对象,定义每页显示10条记录
    paginator = Paginator(balls, 3)
    # 从前端获取当前的页码数,默认为1
    page = request.GET.get('page', 1)
    # 把当前的页码数转换成整数类型
    currentPage = int(page)
    try:
        print(page)
        balls = paginator.page(page)  # 获取当前页码的记录
    except PageNotAnInteger:
        balls = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        balls = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
    return render(request, 'bill/bill_list.html', locals())

def bill_item(request,id):
    ball = Ball.objects.get(id=id)
    business = Business.objects.all()
    lis = []
    fee = 0
    for bus in business:
        if bus.user.id == ball.user.id:
            fee += bus.pay_cost
            lis.append(bus)

    # 生成paginator对象,定义每页显示10条记录
    paginator = Paginator(lis, 3)
    # 从前端获取当前的页码数,默认为1
    page = request.GET.get('page', 1)
    # 把当前的页码数转换成整数类型
    currentPage = int(page)
    try:
        print(page)
        lis = paginator.page(page)  # 获取当前页码的记录
    except PageNotAnInteger:
        lis = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        lis = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
    return render(request, 'bill/bill_item.html', locals())

def bill_service_detail(request, id):
    detail = DetailBall.objects.all()
    details = []
    fee = 0
    for det in detail:
        if str(det.business.id) == str(id):
            fee += det.fee
            details.append(det)
    def time(det):
        if det.business.create_time != '':
            year = det.business.create_time[0:4]
            month = det.business.create_time[5:7]
            if month[0] == '0':
                month = month[1]
            return year + '年' + month + '月'
        else:
            return ''
    if details:
        det = details[0]
        time = time(det)
    print(details)

    # 生成paginator对象,定义每页显示10条记录
    paginator = Paginator(details, 3)
    # 从前端获取当前的页码数,默认为1
    page = request.GET.get('page', 1)
    # 把当前的页码数转换成整数类型
    currentPage = int(page)
    try:
        print(page)
        details = paginator.page(page)  # 获取当前页码的记录
    except PageNotAnInteger:
        details = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        details = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
    return render(request, 'bill/bill_service_detail.html', locals())

@csrf_exempt
def bill_search(request):
    ident = request.POST.get('ident')
    account_name = request.POST.get('account_name')
    nickname = request.POST.get('nickname')
    year = request.POST.get('year')
    month = request.POST.get('month')
    def get_date(ball):
        date = ball.month.replace('年', '').replace('月', '')
        year = date[0:4]
        month = date[4:]
        return year, month
    def get_dict(ball):
        dict = {'id': ball.id, 'nickname': ball.user.nickname, 'ident': ball.user.ident, \
                'account_name': ball.user.account.account_name, 'cost': ball.cost, \
                'month': ball.month, 'pay_method': ball.pay_method, 'pay_code': ball.pay_code}
        return dict

    li_ball = []
    if ident != '':
        balls = Ball.objects.all()
        for ball in balls:
            ball_year, ball_month = get_date(ball)
            if month == '全部': # 根据身份信息和年份进行筛选
                if ball.user.ident == ident and ball_year == year:
                    dict = get_dict(ball)
                    li_ball.append(dict)
            else: # 根据身份信息和年份、月份进行筛选
                if ball.user.ident == ident and ball_year == year and ball_month == month:
                    dict = get_dict(ball)
                    li_ball.append(dict)
    elif ident == '' and account_name != '':
        balls = Ball.objects.all()
        for ball in balls:
            ball_year, ball_month = get_date(ball)
            if month == '全部':  # 根据身份信息和年份进行筛选
                if ball.user.account.account_name == account_name and ball_year == year:
                    dict = get_dict(ball)
                    li_ball.append(dict)
            else:  # 根据身份信息和年份、月份进行筛选
                if ball.user.account.account_name == account_name and ball_year == year and ball_month == month:
                    dict = get_dict(ball)
                    li_ball.append(dict)
    elif ident == '' and account_name == '' and nickname != '':
        balls = Ball.objects.all()
        for ball in balls:
            ball_year, ball_month = get_date(ball)
            if month == '全部':  # 根据身份信息和年份进行筛选
                if ball.user.nickname == nickname and ball_year == year:
                    dict = get_dict(ball)
                    li_ball.append(dict)
            else:  # 根据身份信息和年份、月份进行筛选
                if ball.user.nickname == nickname and ball_year == year and ball_month == month:
                    dict = get_dict(ball)
                    li_ball.append(dict)
    elif ident == '' and account_name == '' and nickname == '':
        balls = Ball.objects.all()
        for ball in balls:
            ball_year, ball_month = get_date(ball)
            if month == '全部':  # 根据身份信息和年份进行筛选
                if ball_year == year:
                    dict = get_dict(ball)
                    li_ball.append(dict)
            else:  # 根据身份信息和年份、月份进行筛选
                if ball_year == year and ball_month == month:
                    dict = get_dict(ball)
                    li_ball.append(dict)
    msg = {'code': 200, 'balls': li_ball}
    return HttpResponse(json.dumps(msg))

