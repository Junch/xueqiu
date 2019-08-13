# -*-coding=utf-8-*-
__author__ = 'Rocky'

from scrapy import cmdline
import datetime

'''
http://30daydo.com
Contact: weigesysu@qq.com
'''

# cmd='scrapy crawl xueqiu -s LOG_FILE={}.log'.format(datetime.datetime.now().strftime('%Y-%m-%d'))
cmd='scrapy crawl xueqiu'
cmdline.execute(cmd.split())