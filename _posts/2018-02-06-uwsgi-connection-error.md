---
layout: post
title: "uWSGI listen queue 队列溢出的问题"
categories: uwsgi
tags: uwsgi
---

* content
{:toc}

nginx对应也会出现错误***** upstream time out，报错信息为：
*** uWSGI listen queue of socket “127.0.0.1:9001 #注：指定某个固定端口” (fd: 3) full !!! (101/100) ***

改大配置文件中的process和threads即可，默认队列为100，即使最大并发数=100*进程数
网上的做法在docker中不方便修改：

修改/etc/sysctl.conf文件,添加或者修改这几个参数值

	net.core.somaxconn = 262144
	​#表示SYN队列的长度，默认为1024，加大队列长度为8192，可以容纳更多等待连接的网络连接数
	net.ipv4.tcp_max_syn_backlog = 8192
	#网卡设备将请求放入队列的长度
	net.core.netdev_max_backlog = 65536

修改完成之后要记得 sysctl -p 重新加载参数，另外调大uwsgi配置中 --listen=1024的数目是提高并发能力最有效的办法

2018.5.15更新：

	报错：(2003, "Can't connect to MySQL server on 'localhost' ([Errno 99] Cannot assign requested address)")
	修复方法：
	net.ipv4.tcp_tw_reuse = 1

	net.ipv4.tcp_syncookies = 1
	新的连接可以重新使用TIME-WAIT套接字
	net.ipv4.tcp_tw_reuse=1
	启动TIME-WAIT套接字状态的快速循环功能
	net.ipv4.tcp_tw_recycle=1
	套接字关闭时，保持FIN-WAIT-2状态的时间
	net.ipv4.tcp_fin_timeout=30
	对于所有协议的队列，设置最大系统发送缓存(wmen)和接收缓存(rmem)到8M
	net.core.wmem_max=8388608
	net.core.rmem_max=8388608
	
	
2018.05.30 更新
修改max_connections
Ubuntu has moved from Upstart to Systemd from version 15.04 and no longer respects the limits in /etc/security/limits.conf for system services. These limits now apply only to user sessions.

The limits for the MySQL service are defined in the Systemd configuration file, which you should copy from its default location into /etc/systemd and then edit the copy.

sudo cp /lib/systemd/system/mysql.service /etc/systemd/system/
sudo vim /etc/systemd/system/mysql.service # or your editor of choice
Add the following lines to the bottom of the file:

LimitNOFILE=infinity
LimitMEMLOCK=infinity
You could also set a numeric limit, eg LimitNOFILE=4096

Now reload the Systemd configuration with:

sudo systemctl daemon-reload
Restart MySQL and it should now obey the max_connections directive.

然后
/etc/mysql/mysql.conf.d/mysqld.cnf
添加 
[mysqld]
max_connections         = 5000
max_connect_errors      = 10000

非常重要的一点，重启完mysql后，服务器程序也要重启一下，否则连接池里面可能会有异常的连接！！！！

参考：

	https://stackoverflow.com/questions/24884438/2003-cant-connect-to-mysql-server-on-127-0-0-13306-99-cannot-assign-reques
	https://www.percona.com/blog/2014/12/08/what-happens-when-your-application-cannot-open-yet-another-connection-to-mysql/
	https://serverfault.com/questions/829072/cant-connect-to-mysql-server-mysql-server-ip-99
	https://blog.csdn.net/tenfyguo/article/details/8499248
	https://www.digitalocean.com/community/questions/max_connections-will-not-change-in-ubuntu