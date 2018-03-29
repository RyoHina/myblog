---
layout: post
title: "Ubuntu下uwsgi 使用python3"
categories: uwsgi
tags: uwsgi python3
---

* content
{:toc}

在Ubuntu环境下python默认是2.7版本，而且这个版本是卸载不掉的，uwsgi默认调用的是python2.7，而且uwsgi也没有参数可以指定使用什么python版本，网上查了下说是用插件，研究了半天也没搞明白怎么个用法。偶然发现了一个简单的方法。

1. 创建python3虚拟环境
```
python3 -m venv mysite
```

2. 激活虚拟环境
```
cd mysite
source bin/activate
```

3. 安装好各种包之后，在虚拟环境中执行uwsgi启动web应用就会默认使用python3环境啦！