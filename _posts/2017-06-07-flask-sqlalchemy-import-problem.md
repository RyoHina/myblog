---
layout: post
title: "使用flask-sqlalchemy扩展后，如何把Model类定义文件分散在不同的文件夹？"
categories: flask
tags: flask
author: kyle
---

* content
{:toc}


先看官方给的例子
<!--more-->

	from flask import Flask
	from flask_sqlalchemy import SQLAlchemy
	
	DATABASE_USERNAME = 'root'
	DATABASE_PASSWORD = '***'
	DATABASE_HOST = 'localhost'
	DATABASE = 'testdb'
	
	app = Flask(__name__)
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://%s:%s@%s:3306/%s' % \
	                                        (DATABASE_USERNAME, DATABASE_PASSWORD, DATABASE_HOST, DATABASE)
	db = SQLAlchemy(app)
	
	class User(db.Model):
	    id = db.Column(db.Integer, primary_key=True)
	    username = db.Column(db.String(80), unique=True)
	    email = db.Column(db.String(120), unique=True)
	
	    def __init__(self, username, email):
	        self.username = username
	        self.email = email
	
	    def __repr__(self):
	        return '<User %r>' % self.username
	
	db.create_all()
	dog = User("Mr.Dog", "liyanhong@baidu.com")
	db.session.add(dog)
	db.session.commit()

但是假如我们想把User类定义在其他文件中要怎么做呢？ User类构造需要db对象，很自然我们可能会这样写：
main.py

	from flask import Flask
	from flask_sqlalchemy import SQLAlchemy
	from model import User
	
	DATABASE_USERNAME = 'root'
	DATABASE_PASSWORD = '***'
	DATABASE_HOST = 'localhost'
	DATABASE = 'testdb'
	
	
	app = Flask(__name__)
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://%s:%s@%s:3306/%s' % \
	                                        (DATABASE_USERNAME, DATABASE_PASSWORD, DATABASE_HOST, DATABASE)
	db = SQLAlchemy(app)
	
	db.create_all()
	dog = User("Mr.Dog", "liyanhong@baidu.com")
	db.session.add(dog)
	db.session.commit()

model.py

	from main import db

	
	class User(db.Model):
	    id = db.Column(db.Integer, primary_key=True)
	    username = db.Column(db.String(80), unique=True)
	    email = db.Column(db.String(120), unique=True)
	
	    def __init__(self, username, email):
	        self.username = username
	        self.email = email
	
	    def __repr__(self):
	        return '<User %r>' % self.username

Run起来发现会报错：

	ImportError: cannot import name User

为什么呢？ 很简单，这样写会造成循环import。 查了一些资料找到了解决方案： main.py model.py basemodel.py 在同一个目录下

main.py

	from flask import Flask
	from basemodel import db
	from model import User
	
	DATABASE_USERNAME = 'root'
	DATABASE_PASSWORD = '***'
	DATABASE_HOST = 'localhost'
	DATABASE = 'testdb'
	
	app = Flask(__name__)
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://%s:%s@%s:3306/%s' % \
	                                        (DATABASE_USERNAME, DATABASE_PASSWORD, DATABASE_HOST, DATABASE)
	db.app = app
	db.init_app(app)
	
	db.create_all()
	dog = User("Mr.Dog", "liyanhong@baidu.com")
	db.session.add(dog)
	db.session.commit()

model.py

	from basemodel import db
	
	
	class User(db.Model):
	    id = db.Column(db.Integer, primary_key=True)
	    username = db.Column(db.String(80), unique=True)
	    email = db.Column(db.String(120), unique=True)
	
	    def __init__(self, username, email):
	        self.username = username
	        self.email = email
	
	    def __repr__(self):
	        return '<User %r>' % self.username

basemodel.py

	from flask_sqlalchemy import SQLAlchemy

	db = SQLAlchemy()

怎样从已知数据库导出SQLAlchemy Class呢？

	pip install sqlacodegen
	sqlacodegen mysql://"root":"***"@localhost:3306/testdb --outfile tables.py

参考资料：

[https://stackoverflow.com/questions/9692962/flask-sqlalchemy-import-context-issue](https://stackoverflow.com/questions/9692962/flask-sqlalchemy-import-context-issue)

[http://www.pythondoc.com/flask-sqlalchemy/quickstart.html](http://www.pythondoc.com/flask-sqlalchemy/quickstart.html)

[https://github.com/svieira/Budget-Manager](https://github.com/svieira/Budget-Manager)