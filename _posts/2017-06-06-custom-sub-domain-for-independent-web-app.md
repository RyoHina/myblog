---
layout: post
title: "如何为子域名配置一个单独web app？"
categories: nginx 
tags: ubuntu nginx
---

* content
{:toc}


本博客的域名是 kyle.net.cn 在后台服务器对应一个web app，怎样对一个子域名（test.kyle.net.cn）单独配置一个web app呢？
#### 1. 添加子域名解析 ####

	添加一条test子域名解析记录
	记录类型    主机记录     记录值
	A          test        120.120.120.120


<!--more-->

#### 2. 修改nginx对子域名的配置 ####
在 /etc/nginx/sites-enabled 目录下添加文件 test.kyle.net.cn.conf, 内容是：

	server {
	    listen          80;
	    server_name     test.kyle.net.cn;
	    access_log      /home/mysite-test/nginx_access.log;
	    error_log       /home/mysite-test/nginx_error.log;
	    root            /home/mysite-test/static;
	    location / {
	        uwsgi_pass      127.0.0.1:9002;
	        include         uwsgi_params;
	        uwsgi_param     UWSGI_SCHEME $scheme;
	        uwsgi_param     SERVER_SOFTWARE    nginx/$nginx_version;
	    }
	}


uwsgi_pass 参数端口要与其他的app区分开
#### 3. 启动uwsgi ####

	uwsgi --socket 127.0.0.1:9002 --chdir ./ --wsgi-file flask_app.py --callable app --pidfile pidfile.pid --master --processes 2 --threads 2


这样就可以用子域名 test.kyle.net.cn 访问一个单独的web app了。
