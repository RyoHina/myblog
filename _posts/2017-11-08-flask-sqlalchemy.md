---
layout: post
title: "Flask-Sqlalchemy使用过程中一个诡异问题"
categories: flask-sqlalchemy
tags: flask-sqlalchemy
---

* content
{:toc}

今天项目在做测试的时候发现日志会报错。报错内容是“This result object does not return rows. It has been closed automatically”，而报错的位置确是最普通的一些查询操作，非常诡异。搜索了半天没有什么收获。

示例代码如下：

flask_app.py主工程文件：
```
from base import db

app = Flask(__name__)
db.app = app
db.init_app(app)
add_system_log(0, int(time.time()), u'服务器启动成功...', "", "")
```

base.py内容：
```
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
```

其中add_system_log代码如下：
```
def add_system_log(stype, timestamp, description, ip, user_agent):
    try:
        sys_log = SystemLog(stype, timestamp, description, ip, user_agent)
        db.session.add(sys_log)
        db.session.commit()
    except Exception, e:
        logging.error("commondb.py add_system_log exception:" + str(e))
```
而出差的位置不是上述代码，而是一些普通的请求中的简单查询操作。

我仔细对比了官方给的例子发现例子中并没有db.app = app这句话。但是我去掉这句话后，add_system_log就会报错，报错内容是“application not registered on db instance and no applicationbound to current context”。

最终我的解决方案是:
1. 去掉db.app = app
2. 去掉add_system_log

但是不知道什么原因导致最开始的报错，猜测是db对象(即SQLAlchemy对象)还没初始化完全就开始使用，从而导致后面的一些报错。