# -*-coding=utf-8-*-

# @Time : 2019/1/28 16:42
# @File : fangtang_pdf.py
# 下载雪球访谈pdf文件
import requests
from scrapy.selector import Selector
from urllib.request import urlretrieve
import pymongo

db = pymongo.MongoClient('10.18.6.26', port=27001)
doc = db['db_parker']['xueqiu_fangtan']

session = requests.Session()

def find_all_link():
    headers = {'Accept': 'application/json,text/javascript,*/*;q=0.01', 'Accept-Encoding': 'gzip,deflate,br',
               'Accept-Language': 'zh,en;q=0.9,en-US;q=0.8', 'Cache-Control': 'no-cache',
               'Cookie': '_ga=GA1.2.680399679.1547772407;device_id=55dee012d9a4d366e2ebfb04411d019c;s=e6136vjhrp;remember=1;remember.sig=K4F3faYzmVuqC0iXIERCQf55g2Y;xq_a_token=aa0c8a706e8d5ff5137f1b70b47856c9fd809f7a;xq_a_token.sig=UuOvInkvH74cB16wN7jWiYYY6Tk;xqat=aa0c8a706e8d5ff5137f1b70b47856c9fd809f7a;xqat.sig=gNK0P-5BROgVMVGLizGKwdPxhOA;xq_r_token=ae9ef720b3b690889efa96e85dfbdc2b89355c94;xq_r_token.sig=zBMozrvf0Zzy8lC7YVpWIQGhK8I;xq_is_login=1;xq_is_login.sig=J3LxgPVPUzbBg3Kee_PquUfih7Q;u=1733473480;u.sig=2sMTnVmBVOASyCZs6lbVBQ6Zfgs;bid=a8ec0ec01035c8be5606c595aed718d4_jr1bwnx9;Hm_lvt_fe218c11eab60b6ab1b6f84fb38bcc4a=1547772708;__utmz=1.1547773050.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none);aliyungf_tc=AQAAAGxuHQasVA4AD+QRtxdxuDu8Y4NL;Hm_lvt_1db88642e346389874251b5a1eded6e3=1547772407,1547777008,1548664798;_gid=GA1.2.832527761.1548664798;__utma=1.680399679.1547772407.1547773050.1548664815.2;__utmc=1;__utmt=1;Hm_lpvt_1db88642e346389874251b5a1eded6e3=1548665101;__utmb=1.3.10.1548664815',
               'Host': 'xueqiu.com', 'Pragma': 'no-cache', 'Referer': 'https://xueqiu.com/talks/all',
               'User-Agent': 'Mozilla/5.0(WindowsNT6.1;WOW64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/67.0.3396.99Safari/537.36',
               'X-Requested-With': 'XMLHttpRequest'}

    urlx = 'https://xueqiu.com/interview/list/backword.json?page={}'
    for pg in range(7, 329):
        next_url =urlx.format(pg)
        print(next_url)
        try:
            r = session.get(url=next_url, headers=headers)
            ret = r.json()
        except Exception as e:
            # print(r.text)
            print('1')
            print(e)
        else:
            for item in ret.get('interviews'):
                title = item.get('title')
                url = item.get('url')
                try:
                    doc.update({'url': url}, {'$set': {'title': title, 'url': url, 'iscrawl': 0}}, True, True)
                except Exception as e:
                    print(e)
                else:
                    detail_headers = {
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                        'Accept-Encoding': 'gzip,deflate,br', 'Accept-Language': 'zh,en;q=0.9,en-US;q=0.8',
                        'Cache-Control': 'no-cache',
                        'Cookie': '_ga=GA1.2.680399679.1547772407;device_id=55dee012d9a4d366e2ebfb04411d019c;s=e6136vjhrp;remember=1;remember.sig=K4F3faYzmVuqC0iXIERCQf55g2Y;xq_a_token=aa0c8a706e8d5ff5137f1b70b47856c9fd809f7a;xq_a_token.sig=UuOvInkvH74cB16wN7jWiYYY6Tk;xqat=aa0c8a706e8d5ff5137f1b70b47856c9fd809f7a;xqat.sig=gNK0P-5BROgVMVGLizGKwdPxhOA;xq_r_token=ae9ef720b3b690889efa96e85dfbdc2b89355c94;xq_r_token.sig=zBMozrvf0Zzy8lC7YVpWIQGhK8I;xq_is_login=1;xq_is_login.sig=J3LxgPVPUzbBg3Kee_PquUfih7Q;u=1733473480;u.sig=2sMTnVmBVOASyCZs6lbVBQ6Zfgs;bid=a8ec0ec01035c8be5606c595aed718d4_jr1bwnx9;Hm_lvt_fe218c11eab60b6ab1b6f84fb38bcc4a=1547772708;__utmz=1.1547773050.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none);aliyungf_tc=AQAAAGxuHQasVA4AD+QRtxdxuDu8Y4NL;Hm_lvt_1db88642e346389874251b5a1eded6e3=1547772407,1547777008,1548664798;_gid=GA1.2.832527761.1548664798;__utma=1.680399679.1547772407.1547773050.1548664815.2;__utmc=1;Hm_lpvt_1db88642e346389874251b5a1eded6e3=1548665101;__utmb=1.3.10.1548664815',
                        'Host': 'xueqiu.com', 'Pragma': 'no-cache', 'Referer': 'https://xueqiu.com/talks/all',
                        'Upgrade-Insecure-Requests': '1',
                        'User-Agent': 'Mozilla/5.0(WindowsNT6.1;WOW64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/67.0.3396.99Safari/537.36'}

                    try:
                        r_detail = session.get(url=url, headers=detail_headers)
                    except Exception as e:
                        print(e)
                        # print(r.text)

                    else:
                        link = get_pdf(r_detail.text)

                        try:
                            print(link)

                            urlretrieve(link, '{}.pdf'.format(title))
                        except Exception as e:
                            print(e)
                        else:
                            doc.update({'url': url}, {'$set': {'pdf_link': link}}, True, True)


def get_pdf(html):
    response = Selector(text=html)
    link = response.xpath('//*/@data_pdf_name').extract_first()
    return 'http://xqdoc.imedao.com/{}.pdf'.format(link)

find_all_link()