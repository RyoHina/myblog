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

参考：
https://stackoverflow.com/questions/24884438/2003-cant-connect-to-mysql-server-on-127-0-0-13306-99-cannot-assign-reques
https://www.percona.com/blog/2014/12/08/what-happens-when-your-application-cannot-open-yet-another-connection-to-mysql/
