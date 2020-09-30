---
layout: post
title: "使用宝塔面板在CentOS系统上部署nodejs项目"
categories: node
tags: node
---

* content
{:toc}

在生成环境中，一般不直接使用nodejs框架的静态文件部署功能，专业的工具做专业的事情，静态文件就交给nginx吧。
0. 安装宝塔面板，安装完成后选择LNMP，因为我们要用nginx
1. 推荐使用宝塔面板->软件商店->PM2管理器 安装node环境。 当然也可以"yum install -y nodejs" 自行安装
2. 将node项目随便放在什么地方，运行起来，端口监听8090
3. 创建网站，PHP版本->选择"纯静态"，目录选择node项目的public文件夹
4. 点击网站设置，选择反向代理，添加反向代理，点击右侧高级功能
```
	代理名称: app
	代理目录: /appservice/
	目标URL: http://127.0.0.1:8090		发送域名: $host
```

注意1:目标URL结尾一定不能带/, 否则会报错
注意2:目标URL中的端口与第2步的监听端口保持一致

5. 点击刚刚添加代理的配置文件，修改 location /appservice/ 下面的 proxy_pass
```
	proxy_pass http://127.0.0.1:8090;  修改为
	proxy_pass http://127.0.0.1:8090/;
	
	否则nginx转发给node应用会带"appservice"路径
```
