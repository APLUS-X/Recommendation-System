# -*- coding: utf-8 -*-

import os
# Scrapy settings for positionDetails project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'positionDetails'

SPIDER_MODULES = ['positionDetails.spiders']
NEWSPIDER_MODULE = 'positionDetails.spiders'

ROBOTSTXT_OBEY = True

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'
basedir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

#FEED_URI = 'file:///C:/Users/ben/Desktop/Lagou/0527/data/position.csv'
FEED_URI = basedir + '/positionData/positionInfo.csv'
FEED_FORMAT = 'csv'

COOKIES_ENABLED=False

DOWNLOAD_DELAY=3


