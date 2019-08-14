# -*- coding: utf-8 -*-
import datetime
import scrapy
import json
from postman.items import PostmanItem,FullItem


class XueqiuSpider(scrapy.Spider):
    name = 'xueqiu'

    def __init__(self, *args, **kwargs):
        super(XueqiuSpider, self).__init__(*args, **kwargs)

        self.headers = {
            'Accept-Language': ' zh-CN,zh;q=0.9', 'Accept-Encoding': ' gzip, deflate, br',
            'X-Requested-With': ' XMLHttpRequest', 'Host': ' xueqiu.com', 'Accept': ' */*',
            'User-Agent': ' Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36',
            'Connection': ' keep-alive',
            'Pragma': ' no-cache', 'Cache-Control': ' no-cache', 'Referer': ' https://xueqiu.com/u/6146070786'
        }

        self.cookies = {
            "_ga": "GA1.2.8758030.1510556188",
            "s": "ec11hzadsn",
            "device_id": "5f39ce5780ab1a6a35cc9507efd53276",
            "__utmz": "1.1543137928.193.8.utmcsr",
            "bid": "a8ec0ec01035c8be5606c595aed718d4_jpb9qusd",
            "__utma": "1.8758030.1510556188.1559486551.1564417180.204",
            "aliyungf_tc": "AQAAAMMpax+EOgAADCAmG/8JTZvB5val",
            "Hm_lvt_1db88642e346389874251b5a1eded6e3": "1564672543,1564754874,1565412065,1565700484",
            "remember": "1",
            "xq_a_token": "7dc8e0cc8c22a73f3d7afb92e78bced74e93b0b0",
            "xqat": "7dc8e0cc8c22a73f3d7afb92e78bced74e93b0b0",
            "xq_r_token": "a57b481f7467e3b2b6f0a36e98df642ac4cf6c37",
            "xq_is_login": "1",
            "u": "5633284888",
            "snbim_minify": "true",
            "Hm_lpvt_1db88642e346389874251b5a1eded6e3": "1565700661",
        }

        self.base_url = 'https://xueqiu.com/v4/statuses/user_timeline.json?page={}&user_id={}'
        self.userid = 9887656769
        self.maxPage = 378
    def start_requests(self):

        yield scrapy.Request(self.base_url.format(1,self.userid), cookies=self.cookies, headers=self.headers,callback=self.parse_total_item,
                             meta={'pn':1}
                             )

    def parse_total_item(self,response):
        pn = response.meta['pn']

        content = json.loads(response.body_as_unicode())
        tweets = content.get('statuses', None)
        print('current page {}'.format(pn))
        if tweets is None:
            print('tweet is empty, current pn is {}'.format(pn))
            return


        for tweet in tweets:
            item = FullItem()
            created_at = tweet.get('created_at')
            edited_at = tweet.get('edited_at')
            try:
                created_at=datetime.datetime.fromtimestamp(int(created_at) / 1000)
            except Exception as e:
                print(created_at)
            try:
                edited_at=datetime.datetime.fromtimestamp(int(edited_at) / 1000)

            except Exception as e:
                print(edited_at)


            tweet['created_at']=created_at
            tweet['edited_at']=edited_at
            tweet['crawltime']=datetime.datetime.now()
            item['DATA'] = tweet
            yield item

        if pn<self.maxPage:
            pn+=1
            yield scrapy.Request(self.base_url.format(pn,self.userid), cookies=self.cookies, headers=self.headers, callback=self.parse_total_item,
                                 meta={'pn':pn})


    def parse(self, response):
        content = json.loads(response.body_as_unicode())
        tweets = content.get('statuses', None)
        if tweets is None:
            return

        for tweet in tweets:
            item = PostmanItem()
            _id = tweet.get('id')
            userid = tweet.get('userid')
            title = tweet.get('title')
            created_at = tweet.get('created_at')
            created_at = datetime.datetime.fromtimestamp(int(created_at) / 1000)
            retweet_count = tweet.get('retweet_count')
            reply_count = tweet.get('reply_count')
            fav_count = tweet.get('fav_count')
            truncated = tweet.get('truncated')
            commentId = tweet.get('commentId')
            symbol_id = tweet.get('symbol_id')
            description = tweet.get('description')
            source_link = tweet.get('source_link')
            user = tweet.get('user')
            target = tweet.get('target')
            timeBefore = tweet.get('timeBefore')
            text = tweet.get('text')
            source = tweet.get('source')
            retweeted_status = tweet.get('retweeted_status')
            item['_id'] = _id
            item['userid'] = userid
            item['title'] = title
            item['created_at'] = created_at
            item['retweet_count'] = retweet_count
            item['reply_count'] = reply_count
            item['fav_count'] = fav_count
            item['truncated'] = truncated
            item['commentId'] = commentId
            item['symbol_id'] = symbol_id
            item['description'] = description
            item['source_link'] = source_link
            item['user'] = user
            item['target'] = target
            item['timeBefore'] = timeBefore
            item['text'] = text
            item['source'] = source
            item['retweeted_status'] = retweeted_status
            yield item
