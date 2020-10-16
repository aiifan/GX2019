#!/bin/env python
#encoding:utf8

from __future__ import print_function
import time
import subprocess

import redis

def redis_cli():
    r = redis.Redis(host="121.42.230.169",port=2019, password="Qc3&0#UhyLtrFTH1v*")
    if r.ping():
        log('redis连接正常')
    else:
        log("redis连接失败")

def unix_command(cmd):
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    p.wait()
    stdout, stderr = p.communicate()
    if p.returncode != 0:
        return p.returncode,stderr
    return p.returncode,stdout

def log(meg):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    with open('./vlog.txt', "a") as f:
        f.write("{} : {}\n".format(timestamp, meg))

def main():
    log("开始")
    while True:
        code, out = unix_command("ping -c 1 121.42.230.169")
        if code != 0:
            log("网络不通")
            log(out)
        else:
            log("网络正常")
            redis_cli()
        time.sleep(10)

if __name__ == "__main__":
    main()