---
layout: post
title: "ubuntu下MySQL创建一个可以远程登录的用户"
categories: mysql
tags: mysql
---

* content
{:toc}

Command Line：

```
0.以root用户登录mysql
mysql -uroot -p

1.随便创建一个数据库
create database test;

2.创建用户
create user user01@localhost identified by 'your_password';

3.设置权限
grant all privileges on *.* to user01@'%' identified by 'your_password';

4.刷新权限
flush privileges;

5.修改 /etc/mysql/mysql.conf.d/mysqld.cnf
bind-address = 127.0.0.1 改为 bind-address = 0.0.0.0

6.重启mysql
service mysql restart

切忌安全组入方向开放3306端口。

```
