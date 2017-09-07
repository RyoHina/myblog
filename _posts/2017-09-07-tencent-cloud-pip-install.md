---
layout: post
title: "解决腾讯云服务器pip install死慢死慢的问题"
categories: pip
tags: pip python
---

* content
{:toc}

今天搞了个腾讯云服务器，发现pip安装包的时候死慢死慢，后来发现是pipy源在国外导致的， 搜了搜国内的源并没有找到靠谱的。
突然灵光一闪，打开我的阿里云服务器，发现了阿里的pipy源，于是就抄了过来。。。

```
cd ~
mkdir .pip
cd .pip
touch pip.conf

# 然后写入下面内容，保存退出，速度嗷嗷快！
[global]
index-url=http://mirrors.aliyun.com/pypi/simple/

[install]
trusted-host=mirrors.aliyun.com
```
