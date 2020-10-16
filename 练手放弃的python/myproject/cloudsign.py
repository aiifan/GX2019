#!/usr/bin/env python
# encoding:utf8

from __future__ import print_function

import os
import sys
import shutil
import subprocess
import tarfile
import base64

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

def unix_command(cmd):
    """
    执行shell命令，返回code,stdout
    """
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    p.wait()
    stdout, stderr = p.communicate()
    if p.returncode != 0:
        return p.returncode,stderr
    return p.returncode,stdout

def un_tgz(file_name):
    un_path = os.path.join(os.getcwd(),file_name.split('.')[0])
    exists_dir(un_path)
    with tarfile.open(file_name, "r:gz") as f:
        for i in f:
            f.extract(i.name, os.getcwd())
    print_blue("{}解压完成".format(file_name))
    return un_path



if __name__ == "__main__":
    if os.getuid() != 0:
        print_red("请使用root用户执行该脚本！")
        sys.exit(1)
    print_green("开始执行安装脚本")
