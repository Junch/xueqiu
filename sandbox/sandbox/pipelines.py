# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from sandbox.config import user, password, host, port
import datetime
from scrapy.exceptions import DropItem


class MongoPipeline(object):
    def __init__(self):
        today = datetime.datetime.today().strftime('%Y-%m-%d')
        self.client = self.mongo()
        self.doc=self.client['xueqiu'][today]
        self.check_exists()

    def check_exists(self):
        if self.doc.count()>0:
            # 清除数据
            self.doc.drop()
    def mongo(self):
        connect_uri = f'mongodb://{user}:{password}@{host}:{port}'
        client = pymongo.MongoClient(connect_uri)
        return client

    def filter(self,data):
        '''
        过滤不需要的
        type = 15 债券
        82：科创板
        :param data:
        :return:
        '''
        return None if data['type']==15 else data

    def process_item(self, item, spider):
        if self.filter(item):
            insert_item = dict(item)
            insert_item['crawltime']=datetime.datetime.now()
            self.doc.insert(insert_item)
            return item
        else:
            raise DropItem(item)