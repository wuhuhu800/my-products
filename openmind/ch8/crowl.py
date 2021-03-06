
from urllib.request import quote
from bs4 import BeautifulSoup
import requests
import re
import json


class Wx_spider(object):

    def __init__(self,key):
        '''
        初始化函数
        '''
        #搜索地址
        self.key = key
        self.sougou_search_url = 'http://weixin.sogou.com/weixin?type=1&query={}&ie=utf8&s_from=input&page={}&_sug_=n&_sug_type_='
        #headers 目的模拟浏览器访问
        self.headers ={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
        # 代理池接口
        self.proxy_url = 'http://' #需要搞一个虚拟机用一下，目的获取代理ip

    #def get_proxy(self):
    #    '''
    #    请求代理池，随机返回ip
    #    '''
    #    text = requests.get(self.proxy_url).text
    #    proxy = {'http':'http://{}'.format(text),
    #    'https':'https://{}'.format(text)
    #    }
    #    print('当前代理是：http://{}'.format(text))
    #    return proxy

    def get_search_response(self,url,proxy=None,total=3):
        try:
            content = requests.get(url,headers = self.headers).content #,proxies = proxy).content#二进制服务器响应内容
            #参考（http://docs.python-requests.org/zh_CN/latest/user/quickstart.html#id4）
            #响应头的内容（http://docs.python-requests.org/zh_CN/latest/user/quickstart.html#id8）
            #响应对象内容（http://docs.python-requests.org/zh_CN/latest/user/advanced.html#request-and-response-objects）

        except Exception as e:
            print('代理异常，重生')
            total -=1
            return self.get_search_response(url,total=total)#proxy=self.get_proxy(),)

        #if '输入验证码' in content.decode():
        #    total -=1
        #    return self.get_search_response(url,total=total)#proxy=self.get_proxy(),)
        #else:
        #    print('返回错误值')

        return content  #.decode()#decode研究一下这个用法

        #取到公众号的链接
    def get_wx_hkmovie(self,sougou_response):
        soup = BeautifulSoup(sougou_response.decode(),'lxml')
        #for i in soup.find_all('div',class_= 'txt-box'):

        return [i.find('p',class_= 'tit').find('a')['href'] for i in soup.find_all('div',class_= 'txt-box')]

    def get_wx_article(self,response):#获取到链接内容
        req = re.compile(r'var msgList = (.*?}}]});',re.S)
        article_urls = re.findall(req,response.decode())
        #print("this is req",req)
        #print('this is article_urls',article_urls)
        return json.loads(article_urls[0])

    def parse_article(self,response):#解析
        article_list = response.get('list')
        articles = []
        for article in article_list:
            article_author = article.get('app_msg_ext_info').get('author')
            article_url = article.get('app_msg_ext_info').get('content_url')
            article_title = article.get('app_msg_ext_info').get('title')
            article_addtime = article.get('comm_msg_info').get('datetime')
            print(article_author)
            print(article_url)
            print(article_title)
            print(article_addtime)

            break



    def main(self):
        content = self.get_search_response(self.sougou_search_url.format(self.key,1)) #获取链接

#第一步利用模拟浏览器行为，输入公众号链接，获取服务器响应的内容
        for url in (self.get_wx_hkmovie(content)):

#第二步从服务器的响应内容中，取（匹配）出列表里每一个公众号详情页的链接
            html = self.get_search_response(url)
            print('this is html',html)
#第三步通过获取链，利用模拟浏览器行为取出详情页服务器响应的内容
            article_dict = self.get_wx_article(html)
#第四步通过正则匹配出所需要的内容的位置，获取该部分内容
            self.parse_article(article_dict)
#第五步将返回的jasn解析，取出值

            break

if __name__ =='__main__':
    key =input('请输入要搜索的内容:')
    spider = Wx_spider(key)
    spider.main()
