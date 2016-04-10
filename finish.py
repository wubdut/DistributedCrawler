# coding: UTF-8
import requests
import redis
import time
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

rserver = redis.Redis('localhost')
file = open('/home/wubin/workspace/py/DistributedCrawler/logs/server', 'w')

t1 = int(rserver.get('time1'))
t2 = int(time.time())

file.write("page: " + str(rserver.scard('setVisited')) + "\n")
file.write("time: " + str(t2-t1) + " s\n")

file.close()
