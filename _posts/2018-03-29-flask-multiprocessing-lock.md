---
layout: post
title: "uwsgi + flask框架多进程多线程资源锁实现"
categories: flask
tags: flask lock multiprocessing
---

* content
{:toc}

我们知道uwsgi + Flask框架，可以实现多进程，多线程。常见线程锁有threading.Lock()，进程锁有multiprocessing.Lock()，但是我在实际测试中发现python原生提供的多进程锁在uwsig + flask多进程多线程环境中并不好用。实测代码如下：


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

在一个单核CPU的阿里云Ubuntu服务器，我开了4个进程4个线程，uwsgi执行参数如下：
```
uwsgi --socket 127.0.0.1:9001 --chdir mysite --wsgi-file flask_app.py --callable app --pidfile /home/pidfile.pid --master --processes 4 --threads 4 --enable-threads --lazy-apps --daemonize /home/uwsgi.log
```
测试方法：
先在浏览器上运行/clear链接，然后运行/run链接若干次（我是用两个浏览器和Postman，几乎同时访问3~5次），然后打开/total链接，每刷新一次数字都有增加，等一会数字稳定了，结果最终数字不是100的整数，说明这个进程锁是错的。

下面我们尝试使用文件锁。
```
# Not work for windows
import fcntl
class FLock(object):
    def __init__(self, lock_file):
        self.lock_file = "/tmp/" + lock_file

    def require(self):
        self.fn = open(self.lock_file, "w")
        fcntl.flock(self.fn.fileno(), fcntl.LOCK_EX)

    def release(self):
        self.fn.close()


mutex = FLock("pis-project")
class MyThread(threading.Thread):
    def run(self):
        for i in range(100):
            mutex.require()
            x = rds.get("lock-test")
            time.sleep(0.03)
            rds.set("lock-test", int(x) + 1)
            mutex.release()
```
发现这样依然有问题，最后total出来的数据也不是100的整数。。。为什么呢？
后来我写了这样一段代码：
```
# Not work for windows
import fcntl
class FLock(object):
    def __init__(self, lock_file):
        self.lock_file = "/tmp/" + lock_file

    def require(self):
        self.fn = open(self.lock_file, "w")
        fcntl.flock(self.fn.fileno(), fcntl.LOCK_EX)

    def release(self):
        self.fn.close()


mutex = FLock("pis-project")

mutex.require()
print("require")

mutex.require()
print("require")

mutex.release()
print("release")
```
发现竟然能一路跑下来， 恍然大悟，原来我们的文件锁可以锁进程，但无法锁同一个进程里的不同线程。
所以再加一个线程锁，最终版本是这样的：
```
# Not work for windows
import fcntl
import threading
class FLock(object):
    def __init__(self, lock_file):
        self.lock_file = "/tmp/" + lock_file
        self.thread_lock = threading.Lock()

    def require(self):
        self.thread_lock.acquire()
        self.fn = open(self.lock_file, "w")
        fcntl.flock(self.fn.fileno(), fcntl.LOCK_EX)

    def release(self):
        self.fn.close()
        self.thread_lock.release()
```

这样测试下来，total始终是100的整数，说明我们的锁是正确的。
那能否使用multiprocessing.Lock + threading.Lock 实现需求呢？
```
import multiprocessing
import threading
class FLock(object):
    def __init__(self):
        self.thread_lock = threading.Lock()
        self.process_lock = multiprocessing.Lock()

    def require(self):
        self.thread_lock.acquire()
        self.process_lock.acquire()

    def release(self):
        self.process_lock.release()
        self.thread_lock.release()
```
经过测试发现这样也是正确的。结论是如果没有多线程，只用一个进程锁就可以了。 如果是多进程+多线程就必须要两个锁了。
