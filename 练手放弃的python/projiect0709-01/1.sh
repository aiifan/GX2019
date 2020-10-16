#!/usr/bin/env bash
# encoding:utf8
###############################################
# 仅支持centos7
# 0:正常
# 1:不是root用户
# 2:网络异常
# 3:安装已存在
# 4:系统不支持
# 5:参数不正确
###############################################



RED = "\033[1;31m"
GREEN = '\033[0;32m'
YELLOW = '\033[0;33m'
BLUE = "\033[0;34m"
PURPLISHRED = "\033[0;35m"
SKYBLUE = '\033[0;36m'
PLAIN = '\033[0m'

function exist() {
    [[ $EUID -ne 0 ]] && echo -e "${RED}Error:${PLAIN} This script must be run as root!" && exit 1
    
    grep -q 'CentOS Linux release 7' /etc/redhat-release
    if [[ $? -ne 0 ]]; then
        printf "不支持系统\n"
        exit 4
    fi

    ping -c 3 www.baidu.com > /dev/null
    if [[ $? -ne 0 ]]; then
        echo -e "${RED}网络连接失败,请检查网络连接${PLAIN}"
        exit 2
    fi

    if [[ ! $# -eq 1 ]];then
        echo -e "${RED}参数不正确${PLAIN}"
        usage
        exit 5
    fi
}

function exitsParam() {
    
    while :
        echo -e "python3 nginx dotnet2 dotnet3 supervisor redis"
        read -p "请选择您需要安装的软件包：" par
        case "${par}" in
            python3)
                installPython3
                break
                ;;
            nginx)
                installNginx
                break
                ;;
            dotnet2)
                installDotnet2
                break
                ;;
            dotnet3)
                installDotnet3
                break
                ;;
            redis)
                installRedis
                break
                ;;
            supervisor)
                installSupervisor
                break
                ;;
            *)
                echo -e "${RED}输入不正确${PLAIN}"
                ;;
        esac
}


function prepare_install() {
    which curl >/dev/null 2>&1
    if [ $? -ne 0 ];then
        yum install -y curl
    fi
    if grep -q 'mirror.centos.org' /etc/yum.repos.d/CentOS-Base.repo; then
        curl -o /etc/yum.repos.d/CentOS-Base.repo https://mirrors.aliyun.com/repo/Centos-7.repo
    fi
    if grep -q 'mirrors.fedoraproject.org' /etc/yum.repos.d/epel.repo; then
        curl -o /etc/yum.repos.d/epel.repo http://mirrors.aliyun.com/repo/epel-7.repo
    fi
    if [[ ! -f "/etc/yum.repos.d/microsoft-prod.repo" ]];then
        rpm -Uvh https://packages.microsoft.com/config/centos/7/packages-microsoft-prod.rpm
    fi
    # yum clean all
    # yum makecache

    setenforce 0
    sed -i 's/SELINUX=enforcing/SELINUX=disabled/' /etc/selinux/config
}

function usage() {
   echo -e "${GREEN}简易安装脚本"
   echo
   echo -e "Usage: "
   echo -e "  bash install.sh [COMMAND] ..."
   echo -e "Examples: "
   echo -e "  bash install.sh python3"
   echo -e "  bash install.sh python3 nginx"
   echo -e "  bash install.sh --help"
   echo
   echo -e "Commands: "
   echo -e "  python3      安装 Python3.6.8"
   echo -e "  nginx        安装 nginx1.16.1"
   echo -e "  dotnet2      安装 dotnet2.2"
   echo -e "  dotnet3      安装 dotnet3.1"
   echo -e "  redis        安装 redis3.2.12"
   echo -e "  supervisor   安装 supervisor"
   echo -e "  upgrade      升级 JumpServer"
   echo -e "  reset        重置组件${PLAIN}"
}

function alreadyInstalled() {
    echo -e "${YELLOW}检测到您已安装${PURPLISHRED}${par}"
    echo -e "${YELLOW}请检查系统!!!${PLAIN}"
    exit 3
}

function installNginx() {
    which nginx >/dev/null 2>&1
    if [ $? -ne 0 ];then
        yum install nginx -y
        systemctl enable nginx
    else
        alreadyInstalled
    fi
}

function configNgin() {
    tee /etc/nginx/nginx.conf <<-"EOF"
    user nginx;
    worker_processes auto;
    error_log /var/log/nginx/error.log;
    pid /run/nginx.pid;

    include /usr/share/nginx/modules/*.conf;

    events {
    worker_connections 1024;
    }

    http {
        log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                        '$status $body_bytes_sent "$http_referer" '
                        '"$http_user_agent" "$http_x_forwarded_for"';

        access_log  /var/log/nginx/access.log  main;

        sendfile            on;
        tcp_nopush          on;
        tcp_nodelay         on;
        keepalive_timeout   65;
        types_hash_max_size 2048;

        include             /etc/nginx/mime.types;
        default_type        application/octet-stream;

        include /etc/nginx/conf.d/*.conf;
    }
EOF
while :
do
    echo -e ""
    echo -e "******配置nginx******"
    read -p "输入nginx使用的端口(80-65535,默认80)：" nginxPort
    if test -z $nginxPort 
    then
        local nginxPort=80
        break
    else
        if [ $nginxPort -lt 80 -o $nginxPort -gt 65535 ];then
            echo -e "${RED}输入端口有误${PLAIN}"
        else
            
        fi

    fi
done

    read -p
        tee /etc/nginx/conf.d/port${nginxPort}.conf <<-"EOF"
        server {
            listen       ${nginxPort} default_server;
            server_name  _;
            root         /usr/share/nginx/html;
            
            include /etc/nginx/default.d/*.conf;

            location / {
            }

            error_page 404 /404.html;
                location = /40x.html {
            }

            error_page 500 502 503 504 /50x.html;
                location = /50x.html {
            }
        }
EOF
done
}



function installRedis() {
    which redis-server >/dev/null 2>&1
    if [ $? -ne 0 ];then
        yum install -y redis
        sed -i "s/bind 127.0.0.1/bind 0.0.0.0/g" /etc/redis.conf
        systemctl enable redis
    else
        alreadyInstalled
    fi
}

function installSupervisor() {
    which supervisorctl >/dev/null 2>&1
    if [ $? -ne 0 ];then
        yum install -y supervisor
    else
        alreadyInstalled
    fi
}

function installDotnet2() {
    which dotnet >/dev/null 2>&1
    if [ $? -ne 0 ];then
        yum install -y dotnet-sdk-2.2
        yum install libgdiplus-devel
    else
        alreadyInstalled
    fi
}

function installDotnet3() {
    which dotnet >/dev/null 2>&1
    if [ $? -ne 0 ];then
        yum install -y dotnet-sdk-3.1
        yum install libgdiplus-devel
    else
        alreadyInstalled
    fi
}

function installPython3() {
    which python3.6 >/dev/null 2>&1
    if [ $? -ne 0 ];then
        yum install -y python36 python36-devel
        pip install -U pip
    else
        alreadyInstalled
    fi
    if [ ! -f "~/.pip/pip.conf" ]; then
        mkdir -p ~/.pip
        tee ~/pip/pip.conf <<-"EOF"
        [global]
        index-url = https://mirrors.aliyun.com/pypi/simple/

        [install]
        trusted-host=mirrors.aliyun.com
EOF
    fi
}

function main() {
    case "${par}" in
        python3)
            installPython3
            ;;
        nginx)
            installNginx
            ;;
        dotnet2)
            installDotnet2
            ;;
        dotnet3)
            installDotnet3
            ;;
        redis)
            installRedis
            ;;
        supervisor)
            installSupervisor
            ;;
        --help)
            usage
            ;;
        -h)
            usage
            ;;
        *)
            echo -e "${RED}UNKNOWN COMMAND: ${PLAIN}${par}"
            echo -e "See 'bash install.sh --help' \n"
            usage
    esac
}


exist
prepare_install
main