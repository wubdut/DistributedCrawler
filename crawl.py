# coding: UTF-8
import requests
import redis
from bs4 import BeautifulSoup
from urlparse import urljoin
from urlparse import urlparse
from urlparse import urlunparse
from posixpath import normpath
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

rserver = redis.Redis('192.168.2.108')
time1 = rserver.time()[0]
zhuji = 'gs.dlut.edu.cn'

def detect(base, url):
    url1 = urljoin(base, url)
    arr = urlparse(url1)
    path = normpath(arr[2])
    return str(urlunparse((arr.scheme, arr.netloc, path, arr.params, arr.query, arr.fragment)))

def parseLink(node):
    try:
        ret = requests.get(node)
        if ret.status_code >= 400: #这里不一定只是200,需要了解状态码后确定.以及ip限制的代理问题
            return []
    except Exception as e:
        print ("客户端或服务器错误:" + node)
        return ['no']
    myset = set()
    soup = BeautifulSoup(ret.text, "html.parser")
    for item in soup.find_all('a'):
        myset.add(item.get('href'))
    return list(myset)

def find(netSite=''):
    global zhuji, rserver
    rserver.rpush('crawlQueue', netSite)
    while rserver.llen('crawlQueue'):
        listURL = []
        node = rserver.lpop('crawlQueue')
        if node.find(zhuji) == -1:
            continue
        if rserver.sismember('setVisited', node):
            continue
        else:
            listURL = parseLink(node)
            if listURL == 'no':
                continue
            rserver.sadd('setVisited', node)
        # print ("I am here: " + node)
        for item in listURL:
            rserver.rpush('crawlQueue', detect(node, item))
    return

rserver.delete('setVisited')
find('http://gs.dlut.edu.cn')
print ('Page: ' + str(rserver.scard('setVisited')))
print('Time: ' + str(rserver.time()[0] - time1) + ' s')
print ("node13 finish jobs (^_^)")
