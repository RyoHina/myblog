---
layout: post
title: "MySQL thread-safe get_or_create function"
categories: mysql
tags: mysql
---

* content
{:toc}

MySQL数据库如何创建一个线程安全的get_or_create方法？

```
# 这里用到了sqlalchemy
def get_or_create(param1):
    try:
        db.session.execute('LOCK TABLES table_name WRITE;')
        a = TableName.query.filter_by(param1=param1).first()
        if a is None:
            a = TableName(param1)
            db.session.add(a)
            db.session.commit()
        db.session.execute('UNLOCK TABLES;')
        return a
    except Exception, e:
        logging.error("xxx.py get_or_create exception:" + str(e))
    return None
```
SQL语句‘LOCK TABLES table_name WRITE;’不能重入，保证了被lock/unlock包裹的代码段只能同时被一个线程执行。