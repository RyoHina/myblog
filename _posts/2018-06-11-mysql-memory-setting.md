---
layout: post
title: "512MB内存超低配服务器MySQL5.7内存占用调优"
categories: mysql
tags: mysql
---

* content
{:toc}

512MB内存超低配服务器安装mysql5.7，很容易启动失败，设置swap分区启动成功后，经常被oom-killer杀掉，从以下三个方面减少mysql内存占用。

```
修改之前先free -h看一下内存使用情况

1. 开启256MB swap内存
free -h
sudo dd if=/dev/zero of=/swapfile bs=1M count=256
sudo mkswap /swapfile
sudo swapon /swapfile
# 这样swap内存就创建成功了，但是重启后会失效
# 永久保存
sudo vi /etc/fstab
# 文件末尾加入这行内容，保存退出
/swapfile   swap    swap    sw  0   0

2. 设置 vm.swappiness = 70  #这个值越大，越积极使用swap分区，相对应的就是越卡，越不容易被oom-killer杀掉
编辑 vi /etc/sysctl.conf , 保存
sysctl -p 加载配置

3. 调整mysql配置
vi /etc/my.cnf
[mysqld]
wait_timeout = 600
interactive_timeout = 600
log_warnings=1
performance_schema=OFF
table_definition_cache=400 
table_open_cache=256 
保存后重启mysql服务器

都改完之后free -h， 再看一下内存使用情况
```