# DistributedCrawler
A distributed crawler for web crawling

亟待解决问题:

server和clients对于任务已完成的同步:

1. 初步方案: 在client中设 1)任务区, 2)等待区. server中有一个全局变量, 记录任务区中client数量is_running.
   当看到server中url_queue为空时, 进入等待区:

   a.如果is_running非零, 循环检测url_queue;
   
   b.如果is_running为零, return.
   
   证明: 任务完全结束的充要条件是is_running为0, 并且url_queue空.
   
         必要性: 显然 (本科期间, 充满了爱与恨的两字. 爱是因为考试不用证明了; 恨是因为问学霸怎么证, 他说"显然", 我就懵逼了@~@, 心里充满了崇拜与怨恨).
         
         充分性: (显然不显然)反证, 假设存在任务未完成时, 满足条件:
         
               任务未完成:
               
               1) url_queue有任务, 则url_queue不为空. 不成立;
               
               2) 还有client在执行任务,但没有提交给server, is_running不为0. 不成立.
               
               总之, 只要只要任务没有完成, 就就不可能二者同时为0, 因为client只有把URL提交到server以后才退出任务区.
               
               
         但是还是有问题的: 主要可能出现在通信延时和redis执行顺序上.
         
         1) 假设有两台client, client1检测url_queue为0, 进入等待区; client2处于任务区解析URL. 当client2提交任务后, server上
         可能先执行检测is_running为0, redis还没有将client2的任务加入url_queue, client1退出了(ps: 知道进程通信有什么然并卵, 
         这么一个简单的同步都实践不了. 骚年还要努力啊)
               
         
         

优化的方向:

一. 分布式与通信:

一次自环通信相当于一次list的push操作。所以要尽量减少频繁的通信，将多次通信任务打包成单次通信。

1. dfs 和 bfs

2. redis分布式 和 bfs单机

3. redis管道事物 和 一个个放入队列

4. 查重后放入队列 和 全放入队列(注:放入的也要通信查)

二. I/O分离:

三. 解析速率(beautifulsoup)

四. requests连接速率
   缺点：不支持异步调用，速度慢。可改为urllib, urllib2.
   
集群稳定性:

一. 单点故障:
   由于client都可以访问信号量is_running. 如果某一client死机, 则没有将is_running减1. 就算任务完成, 其他client也会停留在等待区. (待处理)
