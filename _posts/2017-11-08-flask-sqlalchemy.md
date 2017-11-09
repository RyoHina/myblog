---
layout: post
title: "Flask-Sqlalchemy使用过程中一个诡异问题"
categories: flask-sqlalchemy
tags: flask-sqlalchemy
---

* content
{:toc}

今天项目在做测试的时候发现了一个日志报错。报错内容是“This result object does not return rows. It has been closed automatically”，而报错的位置确是最普通的一些查询操作，非常诡异。
我的生产环境是Ubuntu + nginx + uwsgi, uwsgi执行脚本如下(注意多线程环境)：
```
uwsgi --socket 127.0.0.1:9001 --chdir mysite --wsgi-file flask_app.py --callable app --pidfile /home/labor/pidfile.pid --master --processes 2 --threads 2
```

示例代码如下：

flask_app.py主工程文件：
```
from base import db

app = Flask(__name__)
db.app = app
db.init_app(app)
add_system_log(0, int(time.time()), u'服务器启动成功...', "", "")
...
if __name__ == '__main__':
	...
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
然而报错的位置并不在上述代码中，而是一些普通请求中的简单查询操作。

我仔细对比了官方给的例子发现例子中并没有db.app = app这句话。但是我去掉这句话后，add_system_log就会报错，报错内容是“application not registered on db instance and no applicationbound to current context”。

经过一些资料查找，找到了两个解决方案:
##### 方案1：
```
1). 去掉db.app = app
2). 去掉add_system_log 
缺点：不能在项目启动过程中操作数据库, 启动完成后，在get/post请求中操作
```

##### 方案2：
```
修改uwsgi执行脚本(添加了 --enable-threads --lazy-apps)：
uwsgi --socket 127.0.0.1:9001 --chdir mysite --wsgi-file flask_app.py --callable app --pidfile /home/labor/pidfile.pid --master --processes 2 --threads 2 --enable-threads --lazy-apps
缺点：第一次启动会有数据库不存在的exception，后续每次启动会有两条'服务器启动成功'日志。
```

我最终选择用方案2.

参考资料：
1. [https://stackoverflow.com/questions/20933018/random-errors-with-sqlalchemy](https://stackoverflow.com/questions/20933018/random-errors-with-sqlalchemy)
2. [https://stackoverflow.com/questions/17317344/celery-and-sqlalchemy-this-result-object-does-not-return-rows-it-has-been-clo](https://stackoverflow.com/questions/17317344/celery-and-sqlalchemy-this-result-object-does-not-return-rows-it-has-been-clo)
3. [http://docs.sqlalchemy.org/en/latest/faq/connections.html#mysql-server-has-gone-away](http://docs.sqlalchemy.org/en/latest/faq/connections.html#mysql-server-has-gone-away)
4. [https://stackoverflow.com/questions/44476678/uwsgi-lazy-apps-and-threadpool](https://stackoverflow.com/questions/44476678/uwsgi-lazy-apps-and-threadpool)
