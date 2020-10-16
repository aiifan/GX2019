#!/usr/bin/env bash
# encoding:utf-8


# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
SKYBLUE='\033[0;36m'
PLAIN='\033[0m'


# check root
[[ $EUID -ne 0 ]] && echo -e "${RED}Error:${PLAIN} This script must be run as root!" && exit 1


[[ "$#" -ne 4 ]] && echo -e "${SKYBLUE}需要且只能需要4个参数\n参数1：要创建的网桥名称\n参数2(int)：PORT口开始\n参数3(int)：PORT口结束\n参数4：PORT口前缀\n例如：./ovs.sh ovs-br 1 200 p  会创建一个名叫ovs-br的网桥, 有p1-p200的port,vlan分别为1-200${PLAIN}" && exit 2

BR=$1
FIRST=$2
BREAK=$3
P=$4
ovs-vsctl add-br $BR
for i in `seq $FIRST $BREAK`;do
  ovs-vsctl add-port $BR "$P$i" tag="$i" -- set Interface "$P$i" type=internal
done

exit 0
