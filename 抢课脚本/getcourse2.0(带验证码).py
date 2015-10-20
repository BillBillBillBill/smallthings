#!/usr/bin/env python
#coding:utf-8

__author__ = 'Huang Xiongbiao (billo@qq.com)'
import time
import urllib2
import urllib
import json
import cookielib
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

def login(username, password):

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

        # 获取cookies
        req = urllib2.Request(
                    url = 'http://uems.sysu.edu.cn/elect/index.html',
                    headers = header
                )
        res = urllib2.urlopen(req)

        # 获取验证码图片
        try:
            addr = "http://uems.sysu.edu.cn/elect/login/code"
            img_name = '/home/bill/Desktop/code_img.jpg'
            
            open(img_name, "wb").write(urllib2.urlopen(addr).read())
        except Exception,e:
            print "[Error]Cant't download: %s:%s" % (img_name, e)
        # 登陆获取ssid
        user = {
            'username' : username,
            'password' : password,
            'j_code': raw_input("验证码: "),
            'lt'       : '',
            '_eventId' : 'submit',
            'gateway'  : 'true'
            }
        print user
        user = urllib.urlencode(user)
        req = urllib2.Request(
                    url = 'http://uems.sysu.edu.cn/elect/login',
                    data = user,
                    headers = header
                )
        res = urllib2.urlopen(req)

        sid = res.geturl().replace('http://uems.sysu.edu.cn/elect/s/types?sid=', '')
        print sid
        return sid
        #print res.read()
    except Exception,e:
        print e

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
            s = "抢不到,再试试"
        elif code == 0:
            s = "成功选上了！！！！"
        elif code == 9:
            s = "这门课已经选上了!!!"
        elif code == 5:
            s = "选课失败：系统中没有您这个学期的报到记录，不允许选课。请联系您所在院系的教务员申请补注册。"
        else:
            s = "未知代码" + str(code)
        print "(code:", code, ")", caurse, s
    except Exception, e:
        print "出错, 请重新登录或确认输入的教学班号是否正确", e

def start():
    print "SYSU course helper By Bill"
    print "QQ:536803427"

    # username = raw_input("Student id:")
    # password = raw_input("Password:")


    sid = False
    while not sid:
        sid = login('13331093', 'NezTjJ')
        if sid:
            print "登录成功..Sid:",sid
        else:
            print "登录失败- -再试试"

    # 获取教学班号列表
    courselist = read_course()

    times = 1
    while times:
        print "在进行第", times, "次选课"
        for i in courselist:
            print "选择课程:", i
            takecourse(i, sid)
        times += 1
        time.sleep(3)

def read_course():
    l=[]
    course_num = raw_input("How many course:")
    course_num = int(course_num)
    while course_num:
        c = raw_input("course"+str(course_num)+":")
        l.append(c)
        course_num -= 1
    return l

if __name__ == '__main__':
    start()
