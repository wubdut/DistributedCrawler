# coding: UTF-8
import requests
import redis
import time
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

t1 = time.time()

rserver = redis.Redis('localhost')
rserver.delete('setVisited')                         # just for server
rserver.delete('crawlQueue')                         # just for server
rserver.delete('flag')                               # just for server

netSite = 'http://gs.dlut.edu.cn'
rserver.rpush('crawlQueue', netSite)

while True:
    print("working......: " + str(int(time.time()-t1)) + 's')
    time.sleep(10)
    pipe = rserver.pipeline()

    pipe.multi()
    pipe.llen('crawlQueue')
    pipe.get('flag')                                                     #这里要考虑原子性, 等待过程中其他client可能退出,但queue已不为0
    out = pipe.execute()
    if out[0] == 0 and out[1] == '0':
        break

t2 = time.time()

print ("time: " + str(int(t2-t1)))
print("page: " + str(rserver.scard('setVisited')))
