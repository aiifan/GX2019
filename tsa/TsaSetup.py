#!/usr/bin/python 
# encoding=utf-8

import os

def c(command_list):
    for command in [a.strip() for a in command_list.split('\n')]:
        if command:
            os.system(command)

current_level = 1
def log_level(name, description):
    global current_level
    print '[level {0}: {1}] {2}'.format(current_level, name, description)
    current_level += 1

log_level('web', 'copy and unzip TsaWeb')
c('rm -rf /var/www/html')
c('mkdir /var/www/html')
c('cp TsaWeb.zip /var/www/html')
c('unzip /var/www/html/TsaWeb.zip -d /var/www/html')
c('chmod 777 /var/www/html/services/BusinessLog')
c('chmod 777 /var/www/html/services/Tsa')
c('chmod 777 /var/www/html/services/WebLog')
c('rm -rf /var/www/html/TsaWeb.zip')


log_level('file-privileges', 'change network config and init file privileges')
c('''
touch /etc/sysconfig/network-scripts/ifcfg-eth0
chmod 666 /etc/sysconfig/network-scripts/ifcfg-eth0
touch /etc/sysconfig/network-scripts/ifcfg-eth1
chmod 666 /etc/sysconfig/network-scripts/ifcfg-eth1
''')

log_level('services', 'config services: httpd, mysqld')
c('chkconfig --level 35 httpd on')
c('chkconfig --level 35 mysqld on')
c('chkconfig --level 35 ntpd on')
c('service httpd start')
c('service mysqld start')
c('service ntpd start')

log_level('database', 'initialize database')
c('''
mysql -u root < tsa_mysql_admin.sql
mysql -u root --database=tsa < tsa_mysql.sql
mysql -u root --database=tsa < tsa_mysql_init.sql
''')

log_level('selinux', 'close selinux')
c('''
setenforce 0
rm /etc/selinux/config
cp config /etc/selinux/
''')

log_level('CommandServer', 'install and start CommandServer')
c('''
service CommandServer stop
rm -f /usr/bin/CommandServer
\cp CommandServer.py /usr/bin/CommandServer
\cp CommandServer.service /etc/init.d/CommandServer
chkconfig --add CommandServer
chkconfig --levels 35 CommandServer on
chkconfig --levels 1246 CommandServer off
chmod  777 /etc/ntp.conf
rm -f /etc/httpd/conf.d/nss.conf
cp nss.conf /etc/httpd/conf.d/nss.conf
service CommandServer start
''')

log_level('TsaServer', 'install and start TsaServer')
c('''
service tsserver stop
rm -rf /tsserver
rm -rf /etc/init.d/tsserver
cp tsserver.zip /
unzip /tsserver.zip -d /
chmod 777 /tsserver
chmod 777 /tsserver/tsserver
chmod 777 /tsserver/tsmonitor
chmod 777 /tsserver/GenerateRequest
chmod 777 /tsserver/tsa.cnf
\cp tsserver.service /etc/init.d/tsserver
\cp libcrypto.so.0.9.8 /usr/lib/libcrypto.so.0.9.8 
\cp libcrypto.so.1.0.2 /usr/lib/libcrypto.so.1.0.2
\cp /usr/lib/libcrypto.so.1.0.1e /usr/lib/libcrypto.so.1.0.1
\cp /usr/lib/libcrypto.so.1.0.1e /usr/lib/libcrypto.so.1.0.0
\cp /usr/lib/libssl.so.1.0.1e /usr/lib/libssl.so.1.0.0
rm -rf /usr/lib/libcrypto2.so
ln -s /usr/lib/libcrypto.so.1.0.2 /usr/lib/libcrypto2.so
./req
chkconfig --add tsserver
chkconfig --levels 35 tsserver on
service tsserver start
rm -rf /tsserver.zip
''')

# log_level('CardAutorun', 'Card driver autorun')
# c('''
# rm -rf /lib/swcsmdrv
# mkdir /lib/swcsmdrv
# \cp libswsds.so.3.8.5.0 /usr/lib/libswsds.so.3.8.5.0
# ln -s /usr/lib/libswsds.so.3.8.5.0 /usr/lib/libswsds.so
# \cp swcsm18.ko /lib/swcsmdrv/swcsm18.ko
# \cp loaddrv /lib/swcsmdrv/loaddrv
# chmod 777 /usr/lib/libswsds.so.3.8.5.0
# chmod 777 /lib/swcsmdrv/swcsm18.ko
# chmod 777 /lib/swcsmdrv/loaddrv
# ''')

log_level('autodelete', 'autodelete data')
c('rm -rf /etc/my.cnf')
c('cp my.cnf /etc/my.cnf')
#c('chmod 777 /etc/my.cnf')
c('service mysqld restart')
c('mysql -u root --database=tsa < event.sql')
c('service mysqld restart')

log_level('end', 'completed')
