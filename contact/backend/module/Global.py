#!/usr/bin/python
# coding:utf-8

default = {}

import socket

default['city'] = 'BJ'
hostname = socket.getfqdn().split('.')
if len(hostname) > 2:
    city = hostname[1]
    if city in ['bj', 'dc', 'wx', 'xm', 'la','kl']:
        default['city'] = city.upper()
    if city.lower() == 'ad':
        ip = socket.gethostbyname(socket.gethostname()).split('.')
        ip = int("%03d" % int(ip[0]) + "%03d" % int(ip[1]))
        if ip==10009: default['city'] = 'BJ'
        if ip==10137: default['city'] = 'XM'
        if ip==10073: default['city'] = 'WX'
        if ip==10000: default['city'] = 'LA'
        if ip == 172028: default['city'] = 'DC'
default['domain'] = 'base-fx.com'
