#!/usr/bin/env bash
# *-* encoding=utf-8 *-*

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
SKYBLUE='\033[0;36m'
PLAIN='\033[0m'
LOGFILE='/root/TsaInstall.log'

# check root
[[ $EUID -ne 0 ]] && echo -e "${RED}Error:${PLAIN} This script must be run as root!" && exit 1


echo -e "${YELLOW}#####################################################"
echo -e "#               正在检查网络连接                    #"
echo -e "#####################################################${PLAIN}"
ping -c 3 www.baidu.com > /dev/null
if [[ $? -ne 0 ]]; then
    echo -e "${RED}#####################################################"
    echo -e "#                     网络连接失败                  #"
    echo -e "#                    请检查网络连接                 #"
    echo -e "#####################################################${PLAIN}"
    exit 1
else
    echo -e "${GREEN}#####################################################"
    echo -e "#                     网络连接正常                  #"
    echo -e "#                  开始安装时间戳服务               #"
    echo -e "#####################################################${PLAIN}"
fi

# tsa drive

swcsmdrv(){
    if [[ ! -d ${MIMAKA_DIR} ]]; then
        mkdir ${MIMAKA_DIR}
    else
        /lib/swcsmdrv/unload
        rm -rf /lib/swcsmdrv
        mkdir /lib/swcsmdrv
    fi
    cp ${MIMAKA_DRIVER} ${MIMAKA_DIR}
    chmod +x ${MIMAKA_DIR}/*
    ln -sf ${MIMAKA_DIR}/${MIMAKA_LIBSWSDS} /lib64/libswsds.so
    \cp ${MIMAKA_DIR}/swcsmmgmt_v3.7.5 /root/
}


echo -e "${YELLOW}#####################################################"
echo -e "#                正在安装密码卡驱动                #"
echo -e "#       如未安装密码卡，请选择4退出安装密码卡驱动    #"
echo -e "#####################################################${PLAIN}"
echo -e
echo -ne " 1. 18卡 2. 26卡 3.已安装密码卡 4.退出安装程序"
while :; do echo
        read -p "请输入密码卡型号：" telecom
        if [[ ! $telecom =~ ^[1-4]$ ]]; then
            echo -e "${RED}输入错误，请重新输入${PLAIN}"
        else    
            break
        fi
done
MIMAKA_DIR=/lib/swcsmdrv
if [[ ${telecom} == 1 ]]; then
    MIMAKA_DRIVER=MimakaDriver/18/*
    MIMAKA_LIBSWSDS=libswsds.so.3.8.5.0
    swcsmdrv
fi

if [[ ${telecom} == 2 ]]; then
    MIMAKA_DRIVER=MimakaDriver/26/*
    MIMAKA_LIBSWSDS=libswsds.so.3.8.5.0
    swcsmdrv
fi

if [[ ${telecom} == 3 ]]; then
    break
fi

if [[ ${telecom} == 4 ]]; then
    echo -e "${SKYBLUE}请安装密码卡驱动后重新操作${PLAIN}"
    exit 0
fi
clear
echo -e "${YELLOW}#####################################################"
echo -e "开始安装程序运行环境${PLAIN}"
# install MariaDB PHP Apache NETCORE
yum install epel-release -y
yum install -y ntp mariadb mariadb-server php httpd php-gd php-ldap php-mysql php-odbc php-pdo php-pear php-pecl-apc php-pecl-memcached php-soap php-xml php-xmlrpc certmonger crypto-utils httpd-manual libmemcached memcached mod_auth_kerb mod_nss mod_perl mod_revocator mod_ssl mod_wsgi perl-CGI perl-CGI-Session perl-Cache-Memcached python-memcached squid webalizer python-pip redis 
rpm -Uvh https://packages.microsoft.com/config/rhel/7/packages-microsoft-prod.rpm 
yum install -y dotnet-sdk-2.2 

# tsa web
rm -rf /var/www/html 
unzip  TsaWeb.zip -d /var/www/ 
chmod 777 /var/www/html/services/BusinessLog
chmod 777 /var/www/html/services/Tsa
chmod 777 /var/www/html/services/WebLog
systemctl start httpd
systemctl start ntpd
systemctl start redis

# initialize database
systemctl start mariadb
mysql -u root < tsa_mysql_admin.sql
mysql -u root --database=tsa < tsa_mysql.sql
mysql -u root --database=tsa < tsa_mysql_init.sql


# close selinux
setenforce 0
rm /etc/selinux/config
cp config /etc/selinux/


# install and start CommandServer

#COMMANDSERVER=`ps -uax |  grep -w CommandServer | awk '{print $2}' | sed -n '1,1p' ` 
#kill ${COMMANDSERVER}
killall CommandServer
rm -f /usr/bin/CommandServer
\cp CommandServer /usr/bin/CommandServer
chmod +x /usr/bin/CommandServer
chmod  777 /etc/ntp.conf
\cp nss.conf /etc/httpd/conf.d/nss.conf
/usr/bin/CommandServer
\cp rc.local /etc/rc.d/rc.local


# TsaServer
systemctl stop tsmonitor
systemctl stop tsserver
rm -rf /tsserver
unzip tsserver.zip -d /
chmod 777 /tsserver
chmod 777 /tsserver/tsserver
chmod 777 /tsserver/tsmonitor
chmod 777 /tsserver/GenerateRequest
chmod 777 /tsserver/tsa.cnf
\cp libcrypto.so.1.0.0 /lib64/libcrypto.so.1.0.0
\cp libssl.so.1.0.0 /lib64/libssl.so.1.0.0
\cp tsserver.service /lib/systemd/system/tsserver.service
\cp tsmonitor.service /lib/systemd/system/tsmonitor.service
systemctl daemon-reload
systemctl start tsserver
systemctl start tsmonitor

firewall-cmd --add-port=80/tcp --permanent 
firewall-cmd --add-port=443/tcp --permanent 
firewall-cmd --add-port=8080/tcp --permanent 
firewall-cmd --add-port=9005/tcp --permanent 
systemctl restart firewalld


\cp my.cnf /etc/my.cnf
systemctl start mariadb
mysql -u root --database=tsa < event.sql
systemctl start mariadb


systemctl stop supervisord
rm -rf /root/HttpTsa
unzip HttpTsa.zip -d /root/
pip install supervisor
rm -rf /etc/supervisor
mkdir /etc/supervisor
\cp -r conf.d /etc/supervisor/
\cp supervisord.conf /etc/supervisor
\cp supervisord.service /lib/systemd/system/
systemctl restart supervisord


systemctl enable mariadb
systemctl enable httpd
systemctl enable ntpd
systemctl enable tsserver
systemctl enable tsmonitor
systemctl enable supervisord
systemctl enable redis