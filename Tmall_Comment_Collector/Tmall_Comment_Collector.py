# 按时间 order=1 按信用 order=2 按默认 order=3
# 默认按时间
#coding:utf-8
import urllib
import urllib2
import re

def collectTmallrecommend(itemId, NumOfPage=99):
    find = []
    for page in range(1,NumOfPage):
        url = "http://rate.tmall.com/list_detail_rate.htm?itemId=%s&currentPage=%d" %(itemId,page)
        print "Opening page", page
        keys = {
            "Host":"rate.tmall.com",
            "GET":url,
            "Referer":"http://detail.tmall.com/",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36",
        }
        req = urllib2.Request(url)
        for key in keys:
            req.add_header(key,keys[key])
        find = find + re.findall("rateContent\":\"(.*?)\",\"",urllib2.urlopen(req).read())
        if len(find) == 0:
            break
    Out_Put_File_Name = 'ID_' + str(itemId) + '_recomment' +'.txt'
    print "Writing data to file...\n"
    read = open(Out_Put_File_Name,'a+')
    for recommend in find:
        read.write(recommend)
        read.write("\n")
    read.close()    
    print "Finish!!Please open %s\n" % Out_Put_File_Name

def main():
    print "--------------------------------------------"
    print "-           天猫商品买家评论采集器         -"
    print "-               数据保存形式:              -"
    print "-          ID_itemId_recommend.txt         -"
    print "--------------------------------------------"
    while True:
        itemId = raw_input("Please input itemId(0 to quit):")
        if itemId[0] == '\r':
            itemId = itemId[1:]
        if itemId == '0':
            break
        NumOfPage = raw_input("How many page you want?(max 99)")
        NumOfPage = int(NumOfPage)
        collectTmallrecommend(itemId, NumOfPage)

main()