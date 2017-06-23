---
layout: post
title: "记录Amazon EC2环境配置nginx + jekyll + https过程"
categories: jekyll
tags: jekyll EC2 nginx https
---

* content
{:toc}


这几天一直想给[kyle.net.cn](https://kyle.net.cn)安装https证书，网上了解到Let's Encrypt免费非常好用，于是试了试，但不小心重试次数太多，只能7天后再申请。无意中发现国内腾讯云和阿里云都提供免费SSL证书一年服务，于是就去阿里云上申请了一个，审核还挺快的，打完一把王者审核就通过了。

<!--more-->

进入阿里云后台控制台->安全(云盾)->证书服务->购买证书，按照操作一步一步来，很快就审核通过了，拿到.pem和.key文件，拷贝到自己的服务器。

接下来配置nginx

	server {
		listen			443 ssl;
		server_name     kyle.net.cn;
		access_log      /home/myblog/nginx_access.log;
		error_log       /home/myblog/nginx_error.log;
		root            /home/myblog;
		
		ssl on;
		ssl_certificate /home/myblog/cert.pem;
		ssl_certificate_key /home/myblog/cert.key;
		ssl_session_timeout 5m;
		ssl_protocols SSLv2 SSLv3 TLSv1;
		ssl_ciphers ALL:!ADH:!EXPORT56:RC4+RSA:+HIGH:+MEDIUM:+LOW:+SSLv2:+EXP;
		ssl_prefer_server_ciphers on;
		
		location / {
			proxy_pass http://localhost:9001;
		}
	}
	
	server {
		listen 80;
		server_name kyle.net.cn;
		return 301 https://$server_name$request_uri;
	}


proxy_pass 转发本地9001端口是因为jekyll项目 _config.yml有如下配置

	host: 0.0.0.0
	port: 9001
然后把80端口转发到https就一切搞定啦！

在此期间遇到一个问题一直没有调通，原来Amazon EC2服务器没有开433端口！！！尴尬，瞬间想撞墙！！！

接下来去[https://www.ssllabs.com/](https://www.ssllabs.com/)做一个检测，发现竟然评分是F！！！
于是查了一些资料做了一些nginx修改：

	server {
		listen 443 ssl http2;
		listen [::]:443 ssl http2;
		server_name kyle.net.cn www.kyle.net.cn;
		access_log /home/myblog/nginx_access.log;
		error_log /home/myblog/nginx_error.log;
		root /home/myblog;
		
		ssl on;
		ssl_certificate /home/myblog/cert.pem;
		ssl_certificate_key /home/myblog/cert.key;
		ssl_dhparam /home/myblog/dhparam.pem;
		ssl_protocols TLSv1.2 TLSv1.1 TLSv1;
		ssl_ciphers EECDH+AESGCM:EDH+AESGCM:EECDH:EDH:!MD5:!RC4:!LOW:!MEDIUM:!CAMELLIA:!ECDSA:!DES:!DSS:!3DES:!NULL;
		ssl_prefer_server_ciphers on;

		ssl_session_cache off;
		ssl_session_timeout 10m;
		ssl_session_tickets off;
		
		add_header Strict-Transport-Security "max-age=63072000; includeSubdomains; preload";
		add_header X-Frame-Options DENY;
		add_header X-Content-Type-Options nosniff;
		
		location / {
			proxy_pass http://localhost:9001;
		}
	}

	server {
		listen 80;
		listen [::]:80;
		server_name kyle.net.cn www.kyle.net.cn;
		return 301 https://$server_name$request_uri;
	}

附一张图：
![](https://blog.kyle.net.cn/ssllabs-A+.png)
