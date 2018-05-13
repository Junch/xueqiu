# -*- coding: utf-8 -*-
import datetime
import scrapy
import json
from postman.items import PostmanItem

class XueqiuSpider(scrapy.Spider):
    name = 'xueqiu'
    allowed_domains = ['xueqiu.com']

    # start_urls = ['http://xueqiu.com/']
    def __init__(self):
        self.headers = {
            'Accept-Language': ' zh-CN,zh;q=0.9', 'Accept-Encoding': ' gzip, deflate, br',
            'X-Requested-With': ' XMLHttpRequest', 'Host': ' xueqiu.com', 'Accept': ' */*',
            'User-Agent': ' Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36',
            'Connection': ' keep-alive',
            'Pragma': ' no-cache', 'Cache-Control': ' no-cache', 'Referer': ' https://xueqiu.com/u/1955602780'

        }

        # self.cookies={'Cookie': ' device_id=f174304eb593fc036db5db25d3124fad; s=e31245o8yi; bid=a8ec0ec01035c8be5606c595aed718d4_j9xsz38j; remember=1; remember.sig=K4F3faYzmVuqC0iXIERCQf55g2Y; xq_a_token=f57a2e24d323f2c27ec40d3ac26ee9a10e1857dc; xq_a_token.sig=-3diSs4C6X4-m1mC-h618cAeWj4; xq_r_token=7ceedf9c41c4b6d4054d6f25c1ca3087e40483a2; xq_r_token.sig=XtalVKjjXjLzRRBR0HwHAjfH3N0; xq_is_login=1; xq_is_login.sig=J3LxgPVPUzbBg3Kee_PquUfih7Q; u=1733473480; u.sig=2sMTnVmBVOASyCZs6lbVBQ6Zfgs; __utmz=1.1524820182.167.7.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; aliyungf_tc=AQAAACK8rRyK8gYAAyAmG3lNK4rFWjui; __utma=1.8758030.1510556188.1525936226.1526117855.176; __utmc=1; __utmt=1; Hm_lvt_1db88642e346389874251b5a1eded6e3=1525403929,1525410601,1525929687,1526117855; __utmb=1.5.10.1526117855; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1526117884; snbim_minify=true'}
        # self.cookies={'Cookie':'device_id=f174304eb593fc036db5db25d3124fad; s=e31245o8yi; bid=a8ec0ec01035c8be5606c595aed718d4_j9xsz38j; remember=1; remember.sig=K4F3faYzmVuqC0iXIERCQf55g2Y; xq_a_token=f57a2e24d323f2c27ec40d3ac26ee9a10e1857dc; xq_a_token.sig=-3diSs4C6X4-m1mC-h618cAeWj4; xq_r_token=7ceedf9c41c4b6d4054d6f25c1ca3087e40483a2; xq_r_token.sig=XtalVKjjXjLzRRBR0HwHAjfH3N0; xq_is_login=1; xq_is_login.sig=J3LxgPVPUzbBg3Kee_PquUfih7Q; u=1733473480; u.sig=2sMTnVmBVOASyCZs6lbVBQ6Zfgs; __utmz=1.1524820182.167.7.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; aliyungf_tc=AQAAACK8rRyK8gYAAyAmG3lNK4rFWjui; __utma=1.8758030.1510556188.1525936226.1526117855.176; __utmc=1; __utmt=1; Hm_lvt_1db88642e346389874251b5a1eded6e3=1525403929,1525410601,1525929687,1526117855; __utmb=1.5.10.1526117855; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1526117884; snbim_minify=true'}
        self.cookies = {"device_id": "f174304eb593fc036db5db25d3124fad",
                        "s": "e31245o8yi",
                        "bid": "a8ec0ec01035c8be5606c595aed718d4_j9xsz38j",
                        "remember": "1",
                        "remember.sig": "K4F3faYzmVuqC0iXIERCQf55g2Y",
                        "xq_a_token": "f57a2e24d323f2c27ec40d3ac26ee9a10e1857dc",
                        "xq_a_token.sig": "-3diSs4C6X4-m1mC-h618cAeWj4",
                        "xq_r_token": "7ceedf9c41c4b6d4054d6f25c1ca3087e40483a2",
                        "xq_r_token.sig": "XtalVKjjXjLzRRBR0HwHAjfH3N0",
                        "xq_is_login": "1",
                        "xq_is_login.sig": "J3LxgPVPUzbBg3Kee_PquUfih7Q",
                        "u": "1733473480",
                        "u.sig": "2sMTnVmBVOASyCZs6lbVBQ6Zfgs",
                        "__utmz": "1.1524820182.167.7.utmcsr",
                        "aliyungf_tc": "AQAAACK8rRyK8gYAAyAmG3lNK4rFWjui",
                        "__utma": "1.8758030.1510556188.1525936226.1526117855.176",
                        "__utmc": "1",
                        "__utmt": "1",
                        "Hm_lvt_1db88642e346389874251b5a1eded6e3": "1525403929,1525410601,1525929687,1526117855",
                        "__utmb": "1.5.10.1526117855",
                        "Hm_lpvt_1db88642e346389874251b5a1eded6e3": "1526117884",
                        "snbim_minify": "true"
                        }

    def start_requests(self):
        count = 20
        userid = 1955602780
        # maxPage = 2
        maxPage = 1796
        base_url = 'https://xueqiu.com/v4/statuses/user_timeline.json?page={}&user_id={}'
        for pn in range(1, maxPage + 1):
            url = base_url.format(pn, userid)
            yield scrapy.Request(url, cookies=self.cookies, headers=self.headers)

    def parse(self, response):
        content = json.loads(response.body_as_unicode())
        tweets = content.get('statuses',None)
        if tweets is None:
            return 
        
        for tweet in tweets:
            item = PostmanItem()
            _id = tweet.get('id')
            userid = tweet.get('userid')
            title = tweet.get('title')
            created_at = tweet.get('created_at')
            created_at = datetime.datetime.fromtimestamp(long(created_at)/1000)
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
            item['_id']=_id
            item['userid']=userid
            item['title']=title
            item['created_at']=created_at
            item['retweet_count']=retweet_count
            item['reply_count']=reply_count
            item['fav_count']=fav_count
            item['truncated']=truncated
            item['commentId']=commentId
            item['symbol_id']=symbol_id
            item['description']=description
            item['source_link']=source_link
            item['user']=user
            item['target']=target
            item['timeBefore']=timeBefore
            item['text']=text
            item['source']=source
            item['retweeted_status']=retweeted_status
            yield item