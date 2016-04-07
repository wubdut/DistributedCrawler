# coding: UTF-8
import requests
import redis
import time
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
    while True:
        while rserver.llen('crawlQueue') == 0:                                           # waiting zone
            print("waiting")
            time.sleep(3)
            if rserver.get('flag') == '0':
                return

        rserver.incr('flag')                                                             # enter the working zone
        listURL = []
        node = rserver.lpop('crawlQueue')
        if node is None:
            rserver.decr('flag')
            continue
        if node.find(zhuji) == -1:
            rserver.decr('flag')
            continue
        if rserver.sismember('setVisited', node):        # have to check when arrive, or duplicates of "rpush" that wait to go into queue exist.
            rserver.decr('flag')
            continue
        else:
            listURL = parseLink(node)
            if listURL == 'no':
                rserver.decr('flag')
                continue
            rserver.sadd('setVisited', node)
        # print ("I am here: " + node)
        pipe = rserver.pipeline()
        for item in listURL:
            pipe.rpush('crawlQueue', detect(node, item))
        pipe.execute()
        rserver.decr('flag')                                                           # leave working zone
    return

rserver.delete('setVisited')                         # just for server
rserver.delete('flag')                               # just for server
find('http://gs.dlut.edu.cn')
print ('Page: ' + str(rserver.scard('setVisited')))
print('Time: ' + str(rserver.time()[0] - time1) + ' s')
print ("node13 finish jobs (^_^)")
