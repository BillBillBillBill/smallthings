# -*- coding:utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy.utils.response import get_base_url
from blog.items import Website
import sys
import string
reload(sys)
sys.setdefaultencoding('utf-8')
# sys.stdout=open('output.txt','w') #将打印信息输出在相应的位置下


add = 0


class DmozSpider(CrawlSpider):

    name = "blog"
    allowed_domains = ["csdn.net"]
    start_urls = [
        "http://blog.csdn.net/huangxiongbiao",
    ]

    rules = (
        # 提取匹配 huhuuu/default.html\?page\=([\w]+) 的链接并跟进链接(没有callback意味着follow默认为True)
        Rule(SgmlLinkExtractor(allow=('huangxiongbiao/article/list/([\d]+)', ),)),

        # 提取匹配 'huhuuu/p/' 的链接并使用spider的parse_item方法进行分析
        Rule(SgmlLinkExtractor(allow=('huangxiongbiao/article/details/', )), callback='parse_item'),
    )

    def parse_item(self, response):
        # global add #用于统计博文的数量
        # print  add
        # add+=1
        sel = Selector(response)
        items = []
        item = Website()
        # 观察网页对应得html源码
        item['headTitle'] = sel.xpath('/html/head/title/text()').extract()[0]
        item['url'] = get_base_url(response)
        print item
        items.append(item)
        return items
