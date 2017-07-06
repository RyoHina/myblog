---
layout: post
title: "C++返回局部静态对象引用会调用拷贝构造函数"
categories: c++
tags: c++
---

* content
{:toc}

C++返回局部静态对象引用会调用拷贝构造函数吗？
今天佳何从野鸡博客上看了一个c++单例的实现，代码：

```
static RoomManager& getInstance() {
	static RoomManager mgr;
	return mgr;
};
```


<!--more-->


我看了一下，感觉应该没有问题，调试发现每次调用getInstance返回的竟然不是同一个对象，于是写了个例子
```
#include "stdio.h"

class RoomManager {
public:
	static RoomManager& getInstance() {
		static RoomManager mgr;
		return mgr;
	};
	int _index;

	//构造函数
	RoomManager() {
		printf("Roommanager() default.\n");
	}

	//拷贝构造函数
	RoomManager(const RoomManager &other) {
		printf("Roommanager() copy.\n");

		if (this == &other) {
			return;
		}
		this->_index = other._index;
	}

	void test() {
		printf("addr:%.8x  \n", this);
	}
};

int main()
{
	auto a = RoomManager::getInstance();
	a.test();
	auto b = RoomManager::getInstance();
	b.test();

    return 0;
}
```

输出：
```
Roommanager() default.
Roommanager() copy.
addr:0021fef4
Roommanager() copy.
addr:0021fee8
```
看来"返回局部静态对象引用"是会调用拷贝构造函数从而返回一个临时对象。
修改为下面这种写法，就能避免每次调用都执行拷贝构造函数
```
static RoomManager* getInstance() {
	static RoomManager mgr;
	return &mgr;
};
```

当然，这样也不是完全正确，如果getInstance函数在多个线程同时执行，RoomManager默认构造函数可能会执行多次。但在逻辑上可以避免这种情况发生，比如在进程开启初始化逻辑中，执行一下getInstance，保证没有其他线程竞争，就可以避免这种线程不安全的情况发生。
正确C++单例实现：
```
static RoomManager* getInstance() {
	lock(); //不可重入锁，类似Windows临界区
	static RoomManager mgr;
	unlock(); //解锁
	return &mgr;
};
```

----- 更新 -----：
其实拷贝构造函数，是"auto a=..."赋值引起的，并不是“返回静态局部对象引用”会返回一个拷贝构造临时对象。好久不写c++都忘了。。。
原始的写法，把main修改为这样就不会有问题。
```
int main()
{
	RoomManager::getInstance().test();
	//a.test();
	RoomManager::getInstance().test();
	//b.test();

    return 0;
}
```
其实是单例应该把 构造函数，拷贝构造函数，赋值运算符都设置为私有的，比如这样：
```
private:
  RoomManager() { printf("Roommanager() default.\n"); }
  RoomManager(const RoomManager&);
  RoomManager & operator=(const RoomManager&); 
```
这样，“auto a=RoomManager::getInstance();”就会报错，在编译阶段就可以避免一些可能出现的问题。
