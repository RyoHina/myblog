---
layout: post
title: "Ubuntu 16.04.2下配置nginx + uwsgi + flask + mysql"
categories: flask
tags: flask ubuntu nginx uwsgi mysql
---

* content
{:toc}


#### 0.准备工作 ####
	sudo apt-get update     # 更新配置文件
	sudo apt-get upgrade    # 安装更新

<!--more-->

如果没有这一步后面安装某些软件可能会出错。
#### 1.安装flask ####
	pip install flask       # 安装flask

#### 2.安装并配置 nginx  ####
	sudo apt-get install nginx

在目录 '/etc/nginx/sites-enabled' 下新建文件 'kyle.net.cn.conf‘’, 内容设置为:

	server {
	    listen          80;
	    server_name     kyle.net.cn www.kyle.net.cn;
	    access_log      /home/nginx_access.log;
	    error_log       /home/nginx_error.log;
	    root            /home/mysite;
	    location / {
	        uwsgi_pass      127.0.0.1:9001;
	        include         uwsgi_params;
	        uwsgi_param     UWSGI_SCHEME $scheme;
	        uwsgi_param     SERVER_SOFTWARE    nginx/$nginx_version;
	    }
	    
	    # 静态文件直接转发
	    # css|js|ico|gif|jpg|jpeg|png|txt|html|htm|xml|swf|wav这些都是静态文件
	    # 但应分辨，js、css可能经常会变，过期时间应小一些，图片、html基本不变，过期时间可以设长一些  
	    location ~* ^.+\.(ico|gif|jpg|jpeg|png)$ {
	        root         /home/mysite;  
	        access_log   off;  
	        expires      30d;  
	    }  
	
	    location ~* ^.+\.(css|js|txt|xml|swf|wav)$ {
	        root        /home/mysite;  
	        access_log   off;  
	        expires      24h;  
	    }
	
	    location ~ ^/favicon\.ico$ {
	        log_not_found off;
	        access_log   off;  
	        root   work;
	    }
	}


#### 3.安装并配置uwsgi ####
	sudo apt-get install uwsgi
	pip install uwsgi

新建flask_app.py, 内容为：

	from flask import Flask
	app = Flask(__name__)
	
	@app.route(&quot;/&quot;)
	def hello():
	    return 'Hello, Flask!'


由uwsgi启动flask web应用，注意--socket配置和nginx配置 uwsgi_pass保持一致，完成反向代理和负载均衡。这样我们就启动了2个flask进程(每个进程就是一个worker)，每个进程有2个线程。

	uwsgi --socket 127.0.0.1:9001 --wsgi-file flask_app.py --callable app --master --processes 2 --threads 2;


#### 4.安装MySQL python环境 ####
	sudo apt-get install python-setuptools
	sudo apt-get install libmysqld-dev
	sudo apt-get install libmysqlclient-dev
	sudo apt-get install python-dev
	pip install mysql-python


在shell中输入python，打开python交互窗口，执行&quot;import MySQLdb&quot;(注意大小写)不报错的话，就证明安装好了。
