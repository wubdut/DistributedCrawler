#!/bin/bash
python server.py
sleep 3

ssh -f -n -l hadoop node13 'python /home/hadoop/workspace/DistributedCrawler/crawl.py &' # 后台运行ssh
pid=$(ps aux | grep "ssh -f -n -l hadoop node13 python /home/hadoop/workspace/DistributedCrawler/crawl.py" | awk '{print $2}' | sort -n | head -n 1) # 获取进程号
echo "ssh command is running, pid:${pid}"
sleep 3 && kill ${pid} && echo "ssh command is complete" # 延迟3秒后执行kill命令，关闭ssh进程，延迟时间可以根据调用的命令不同调整

ssh -f -n -l hadoop node14 'python /home/hadoop/workspace/DistributedCrawler/crawl.py &' # 后台运行ssh
pid=$(ps aux | grep "ssh -f -n -l hadoop node14 python /home/hadoop/workspace/DistributedCrawler/crawl.py" | awk '{print $2}' | sort -n | head -n 1) # 获取进程号
echo "ssh command is running, pid:${pid}"
sleep 3 && kill ${pid} && echo "ssh command is complete" # 延迟3秒后执行kill命令，关闭ssh进程，延迟时间可以根据调用的命令不同调整

ssh -f -n -l hadoop node15 'python /home/hadoop/workspace/DistributedCrawler/crawl.py &' # 后台运行ssh
pid=$(ps aux | grep "ssh -f -n -l hadoop node15 python /home/hadoop/workspace/DistributedCrawler/crawl.py" | awk '{print $2}' | sort -n | head -n 1) # 获取进程号
echo "ssh command is running, pid:${pid}"
sleep 3 && kill ${pid} && echo "ssh command is complete" # 延迟3秒后执行kill命令，关闭ssh进程，延迟时间可以根据调用的命令不同调整

ssh -f -n -l hadoop node16 'python /home/hadoop/workspace/DistributedCrawler/crawl.py &' # 后台运行ssh
pid=$(ps aux | grep "ssh -f -n -l hadoop node16 python /home/hadoop/workspace/DistributedCrawler/crawl.py" | awk '{print $2}' | sort -n | head -n 1) # 获取进程号
echo "ssh command is running, pid:${pid}"
sleep 3 && kill ${pid} && echo "ssh command is complete" # 延迟3秒后执行kill命令，关闭ssh进程，延迟时间可以根据调用的命令不同调整

ssh -f -n -l hadoop node18 'python /home/hadoop/workspace/DistributedCrawler/crawl.py &' # 后台运行ssh
pid=$(ps aux | grep "ssh -f -n -l hadoop node18 python /home/hadoop/workspace/DistributedCrawler/crawl.py" | awk '{print $2}' | sort -n | head -n 1) # 获取进程号
echo "ssh command is running, pid:${pid}"
sleep 3 && kill ${pid} && echo "ssh command is complete" # 延迟3秒后执行kill命令，关闭ssh进程，延迟时间可以根据调用的命令不同调整

exit 0

#gnome-terminal -x bash -c "redis-server"
#sleep 3
# python server.py
# sleep 3
# ssh hadoop@node13 'python /home/hadoop/workspace/DistributedCrawler/crawl.py'
# ssh hadoop@node14 'python /home/hadoop/workspace/DistributedCrawler/crawl.py'
# ssh hadoop@node15 'python /home/hadoop/workspace/DistributedCrawler/crawl.py'
# ssh hadoop@node16 'python /home/hadoop/workspace/DistributedCrawler/crawl.py'
# ssh hadoop@node18 'python /home/hadoop/workspace/DistributedCrawler/crawl.py'
