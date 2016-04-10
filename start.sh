#gnome-terminal -x bash -c "redis-server"
#sleep 3
#gnome-terminal -x bash -c "python server.py"
#sleep 3
ssh hadoop@node13 'python /home/hadoop/workspace/DistributedCrawler/crawl.py > client.log'
ssh hadoop@node14 'python /home/hadoop/workspace/DistributedCrawler/crawl.py > client.log'
ssh hadoop@node15 'python /home/hadoop/workspace/DistributedCrawler/crawl.py > client.log'
ssh hadoop@node16 'python /home/hadoop/workspace/DistributedCrawler/crawl.py > client.log'
ssh hadoop@node18 'python /home/hadoop/workspace/DistributedCrawler/crawl.py > client.log'
