# -*-coding=utf-8-*-

# @Time : 2018/10/23 9:26
# @File : money_reward.py
import requests
from collections import OrderedDict
import time
import datetime
import pymongo
import config
client = pymongo.MongoClient('10.18.6.46', 27001)
db = client['xueqiu']
failed_doc = db['reward_failed']

# 根据不同用户修改
ZHUAN_LAN='zhuanlan_元卫南'
user_id='2227798650'

session = requests.Session()
def get_proxy(retry=10):
    proxyurl = 'http://{}:8081/dynamicIp/common/getDynamicIp.do'.format(config.PROXY)
    count = 0
    for i in range(retry):
        try:
            r = requests.get(proxyurl, timeout=10)
        except Exception as e:
            print(e)
            count += 1
            print('代理获取失败,重试' + str(count))
            time.sleep(1)

        else:
            js = r.json()
            proxyServer = 'http://{0}:{1}'.format(js.get('ip'), js.get('port'))
            proxies_random = {
                'http': proxyServer
            }
            return proxies_random


def get_content(url):
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh,en;q=0.9,en-US;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Cookie":"_ga=GA1.2.8758030.1510556188; s=ec11hzadsn; device_id=5f39ce5780ab1a6a35cc9507efd53276; __utmz=1.1543137928.193.8.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); bid=a8ec0ec01035c8be5606c595aed718d4_jpb9qusd; __utma=1.8758030.1510556188.1559486551.1564417180.204; aliyungf_tc=AQAAAMMpax+EOgAADCAmG/8JTZvB5val; Hm_lvt_1db88642e346389874251b5a1eded6e3=1564672543,1564754874,1565412065,1565700484; remember=1; xq_a_token=7dc8e0cc8c22a73f3d7afb92e78bced74e93b0b0; xqat=7dc8e0cc8c22a73f3d7afb92e78bced74e93b0b0; xq_r_token=a57b481f7467e3b2b6f0a36e98df642ac4cf6c37; xq_is_login=1; u=5633284888; snbim_minify=true; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1565700661",
        # "Cookie": "_ga=GA1.2.1120330993.1533803771; device_id=45dc0a51a26fc3078e5d8636d5141178; aliyungf_tc=AQAAABUPpRGD+w0AOnFoypiKi1AgLha3; Hm_lvt_1db88642e346389874251b5a1eded6e3=1538060166,1539759418; s=ev17xxecme; _gid=GA1.2.489835841.1540172180; remember=1; remember.sig=K4F3faYzmVuqC0iXIERCQf55g2Y; xq_a_token=0a093a7b60eeaf5abb3468ebb1827ab37492829a; xq_a_token.sig=Ugrl-_BEM5Ed2K1tThP4B9xd-WI; xqat=0a093a7b60eeaf5abb3468ebb1827ab37492829a; xqat.sig=cC3oDwhUgpI-cY_nx4o-fIir8ag; xq_r_token=7147aa65f965bdfd68872710923386e22d547761; xq_r_token.sig=WZ_zkORdsy2K2ngXNlFRV6DkcCg; xq_is_login=1; xq_is_login.sig=J3LxgPVPUzbBg3Kee_PquUfih7Q; u=1733473480; u.sig=2sMTnVmBVOASyCZs6lbVBQ6Zfgs; bid=a8ec0ec01035c8be5606c595aed718d4_jnl1zufy; _gat_gtag_UA_16079156_4=1; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1540258247",
        "Host": "xueqiu.com",
        "Pragma": "no-cache",
        "Referer": "https://xueqiu.com/2227798650/115496801",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }


    try:
        r = session.get(url=url, headers=headers,timeout=10)
    except Exception as e:
        print(e)
        r = None
    return r


def parse_content(post_id):
    url = 'https://xueqiu.com/statuses/reward/list_by_user.json?status_id={}&page=1&size=99999999'.format(post_id)
    r = get_content(url)

    if r.status_code != 200:
        print('status code != 200')
        failed_doc.update({'post_id':post_id},{'post_id':post_id,'status':0},True,True)
        return None

    try:

        js_data = r.json()
    except Exception as e:
        print(e)
        print('can not parse to json')
        print(post_id)
        failed_doc.update({'post_id':post_id},{'post_id':post_id,'status':0},True,True)
        return

    ret = []
    been_reward_user = '元卫南'
    for item in js_data.get('items'):
        name = item.get('name')
        amount = item.get('amount')
        description = item.get('description')
        user_id = item.get('user_id')
        created_at = item.get('created_at')
        if created_at:
            created_at = datetime.datetime.fromtimestamp(int(created_at) / 1000).strftime('%Y-%m-%d %H:%M:%S')

        d = OrderedDict()
        d['name'] = name
        d['user_id'] = user_id
        d['amount'] = amount / 100
        d['description'] = description
        d['created_at'] = created_at
        d['been_reward'] = been_reward_user
        d['origin_post_id']=post_id
        ret.append(d)

    if ret:
        db['reward'].insert_many(ret)
        failed_doc.update({'post_id':post_id},{'post_id':post_id,'status':1},True,True)


# 获取所有的文章
def get_all_article():

    get_page_url = 'https://xueqiu.com/statuses/original/timeline.json?user_id={}&page={}'.format(user_id,1)
    r = get_content(get_page_url)
    max_page = int(r.json().get('maxPage'))

    for i in range(1, max_page + 1):
        url = get_page_url.format(i)
        r = get_content(url)
        js_data = r.json()
        ret = []

        for item in js_data.get('list'):
            d = OrderedDict()

            d['article_id'] = item.get('id')
            d['title'] = item.get('title')
            d['description'] = item.get('description')
            d['view_count'] = item.get('view_count')
            d['target'] = 'https://xueqiu.com/' + item.get('target')
            d['user_id']= item.get('user_id')
            d['created_at'] = datetime.datetime.fromtimestamp(int(item.get('created_at')) / 1000).strftime(
                '%Y-%m-%d %H:%M:%S')

            ret.append(d)

        db[ZHUAN_LAN].insert_many(ret)
        time.sleep(5)

def loop_article():
    ret = db[ZHUAN_LAN].find({},{'article_id':1})
    failed_ret = failed_doc.find({'status':1})
    article_id_list =[]

    for i in failed_ret:
        article_id_list.append(i.get('article_id'))

    for item in ret:
        article_id = item.get('article_id')
        # print(article_id)
        article_id_list=[]
        if article_id in article_id_list:
            continue
        else:
            time.sleep(3)
            parse_content(article_id)

get_all_article()
# post_id = '115496801'
# parse_content(post_id)
# loop_article()