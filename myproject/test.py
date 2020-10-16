#!/bin/env python
#encoding:utf8

from __future__ import print_function

import time
import redis
timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
print(timestamp)
def redis_cli():
    r = redis.Redis(host="192.168.0.131",port=6379)
    out = r.ping()
    if out:
        with open("123.txt", "a") as f:
            f.write("redis连接正常")
    # print(r.ping())
if __name__ == "__main__":
    while True:
        redis_cli()
        time.sleep(3)
    
