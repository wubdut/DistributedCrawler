# coding: UTF-8
import requests
import redis
import time
import os
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
zhuji = rserver.get('zhuji')
file = open('/home/hadoop/workspace/DistributedCrawler/logs/client', 'w')

file.write('come here \n')
def detect(base, url):
    url1 = urljoin(base, url)
    arr = urlparse(url1)
    path = normpath(arr[2])
    return str(urlunparse((arr.scheme, arr.netloc, path, arr.params, arr.query, arr.fragment)))

def parseLink(node):
    global file
    try:
        ret = requests.get(node)
        if ret.status_code >= 400: #这里不一定只是200,需要了解状态码后确定.以及ip限制的代理问题
            return []
    except Exception as e:
        file.write("客户端或服务器错误:" + node + "\n")
        return ['no']
    myset = set()
    soup = BeautifulSoup(ret.text) #, "html.parser")
    for item in soup.find_all('a'):
        myset.add(item.get('href'))
    return list(myset)

def find():
    global zhuji, rserver
    while True:
        while rserver.llen('crawlQueue') == 0:                                           # waiting zone
            file.write("waiting\n")
            time.sleep(3)
            pipe = rserver.pipeline()
            pipe.multi()
            pipe.llen('crawlQueue')
            pipe.get('flag')                                                     #这里要考虑原子性, 等待过程中其他client可能退出,但queue已不为0
            out = pipe.execute()
            if out[0] == 0 and out[1] == '0':
                return

        listURL = []
        pipe = rserver.pipeline()
        pipe.multi()
        pipe.incr('flag')                                                             # enter the working zone
        pipe.lpop('crawlQueue')
        node = pipe.execute()[1]
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
        pipe.multi()
        for item in listURL:
            tmp = detect(node, item)
            if not rserver.sismember('setVisited', tmp):
                pipe.rpush('crawlQueue', tmp)                                         #此处要有隔离
        pipe.decr('flag')                                                             # leave working zone
        pipe.execute()
    return

find()
file.write ("node13 finish jobs (^_^)\n")
file.close()
if rserver.get('returnServer') == '0':
    os.system("ssh wubin@192.168.2.108 'python /home/wubin/workspace/py/DistributedCrawler/finish.py'")
    rserver.incr('returnServer')
