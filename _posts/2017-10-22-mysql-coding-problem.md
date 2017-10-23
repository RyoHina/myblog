---
layout: post
title: "Ubuntu下解决mysql编码问题
categories: mysql
tags: mysql ubuntu
---

* content
{:toc}

打开 /etc/mysql/mysql.conf.d/mysqld.cnf
添加：
character_set_server = utf8

打开 /etc/mysql/conf.d/mysql.cnf
添加：
[mysql]
default-character-set = utf8

[client]
default-character-set = utf8

重启mysql服务
service mysql restart

进入mysql检查, 如下所示表示修改好了
mysql> show variables like 'collation%';
+----------------------+-----------------+
| Variable_name        | Value           |
+----------------------+-----------------+
| collation_connection | utf8_general_ci |
| collation_database   | utf8_general_ci |
| collation_server     | utf8_general_ci |
+----------------------+-----------------+
3 rows in set (0.00 sec)

mysql> show variables like 'char%';
+--------------------------+----------------------------+
| Variable_name            | Value                      |
+--------------------------+----------------------------+
| character_set_client     | utf8                       |
| character_set_connection | utf8                       |
| character_set_database   | utf8                       |
| character_set_filesystem | binary                     |
| character_set_results    | utf8                       |
| character_set_server     | utf8                       |
| character_set_system     | utf8                       |
| character_sets_dir       | /usr/share/mysql/charsets/ |
+--------------------------+----------------------------+
8 rows in set (0.01 sec)

