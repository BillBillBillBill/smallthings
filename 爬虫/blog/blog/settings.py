# -*- coding: utf-8 -*-

# Scrapy settings for blog project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'blog'

SPIDER_MODULES = ['blog.spiders']
NEWSPIDER_MODULE = 'blog.spiders'

ITEM_PIPELINES = {
    'blog.pipelines.BlogPipeline': 300,
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'blog (+http://www.yourdomain.com)'
