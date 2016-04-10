# coding: UTF-8
import requests
import redis
import time
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

t1 = int(rserver.get('time1'))

t2 = int(time.time())

print ("page: " + str(rserver.scard('setVisited')))
print ("time: " + str(t2-t1))
