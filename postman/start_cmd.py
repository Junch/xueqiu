# -*-coding=utf-8-*-
from scrapy import cmdline
__author__ = 'Rocky'
'''
http://30daydo.com
Contact: weigesysu@qq.com
'''
cmd='scrapy crawl xueqiu -s LOG_FILE=scrapy.log'
cmdline.execute(cmd.split())