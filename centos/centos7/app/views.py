from django.shortcuts import render, redirect,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from . import form
from . import models

import paramiko

import json
# Create your views here.


def connect_ssh(ipaddr, user, password, cmd, port=22):
    '''
    判断服务器是否可以正常连接
    '''
    sshclient = paramiko.SSHClient()
    sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        sshclient.connect(ipaddr, port, user, password,timeout=10)
    except:
        return '连接失败'
    stdin,stdout,stderr = sshclient.exec_command(cmd)
    try:
        if stdout.channel.recv_exit_status() != 0:
            return stderr.read().decode('utf8')
        else:
            return stdout.read().decode('utf8')
    finally:
        sshclient.close()

def save_server(request):
    if request.method == 'POST':
        server_form = form.serverform(request.POST)
        message = "请检查输入"
        if server_form.is_valid():
            serverip = server_form.cleaned_data.get('serverip')
            serveruser = server_form.cleaned_data.get('serveruser')
            serverport = server_form.cleaned_data.get('serverport')
            serverpwd = server_form.cleaned_data.get('serverpwd')
            # ip = get_object_or_404(models.Servers, server_ip=serverip)
            obj = models.Servers.objects.filter(server_ip=serverip,server_user=serveruser)
            try:
                ip = obj[0].server_ip
            except IndexError:
                models.Servers.objects.create(server_ip=serverip,server_port=serverport,server_user=serveruser,server_pwd=serverpwd)
                return redirect('lists')
            if ip is not None:
                message = "该ip及用户已存在表中"
                return render(request, 'index.html', locals())
        return render(request, 'index.html', locals())
    elif request.method == 'GET':
        server_form = form.serverform()
        return render(request, 'index.html', locals())

def lists(request):
    obj = models.Servers.objects.all()
    return render(request, 'list.html', locals())

@csrf_exempt
def exists_connect(request):
    serverid = request.POST.get('serverid')
    obj = models.Servers.objects.filter(pk=serverid)
    serverip = obj[0].server_ip
    serverport = obj[0].server_port
    serveruser = obj[0].server_user
    serverpwd = obj[0].server_pwd
    result = connect_ssh(serverip,serveruser,serverpwd,'uname',serverport)
    print(result)
    if result.strip('\n')  == 'Linux':
        message = {'code':200, 'infor':'是linux'}
        # return HttpResponse(json.dumps(message))
    elif result == '连接失败':
        message = {'code':500, 'infor':'未成功连接服务器，请检查服务器地址是否正确'}
    else:
        message = {'code':501, 'infor':'不是linux'}
    return HttpResponse(json.dumps(message))
    


