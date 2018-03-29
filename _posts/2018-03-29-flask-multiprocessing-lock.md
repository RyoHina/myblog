---
layout: post
title: "uwsgi + flask框架多进程多线程资源锁实现"
categories: flask
tags: flask lock multiprocessing
---

* content
{:toc}

我们知道uwsgi + Flask框架，可以实现多进程，多线程锁有threading.Lock()，多进程有 multiprocessing.Lock()，但是我在实际测试中发现python原生提供的多进程锁在uwsig + flask多进程多线程环境中并不好用。实测代码如下：


```
import multiprocessing
import threading
import time
import redis

rds = redis.Redis()
mutex = multiprocessing.Lock()

class MyThread(threading.Thread):
    # 大概需要执行3秒钟
    def run(self):
        for i in range(100):
            with mutex:
                x = rds.get("lock-test")
                time.sleep(0.03)
                rds.set("lock-test", int(x) + 1)

@app.route('/run', methods=['GET'])
def run():
    t = MyThread()
    t.start()
    return "run function run."

@app.route('/total', methods=['GET'])
def total():
    return str(rds.get("lock-test"))

@app.route('/clear', methods=['GET'])
def clear():
    rds.set("lock-test", 0)
    return "clear!"
```

我们开了4个进程4个线程，uwsgi执行参数如下：
```
uwsgi --socket 127.0.0.1:9001 --chdir mysite --wsgi-file flask_app.py --callable app --pidfile /home/pidfile.pid --master --processes 4 --threads 4 --enable-threads --lazy-apps --daemonize /home/uwsgi.log
```
测试方法：
先执行