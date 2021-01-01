# -*- coding: utf-8 -*-
import datetime
import json
import re
import scrapy
from scrapy import Request, FormRequest
import logging
import redis
from sandbox.items import SpiderItem
from sandbox.utility import get_header

# get
class GeneralSpider(scrapy.Spider):
    name = 'spider'
    # 技术
    # BASE_URL = 'https://cuiqingcai.com/category/technique/page/{}'
    # 生活
    BASE_URL = 'https://xueqiu.com/service/v5/stock/screener/quote/list?page={}&size=30&order=desc&orderby=percent&order_by=percent&market=CN&type=sh_sz'

    def start_requests(self):
        start_page = 1

        yield Request(
            url=self.BASE_URL.format(start_page),
            meta={'page': start_page}
        )

    def parse(self, response,**kwargs):
        page = response.meta['page']
        next_page = page + 1

        js_data = json.loads(response.text)
        count = js_data['data']['count']
        total_page = count//30+1
        stock_list = js_data['data']['list']
        for stock in stock_list:
            yield stock

        if next_page<=total_page:
            yield Request(
            url=self.BASE_URL.format(next_page),
            meta={'page': next_page}
        )



    def close(spider, reason):
        print('关闭spider')


