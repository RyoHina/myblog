---
layout: post
title: "Web服务器怎么保存用户名密码？"
categories: algorithm
tags: algorithm security
---

* content
{:toc}


Web服务器用户名密码存储方式不当导致的信息安全事故时有发生，到底怎么存才是安全的呢？ 我思考了一个非常容易实现，安全性也还凑合的实现。

前端（App端，微信端等）代码：

	md5str = hex_md5("明文密码" + "client salt1 hard to guess...").toLowerCase();
	md5str = hex_md5(md5str + "client salt2 hard to guess...").toLowerCase();
	//接下来，把md5str发给服务器

<!--more-->

如你所见，其实这个salt1和salt2是完全暴露的，所以服务器端还要做一些事情：

	md5str = hex_md5("前端发过来的密码" + "server salt1 hard to guess...").toLowerCase();
	md5str = hex_md5(md5str + "server salt2 hard to guess...").toLowerCase();
	//接下来，把md5str存到数据库


我们从下面几个维度衡量服务器安全性：

1. 劫持用户请求，密码明文会泄漏吗？  (✖)
2. 劫持用户请求，能伪造登录请求通过验证吗？  (✔)
3. 数据库泄漏了，密码明文会泄漏吗？  (✖)
4. 数据库泄漏了，能伪造登录请求通过验证吗？  (✖)
5. 数据库泄漏 + 代码泄漏，密码明文会泄漏吗？ (✖?)
6. 数据库泄漏 + 代码泄漏，能伪造登录请求通过验证吗？ (✖?)

如果我们启用https，劫持用户数据的情况基本不会发生。但就本实现而言，一旦被劫持就可以伪造登录请求通过验证，所以对于2是不安全的。

单单数据库泄漏了，黑客是做不了什么事情的，因为不知道服务器端salt。

为什么5，6会打个问号呢？如果数据库和代码同时泄漏了，黑客可以用彩虹表攻击，可以在很短的时间内把弱密码都抓出来, 伪代码如下：
	

	def get_real_pass(p):
		# 原本只在客户端计算
		md5str = hex_md5(p + "client salt1 hard to guess...").toLowerCase();
		md5str = hex_md5(md5str + "client salt2 hard to guess...").toLowerCase();
		# 原本只在服务器端计算
		md5str = hex_md5(md5str + "server salt1 hard to guess...").toLowerCase();
		md5str = hex_md5(md5str + "server salt2 hard to guess...").toLowerCase();
		return md5str

	list = [...大量的弱明文密码字典...]
	for p in list:
		real_pass = get_real_pass(p))
		if real_pass in 数据库密码字段:
			print ("找到明文："+ p)


所以，只要密码位数够长(比如18位大小写字母和数字)，即使黑客拿到数据库+代码也无济于事，啥也干不了（因为位数越高爆破难度就越大）。

本例中的md5可以换成更复杂的sha-1等算法，盐可以更长一些。 在没被黑客拿到代码的情况下会显著提高安全性。

怎样把2，5，6的安全隐患消除呢？ 这就要采用更加复杂的流程和算法了。比如HMAC算法。 

HMAC算法简介：

(-待续-)