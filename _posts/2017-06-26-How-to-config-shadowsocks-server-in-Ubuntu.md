---
layout: post
title: "怎样在Ubuntu系统快速搭建shadowsocks server？"
categories: shadowsocks
tags: shadowsocks-server
---

* content
{:toc}

今天尝试搭建shadowsocks服务器（python版本），发现非常简单。几个步骤就搞定了。开始之前确认服务器能访问被墙的网站, 一般国内的服务器就不要折腾了，除非并不是为了翻墙。

下面开始，假如我们想绑定22222端口。

1.确认服务器对外（也就是入站）TCP端口22222开放，一般是编辑安全组就可以搞定。
	
	类型				协议		端口		来源
	自定义TCP规则  	TCP 	22222	0.0.0.0/0
	自定义TCP规则  	TCP 	22222	::/0

2.安装python环境
	
	apt-get install -y python-pip

3.安装shadowsocks
	
	pip install shadowsocks

4.写一个执行脚本shadowsocks.sh, 然后对这个脚本加上执行权限 "chmod 777 shadowsocks.sh", 脚本内容如下： 

	# 这里为什么要写ssserver全路径呢， 是因为crontab开机启动的时找不到ssserver路径
	/usr/local/bin/ssserver -p 22222 -k your_password -m aes-256-cfb --workers 10 -v -d start	
	
5.加入开机启动

	crontab -e
	@reboot /path/of/shadowsocks.sh

6.Windows客户端连接测试
	
  下载地址：[https://github.com/shadowsocks/shadowsocks-windows](https://github.com/shadowsocks/shadowsocks-windows)

	配置ip： 你服务器的ip
	配置端口：22222
	密码：your_password
	加密方法：aes-256-cfb

好了，可以愉快的翻墙了。。。
	

