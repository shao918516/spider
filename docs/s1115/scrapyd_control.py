#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Terry'

import requests

def schedule(ip_port, project, spider):
    url = f'http://{ip_port}/schedule.json'
    data = {
        'project': project,
        'spider': spider
    }
    response = requests.post(url, data=data)
    print(response.text)

def cancel(ip_port, project, job):
    url = f'http://{ip_port}/cancel.json'
    data = {
        'project': project,
        'job': job
    }
    response = requests.post(url, data=data)
    print(response.text)

if __name__ == '__main__':
    ip_port = '192.168.1.122:6800'
    project = 'dingdian'
    spider = 'dingdian'

    # 启动爬虫
    # schedule(ip_port, project, spider)

    #  关闭爬虫
    job = '383c97bae87c11e8b3f758fb8457c654'
    cancel(ip_port, project, job)