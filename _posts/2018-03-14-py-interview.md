---
layout: post
title: "python面试题"
categories: python
tags: python
---

* content
{:toc}


搜集一些常见python面试题

最近换工作了，准备找python web服务器相关， 虽然上一个项目都是一个人边自学边撸出来的，但毕竟是小项目，有些常见知识会用不到，还是有必要看一些面试题，提高面试通过率。

### 1. 实现python中单例模式
方法1. 使用模块
```
#mysingleton.py
class MySingleton(object):
    def foo(self):
        print("call foo()")

my_singleton = MySingleton()
```
将上面代码保存在mysingleton.py中，然后这样使用
```
from mysingleton import my_singleton
my_singleton.foo()
```

方法2. 使用 __new__
```
class Singleton(object):
    _instance = None
    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kw)
        return cls._instance

class MyClass(Singleton):
    a = 1

a = MyClass()
b = MyClass()
if a == b:
    print("Good Singleton.")
else:
    print("Bad Singleton.")
print(id(one))
print(id(two))
```

方法3. 使用装饰器
```
def singleton(cls):
    instances = {}
    def getinstance(*args, **kw):
        if cls not in instances:
            instances[cls] = cls(*args, **kw);
        return instances[cls]
    return getinstance

@singleton
class MyClass(object):
    a = 1
```

方法4. 使用 metaclass
元类（metaclass）可以控制类的创建过程，它主要做三件事：
拦截类的创建
修改类的定义
返回修改后的类
使用元类实现单例模式的代码如下：
```
class Singleton(type):
    _ins = None
    def __call__(cls, *args, **kw):
        if cls._ins is None:
            cls._ins = super(Singleton, cls).__call__(*args, **kw)
        return cls._ins

#py2
class MyClass(object):
    __metaclass__ = Signleton

#py3
class MyClass(metaclass=Singleton):
    pass
```

### 2. 什么是lambda函数
lambda表达式通常是在需要一个函数，但又不想费神去命名一个函数的场景使用，也就是匿名函数。
例如：
add = lambda x,y: x+y
add(1,2) # result = 3

### 3. python是如何进行内存管理的？
主要有两点 
1. 使用引用计数+标记-清除对象 
2. 需要被清除的基础对象（自定义对象是否会立刻还给OS待确定）不会立刻还给OS（会在适当的时候归还），而是放到一个private memory pool中以便下次使用
需要重点注意循环引用的问题

### 4. 说说decorator的用法和它的应用场景，并写一个decorator
装饰器就是把函数包装一下，为函数添加一些附加功能。装饰器是一个函数，参数为被包装的函数，返回包装后的函数：
```
def dec(fp):
    def _d(*args, **kw):
        print("before call func.")
        r = fp(*args, **kw)
        print("after call func.")
        return r
    return _d

@dec
def func():
    print("call func")

func();

# *** 等价与 ***
def dec(fp):
    def _d(*args, **kw):
        print("before call func.")
        r = fp(*args, **kw)
        print("after call func.")
        return r
    return _d

def func():
    print("call func")

f = dec(func)
f()
```

### 5. Python中pass语句的作用是什么？
pass语句什么也不做，一般作为占位符。

### 6. 名词解释CGI，FastCGI, WSGI
CGI全称是“公共网关接口”(CommonGateway Interface)，HTTP服务器与你的或其它机器上的程序进行“交谈”的一种工具，其程序须运行在网络服务器上。　CGI可以用任何一种语言编写，只要这种语言具有标准输入、输出和环境变量。如php,perl,tcl等。

FastCGI像是一个常驻(long-live)型的CGI，它可以一直执行着，只要激活后，不会每次都要花费时间去fork一次(这是CGI最为人诟病的fork-and-execute模式)。它还支持分布式的运算, 即 FastCGI 程序可以在网站服务器以外的主机上执行并且接受来自其它网站服务器来的请求。

FastCGI是语言无关的、可伸缩架构的CGI开放扩展，其主要行为是将CGI解释器进程保持在内存中并因此获得较高的性能。众所周知，CGI解释器的反复加载是CGI性能低下的主要原因，如果CGI解释器保持在内存中并接受FastCGI进程管理器调度，则可以提供良好的性能、伸缩性、Fail- Over特性等等。

WSGI的全称为： PythonWeb Server Gateway Interface v1.0 （Python Web 服务器网关接口），
它是 Python 应用程序和 WEB 服务器之间的一种接口。它的作用，类似于FCGI 或 FASTCGI 之类的协议的作用。
WSGI 的目标，是要建立一个简单的普遍适用的服务器与 WEB 框架之间的接口。

### 7. python代码得到列表list的交集与并集
b1 = [1,2,3]
b2 = [2,3,4]
# 交集
print([item for item in b1 if item in b2 ])
# 并集
print list(set(a).union(set(b)))

### 8. map, reduce, filter, sorted用法
map()函数接收两个参数，一个是函数，一个是序列，map将传入的函数依次作用到序列的每个元素，并把结果作为新的list返回。
```
>>> def f(x):
...     return x * x
...
>>> map(f, [1, 2, 3, 4, 5, 6, 7, 8, 9])
[1, 4, 9, 16, 25, 36, 49, 64, 81]

>>> map(str, [1, 2, 3, 4, 5, 6, 7, 8, 9])
['1', '2', '3', '4', '5', '6', '7', '8', '9']
```

reduce把一个函数作用在一个序列[x1, x2, x3...]上，这个函数必须接收两个参数，reduce把结果继续和序列的下一个元素做累积计算
```
>>> def add(x, y):
...     return x + y
...
>>> reduce(add, [1, 3, 5, 7, 9])
25

>>> def fn(x, y):
...     return x * 10 + y
...
>>> reduce(fn, [1, 3, 5, 7, 9])
13579
```

filter()也接收一个函数和一个序列。和map()不同的时，filter()把传入的函数依次作用于每个元素，然后根据返回值是True还是False决定保留还是丢弃该元素。
```
def is_odd(n):
    return n % 2 == 1

filter(is_odd, [1, 2, 4, 5, 6, 9, 10, 15])
# 结果: [1, 5, 9, 15]
```

sorted()函数就可以对list进行排序,也可以接收一个比较函数来实现自定义的排序。 与容器内置sort()区别是sort()函数直接修改原对象，而sorted()函数则返回一个新序列。
```
>>> sorted([36, 5, 12, 9, 21])
[5, 9, 12, 21, 36]

def reversed_cmp(x, y):
    if x > y:
        return -1
    if x < y:
        return 1
    return 0
>>> sorted([36, 5, 12, 9, 21], reversed_cmp)
[36, 21, 12, 9, 5]
```

### 9. 标准库线程安全的队列是哪一个？不安全的是哪一个？logging是线程安全的吗？
都是线程安全的。 普通容器如list, tuple, dict, set是非线程安全的。 logging是线程安全的

### 10. 什么是迭代器？
(Iterator)迭代器是带状态的对象,它会记录当前迭代所在的位置,以方便下次迭代的时候获取正确的元素.

### 11. 什么是生成器？
1. 生成器函数
```
def scq(N):
  for i in range(N):
    yield i * 2

for i in scq(5):
  print i
```

2. 生成器表达式
使用列表推倒， 将会一次产生所有结果
s = [x*2 for x in range(5)]
print(s) # [0,2,4,6,8]

将[] => ()，返回生成器表达式
s = (x*2 for x in range(5))
print(s) # <generator object at 0x00B2EC88>
print next(s) # 0
print next(s) # 4
...

生成器的好处是延迟计算，一次返回一个结果。也就是说，它不会一次生成所有的结果，这对于大数据量处理，将会非常有用。
注意事项：生成器只能遍历一次。例如：
```
def scq(N):
  for i in range(N):
    yield i * 2

x = scq(10)
for i in x:
  print i

print("第二次遍历开始")
for i in x:
  print i # 不会打印任何东西
print("第二次遍历结束")
```

### 12. 谈谈python多进程与多线程？
多线程和多进程最大的不同在于，多进程中，同一个变量，各自有一份拷贝存在于每个进程中，互不影响，而多线程中，所有变量都由所有线程共享，所以，任何一个变量都可以被任何一个线程修改，因此，线程之间共享数据最大的危险在于多个线程同时改一个变量，把内容给改乱了。

### 13. 什么是GIL?
GIL(Global Interpreter Lock)，任何Python线程执行前，必须先获得GIL锁，然后，每执行100条字节码，解释器就自动释放GIL锁，让别的线程有机会执行。这个GIL全局锁实际上把所有线程的执行代码都给上了锁，所以，多线程在Python中只能交替执行，即使100个线程跑在100核CPU上，也只能用到1个核。
GIL是Python解释器设计的历史遗留问题，通常我们用的解释器是官方实现的CPython，要真正利用多核，除非重写一个不带GIL的解释器。
所以，在Python中，可以使用多线程，但不要指望能有效利用多核。如果一定要通过多线程利用多核，那只能通过C扩展来实现，不过这样就失去了Python简单易用的特点。
不过，也不用过于担心，Python虽然不能利用多线程实现多核任务，但可以通过多进程实现多核任务。多个Python进程有各自独立的GIL锁，互不影响。
