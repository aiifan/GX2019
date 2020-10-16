from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from account.models import Accounts, User, Ball, Postage, Business, DetailBall

# Create your views here.
def report_list(request):
    balls_desc = Ball.objects.all().order_by('time_length')[:3]
    buss = Business.objects.all()
    users = User.objects.all()
    lis = []
    for user in users:
        taocan = 0
        baoyue = 0
        jishi = 0
        for bus in buss:
            if bus.user.id == user.id:
                if bus.postage.pg_type == '包月':
                    baoyue += 1
                if bus.postage.pg_type == '套餐':
                    taocan += 1
                if bus.postage.pg_type == '计时':
                    jishi += 1
        dict1 = {'ip': user.osip, 'taocan': taocan, 'baoyue': baoyue, 'jishi': jishi}
        lis.append(dict1)

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

    return render(request, 'report/report_list.html', locals())
