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



log_level('TsaMod', 'install and start TsaMod')
c('''
cp hnca.crt /tsserver/hnca.crt
cp hnca-sm2.crt /tsserver/hnca-sm2.crt
cp mod_createTimeStamp.so /usr/lib/httpd/modules/mod_createTimeStamp.so
cp mod_verifyTimeStamp.so /usr/lib/httpd/modules/mod_verifyTimeStamp.so
cp mod_getTimeStampInfo.so /usr/lib/httpd/modules/mod_getTimeStampInfo.so
chmod 777 /usr/lib/httpd/modules/mod_createTimeStamp.so
chmod 777 /usr/lib/httpd/modules/mod_verifyTimeStamp.so
chmod 777 /usr/lib/httpd/modules/mod_getTimeStampInfo.so
rm -f /etc/httpd/conf/httpd.conf
cp httpd.conf /etc/httpd/conf/httpd.conf
service httpd restart
''')


