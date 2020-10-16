#!/usr/bin/env python
# encoding:utf-8

# vlan
def w_network(n1,n2):
    config = """config interface 'p{}'
        option proto 'static'
        option ifname 'eth1.{}'
        option delegate '0'
        option ipaddr '10.0.{}.1'
        option netmask '255.255.255.0'

"""
    for i in range(n1,n2):
        a = config.format(i,i,i)
        with open("network", 'a') as f:
            f.write(a)
    return None

# dhcp
def w_dhcp(n1,n2):
    config = """config dhcp 'p{}'                                     
        option start '100'                           
        option leasetime '12h'                       
        option limit '150'                           
        option interface 'p{}'

"""
    for i in range(n1,n2):
        a = config.format(i,i)
        with open("dhcp", 'a+') as f:
            f.write(a)
    return None
# firewall
def w_firewall(n1,n2):
    for i in range(n1,n2):
        p = "p{} ".format(i)
        with open("firewall",'a') as f:
            f.write(p)
    return None

if __name__ == "__main__":
    w_network(5,201)
    w_dhcp(5,201)
    w_firewall(5,201)