#!/usr/bin/env python
#coding:utf-8

__author__ = 'Huang Xiongbiao (billo@qq.com)'
import time
import urllib2
import urllib
import json
import cookielib

def login():
    user = {
        'username' : "学号",
        'password' : "密码",
        'lt'       : '',
        '_eventId' : 'submit',
        'gateway'  : 'true'
        }
    # user = {'username' : raw_input("学号: "),
    #     'password' :raw_input("密码: "),
    #     'lt'       : '',
    #     '_eventId' : 'submit',
    #     'gateway'  : 'true'
    #     }
    try:
        cookie = cookielib.CookieJar()
        cookieProc = urllib2.HTTPCookieProcessor(cookie)
        opener = urllib2.build_opener(cookieProc)
        urllib2.install_opener(opener)

        header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding' : 'gzip,deflate,sdch',
            'Accept-Language' : 'zh-CN,zh;q=0.8',
            'Cache-Control'   : 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Length'  : '66',
            'Content-Type'    : 'application/x-www-form-urlencoded',
            'Host': 'uems.sysu.edu.cn',
            'Origin'          : 'http://uems.sysu.edu.cn',
            'Referer'         : 'http//uems.sysu.edu.cn/elect/',
            'User-Agent'      : 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0',
            }

        user = urllib.urlencode(user)
        req = urllib2.Request(
                    url = 'http://uems.sysu.edu.cn/elect/login',
                    data = user,
                    headers = header
                )
        res = urllib2.urlopen(req)
        sid = res.geturl().replace('http://uems.sysu.edu.cn/elect/s/types?sid=', '')
        return sid
    except Exception,e:
        print e
        return False

def takecourse(id, sid):
    try:
        data = {
            "jxbh": id,
            "sid": sid
        }
        header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding' : 'gzip,deflate,sdch',
            'Accept-Language' : 'zh-CN,zh;q=0.8',
            'Cache-Control'   : 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Length'  : '60',
            'Content-Type'    : 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'uems.sysu.edu.cn',
            'Origin'          : 'http://uems.sysu.edu.cn',
            'Referer'         : 'http://uems.sysu.edu.cn/elect/s/',
            'User-Agent'      : 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0',
            'X-Requested-With': 'XMLHttpRequest'
            }
        data = urllib.urlencode(data)
        req = urllib2.Request(
                    url = 'http://uems.sysu.edu.cn/elect/s/elect',
                    data = data,
                    headers = header
                )
        res = urllib2.urlopen(req)
        js = json.loads(res.read())
        code = js.get('err').get('code')
        caurse = js.get('err').get('caurse')
        s = ""
        if caurse == None:
            caurse = ""
        if code == 18:
            s = "抢不到,再努力试试"
        elif code == 0 or code == 9:
            s = "已经选上了O(∩_∩)O!!!"
        print "(code:", code, ")", caurse, s
    except Exception,e:
        print "掉线了吧, 赶紧重新登录吧", e



def start():
    sid = False
    while not sid:
        sid = login()
        print sid
        if sid:
            print "登录成功..Sid:",sid
        else:
            print "登录失败- -再试试"

    #教学班号列表
    l = [""]

    # numOfcourse = raw_input("输入想选课门数:")
    # l = []
    # for i in range(int(numOfcourse)):
    #     msg = "请输入第"+str(i+1)+"门课教学班号："
    #     l.append(raw_input(msg))

    times = 1
    while times:
        print "在进行第", times, "次选课"
        for i in l:
            print "Take:", i
            takecourse(i, sid)
        times += 1
        time.sleep(1)


start()