gnome-terminal -x bash -c "redis-server"
sleep 3
gnome-terminal -x bash -c "python server.py"
sleep 3
ssh hadoop@node13 '/home/hadoop/workspace/DistributedCrawler/crawl > client.log'
ssh hadoop@node14 '/home/hadoop/workspace/DistributedCrawler/crawl > client.log'
ssh hadoop@node15 '/home/hadoop/workspace/DistributedCrawler/crawl > client.log'
ssh hadoop@node16 '/home/hadoop/workspace/DistributedCrawler/crawl > client.log'
ssh hadoop@node18 '/home/hadoop/workspace/DistributedCrawler/crawl > client.log'
