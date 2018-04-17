---
layout: post
title: "Ubuntu下解决mysql编码问题"
categories: mysql
tags: mysql ubuntu
---

* content
{:toc}

打开 /etc/mysql/mysql.conf.d/mysqld.cnf
添加：
```
character_set_server = utf8
```

打开 /etc/mysql/conf.d/mysql.cnf
添加：
```
[mysql]
default-character-set = utf8

[client]
default-character-set = utf8
```

重启mysql服务
```
service mysql restart
```

进入mysql检查, 如下所示则表示改好了

```
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
```
这样修改为utf8后，如果遇到生僻汉字（utf8编码后4个字节）还是会有问题，比如“𡋾”字，插入数据库就会报错。怎么解决这种问题呢？
1. 把上面都修改为utf8都地方都换成utf8mb4， character_set_system 依然是utf8不用管。
2. 
```
    SQL_URI = 'mysql+mysqldb://%s:%s@%s' % (DATABASE_USERNAME, DATABASE_PASSWORD, DATABASE_HOST)
    app.config['SQLALCHEMY_DATABASE_URI'] = SQL_URI + '/%s?charset=utf8mb4' % DATABASE

    conn.execute("CREATE DATABASE IF NOT EXISTS %s CHARACTER SET = 'utf8mb4';" % DATABASE)
```

3. 已有的数据库要手动修改为 utf8mb4， 包括数据库字符设置，表字符设置，还有表里面字符串字段。