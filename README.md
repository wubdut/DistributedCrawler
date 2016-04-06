# DistributedCrawler
A distributed crawler for web crawling

亟待解决问题:

server和clients对于任务已完成的同步:

1. 初步方案: 在client中设 1)任务区, 2)等待区. server中有一个全局变量, 记录任务区中client数量is_running.
   当看到server中url_queue为空时, 进入等待区:

   a.如果is_running非零, 循环检测url_queue;
   
   b.如果is_running为零, return.

优化的方向:

一. 分布式与通信:

一次自环通信相当于一次list的sadd操作。所以要尽量减少频繁的通信，将多次通信任务打包成单次通信。

1. dfs 和 bfs

2. redis分布式 和 bfs单机

3. redis管道事物 和 一个个放入队列

4. 查重后放入队列 和 全放入队列(注:放入的也要通信查)

二. I/O分离:

三. 解析速率(beautifulsoup)

四. requests连接速率
