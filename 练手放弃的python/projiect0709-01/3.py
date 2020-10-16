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





