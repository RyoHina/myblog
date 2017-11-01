---
layout: post
title: "MySQL 怎样检测某数据库是否存在？"
categories: mysql
tags: mysql
---

* content
{:toc}

第一种方法，就是使用SQL语句"SHOW DATABASES;", 根据其结果判断是否某数据库存在即可。
python版sqlalchemy实现：

```
	engine = create_engine(sql_uri)
	conn = engine.connect()
	conn.execute("commit")
	existing_databases = conn.execute("SHOW DATABASES;")
	existing_databases = [d[0] for d in existing_databases]
	if DATABASE in existing_databases:
		# exist
		pass
	else:
		# NOT exist
		pass
	conn.close()
```

第二种方法是在sqlalchemy-utils包源码中学到的，代码如下

```
	engine = create_engine(sql_uri)
	text = ("SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA "
			"WHERE SCHEMA_NAME = '%s'" % database)
	return bool(engine.execute(text).scalar())
```