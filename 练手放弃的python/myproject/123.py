#!/usr/bin/env python
#encoding:utf-8
from __future__ import print_function
import os

import psutil


def get_cpu_info():
    cpu_percent = psutil.cpu_percent()
    return dict(cpu_percent=cpu_percent)


print(get_cpu_info())