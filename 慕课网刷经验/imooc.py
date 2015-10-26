#!/usr/bin/env python
#coding:utf-8
'''
慕课网刷经验
'''

__author__ = 'Huang Xiongbiao (billo@qq.com)'
import time
import urllib2
import urllib
import json
import cookielib
import random

ti = 40000.02

def takecourse(id):
    global ti
    ti = ti + 1000
    print ti
    id = str(id)
    try:
        data = {
            'learn_time': ti,
            'mid': id,
            'time': '99.138000000000005'
        }
        header = {
            'Accept': ' application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding' : 'gzip, deflate',
            'Accept-Language' : 'zh-CN,zh;q=0.8',
            'Cache-Control'   : 'no-cache',
            'Cookie':'imooc_uuid=63a5032b-613b-4ad3-b9f3-520c914277e3; Hm_lvt_f0cfcccd7b1393990c78efdeebff3968=1422191903,1422340830,1422421658,1422459744; uid=467694; xiao=467694; nickname=%E9%BB%91%E7%BE%BD%E5%A4%A7%E4%BA%BA; loginstate=1; apsid=ExNDA1ZDgwZTNlOGUzNzliZmJkYzZmOTA1OWY1N2YAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADIwMzIyNTQ2MzUAAAAAAAAAAAAAAAAAAAAAAAAAAAAANDY3Njk0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA1MzY4MDM0MjdAcXEuY29tAAAAAAAAAAAAAAAAAAAAADliZjNiNWRlZTU2NTg4MDA1NDZhOTNhZDJhYmY0MGE4pAVJVKkbSVQ%3DOD; channel=9a720972bb7a45e13470d2a6d5345b9f_cnblogs; PHPSESSID=7a3r6c4ju2lt89bbc6m93c57m4; jwplayer.volume=29; Hm_lpvt_f0cfcccd7b1393990c78efdeebff3968=1422467274',
            'Connection': 'keep-alive',
            'Content-Length'  : '48',
            'Content-Type'    : 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'www.imooc.com',
            'Origin'          : 'http://www.imooc.com/video/'+id,
            'Referer'         : 'http://www.imooc.com/video/'+id,
            'User-Agent'      : 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0',
            'X-Requested-With': 'XMLHttpRequest'
            }
        data = urllib.urlencode(data)
        req = urllib2.Request(
                    url = 'http://www.imooc.com/course/ajaxmediauser/',
                    data = data,
                    headers = header
                )
        res = urllib2.urlopen(req)
    except Exception, e:
        takecourse(random.randrange(1, 30000))
        print "掉线了吧, 赶紧重新登录吧", e


times = 1

while times:
    print "在进行第", times, "次"
    takecourse(times % 30000)
    times += 1
    time.sleep(0.1)
