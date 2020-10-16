from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
# Create your views here.

from .form import NameForm



def login(request):
    if request.method == 'POST':
        login_form = NameForm(request.POST)
        message = '检查填写内容'
        if login_form.is_valid():
            name = login_form.changed_data.get('name')
            passwd = login_form.changed_data.get('passwd')
            try:
                user = User.objects.get(name=name)
            except:
                message = '用户不村子啊'
                return render(request, 'users/login.html', locals())
            if user.password == passwd:
                return redirect('/index/')
            else:
                message = '密码不正确！'
                return render(request, 'users/login.html', locals())
        else:
            return render(request, 'users/login.html', locals())

    login_form = NameForm()
    return render(request, 'users/login.html', locals())