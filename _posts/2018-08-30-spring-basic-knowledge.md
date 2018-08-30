---
layout: post
title: "Spring框架 - 各种名词解释"
categories: java
tags: java spring DI
---

* content
{:toc}

##### DI
Dependency injection, 依赖注入

根本的目的是解耦，降低对类之间的耦合，底层使用Java语言reflection(反射)机制实现的。那到底什么是DI呢？(待续)

##### IoC
Inversion of Control, 反转控制

一般我们使用一个对象，先是new对象，用完之后，丢给GC回收。但在Spring框架中，所有的类都来我这里注册，你要什么告诉我就行，由Spring统一控制对象生命周期，所以叫反转控制。那到底什么反转了？获得对象的方式反转了。

##### AOP
Aspect-Oriented Programming, 面向切面编程

##### POJO
Plain Old Java Object, 简单老式Java对象

##### wiring
装配
创建应用对象之间协作关系的行为通常称之为装配。

