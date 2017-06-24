---
layout: post
title: "怎样为sqlite表设置一个自定义自增值？"
categories: database
tags: sqlite
---

* content
{:toc}

类似MySQL比较重一点的数据库，实现自定义自增值，在创建表的时候指定 AUTO_INCREMENT = 1000 就可以了。而sqlite这样非常轻量级的数据库，并不支持在创建表的时候就指定初始自增值，默认是从1开始自增。假如我们希望主键id从1000自增，有下面两种方法

<!--more-->

方法1：

	CREATE TABLE user (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(60));
	INSERT INTO user(id, name) VALUES (999, "nnnn");
	DELETE FROM user WHERE id=999;

方法2：
	
	CREATE TABLE user (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(60));
	REPLACE INTO sqlite_sequence (name, seq) VALUES ('user', 999);

网上有人说 REPLACE INTO 这句可以换成下面这句，我试了并不行
因为此时sqlite_sequence表还没有name='user'数据，UPDATE语句执行失败了。
而 REPLACE INTO的语义是存在则修改，不存在则插入。

	UPDATE SQLITE_SEQUENCE SET seq = 999 WHERE name = 'user';


当然，我们推荐方法2，方法1怎么都像是野路子。

参考资料：

[https://stackoverflow.com/questions/692856/set-start-value-for-autoincrement-in-sqlite](https://stackoverflow.com/questions/692856/set-start-value-for-autoincrement-in-sqlite)
