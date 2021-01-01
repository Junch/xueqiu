# -*- coding: utf-8 -*-
# @Time : 2020/12/30 16:16
# @File : hot_stock.py
# @Author : Rocky C@www.30daydo.com

'''
热门股
'''
import datetime
import numpy as np
import pymongo
import sys
sys.path.append('..')
from configure.settings import send_from_aliyun
from config import user, password, host, port
import pandas as pd

class HotStock():

    def __init__(self):
        self.db = self.client()['xueqiu']


    def init_data(self):
        # mongo获取数据
        today = datetime.datetime.now()
        yesterday = today + datetime.timedelta(days=-1)
        today_str = today.strftime('%Y-%m-%d')
        self.today_str=today_str
        yesterday_str = yesterday.strftime('%Y-%m-%d')

        self.today_stock = self.stock_info(today_str)
        self.yesterday_stock=self.stock_info(yesterday_str)
        self.yesterday_stock.rename(columns={'followers':'old_followers'},inplace=True)

    def trend(self):
        self.init_data()
        df = pd.merge(self.today_stock,self.yesterday_stock,on='symbol',how='left')
        df['diff']=df['followers']-df['old_followers']
        df['diff_percent']=round(df['diff']/df['old_followers']*100,2)
        df=df[['name_x','followers','diff','diff_percent']]
        df=df.replace([np.inf, -np.inf], np.nan)
        df.dropna(inplace=True)
        df['followers']=df['followers'].astype(np.int32)
        df['diff']=df['diff'].astype(np.int32)
        df_count=df.sort_values(by='diff',ascending=False).head(10)
        df_percent=df.sort_values(by='diff_percent',ascending=False).head(10)
        return df_count,df_percent

    def stock_info(self,collection):
        stocks = self.db[collection].find({},{'name':1,'followers':1,'_id':0,'symbol':1})
        return pd.DataFrame(list(stocks))


    def client(self):
        connect_uri = f'mongodb://{user}:{password}@{host}:{port}'
        client = pymongo.MongoClient(connect_uri)
        return client

    def html(self):
        df_count,df_percent = self.trend()
        return df_count.to_html() + df_percent.to_html()

    def send_mail(self):
        html = self.html()
        title=f'{self.today_str} 雪球趋势'
        send_from_aliyun(title,html,types='html')

def main():
    app = HotStock()
    app.send_mail()

if __name__ == '__main__':
    main()
