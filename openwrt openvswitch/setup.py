#!/usr/bin/env python
# encoding:utf8

from __future__ import print_function

import os
import sys
import shutil
import subprocess
import tarfile


RED = "\033[1;31m"           # 红色
GREEN = '\033[0;32m'         # 绿色
YELLOW = '\033[0;33m'        # 黄色
BLUE = "\033[0;34m"          # 蓝色
PURPLISHRED = "\033[0;35m"   # 紫红色
SKYBLUE = '\033[0;36m'       # 天蓝色
PLAIN = '\033[0m'            # 默认

def print_red(content):
    print(RED,content,PLAIN)         # 红色
def print_green(content): 
    print(GREEN,content,PLAIN)       # 绿色
def print_yellow(content):
    print(YELLOW,content,PLAIN)      # 黄色
def print_blue(content):
    print(BLUE,content,PLAIN)        # 蓝色
def print_purplishred(content):
    print(PURPLISHRED,content,PLAIN) # 紫红色
def print_skyblue(content):
    print(SKYBLUE,content,PLAIN)     # 天蓝色



def exists_root():
    if os.getuid() != 0:
        print_red("请使用root用户执行该脚本！")
        sys.exit(1)
    print_green("检测到用户是root用户，开始执行安装脚本")
    return None

# 解压,返回解压文件夹
def un_tgz(file_name):
    un_path = os.path.join(os.getcwd(),file_name.split('.')[0])
    exists_dir(un_path)
    with tarfile.open(file_name, "r:gz") as f:
        for i in f:
            f.extract(i.name, os.getcwd())
    print_blue("{}解压完成".format(file_name))
    return un_path

# 检查文件夹是否存在,存在即删除
def exists_dir(dir_name):
    if os.path.exists(dir_name):
        shutil.rmtree(dir_name)
        print_purplishred('{}已存在,删除'.format(dir_name))
    else:
        print_yellow("{}不存在,无需删除".format(dir_name))

# 移动程序包
def move_dir(un_dir_name):
    wifihunter_dir = os.path.join(os.environ['HOME'],'WifiHunter')
    exists_dir(wifihunter_dir)
    shutil.move(os.path.join(un_dir_name,'WifiHunter'), os.environ['HOME'])
    print_skyblue('WifiHunter已放置在/root目录')
    html_dir = '/usr/share/nginx/html'
    exists_dir(html_dir)
    shutil.move(os.path.join(un_dir_name,'www'), html_dir)
    print_skyblue('WifiHunter已放置在/usr/share/nginx/html目录')

def unix_command(cmd):
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    p.wait()
    stdout, stderr = p.communicate()
    if p.returncode != 0:
        return p.returncode,stderr
    return p.returncode,stdout

# supervisor config
def supervisor_config(wifihunter_config):
    # exists_dir(wifihunter_config)
    with open(wifihunter_config, 'w') as f:
        f.write("""[program:WifiHunter]
command=dotnet WifiHunter.dll
directory=/root/WifiHunter/
autorestart=true
stderr_logfile=/var/log/WifiHunter.err.log 
stdout_logfile=/var/log/WifiHunter.out.log 
environment=ASPNETCORE_ENVIRONMENT=Development 
user=root 
stopsignal=INT
        """)
    print_green("supervisor配置文件写入完成")

# nginx配置文件
def nginx_config(nginx_config_file):
    with open(nginx_config_file,'w') as f:
        f.write("""user www-data;
worker_processes auto;
pid /run/nginx.pid;
include /etc/nginx/modules-enabled/*.conf;

events {
	worker_connections 768;
	# multi_accept on;
}
http {
	sendfile on;
	tcp_nopush on;
	tcp_nodelay on;
	keepalive_timeout 65;
	types_hash_max_size 2048;

	include /etc/nginx/mime.types;
	default_type application/octet-stream;

	ssl_protocols TLSv1 TLSv1.1 TLSv1.2; # Dropping SSLv3, ref: POODLE
	ssl_prefer_server_ciphers on;

	access_log /var/log/nginx/access.log;
	error_log /var/log/nginx/error.log;

	gzip on;

    server {
        listen 80;
        location / {
            root /usr/share/nginx/html;
            index index.html;
        }
    }
}
        """)
    print_green("nginx配置文件写入完成")

# 修改镜像源为阿里源
def mirrors():
    if not os.path.isfile("/etc/apt/sources.list.bak"):
        shutil.move('/etc/apt/sources.list',"/etc/apt/sources.list.bak")
        with open("/etc/apt/sources.list",'w') as f:
            f.write("""deb https://mirrors.aliyun.com/kali kali-rolling main non-free contrib
deb-src https://mirrors.aliyun.com/kali kali-rolling main non-free contrib            
            """)
        unix_command("apt-get update")
        print_blue('成功修改为阿里源')
    else:
        unix_command("apt-get update")
        print_yellow('无需修改镜像源')

# 安装doenet
def install_dotnet():
    dotnet_src_dir = un_tgz("dotnet.tar.gz")
    dotnet_dst_dir = "/usr/local/dotnet"
    bin_dotnet = '/usr/bin/dotnet'
    exists_dir(dotnet_dst_dir)
    shutil.move(dotnet_src_dir, dotnet_dst_dir)
    if os.path.exists(bin_dotnet):
        os.remove(bin_dotnet)
        print_red("{}文件存在，已成功删除旧文件".format(bin_dotnet))
    else:
        print_blue("{}文件不存在,无需删除".format(bin_dotnet))
    os.symlink(os.path.join(dotnet_dst_dir,"dotnet"), bin_dotnet)
    print_green('dotnet安装完成')

# 运行程序
def run_program():
    unix_command("systemctl restart supervisor && systemctl enable supervisor")
    unix_command("systemctl restart nginx && systemctl enable nginx")
    print_green("程序启动成功")

def main():
    print("{}检查是否为root用户...".format(RED))
    exists_root()
    print("解压文件...")
    un_dir = un_tgz("wifi.tgz")
    print("开始移动程序文件...")
    move_dir(un_dir)
    print("开始修改镜像源...")
    mirrors()
    print("安装supervisor")
    unix_command("apt install -y supervisor")
    print("开始安装dotnet...")
    install_dotnet()
    print('开始写入supervisor配置文件...')
    supervisor_config('/etc/supervisor/conf.d/wifi.conf')
    print('开始写入nginx配置文件...')
    nginx_config("/etc/nginx/nginx.conf")
    print("开始运行程序...")
    run_program()

if __name__ == "__main__":
    main()