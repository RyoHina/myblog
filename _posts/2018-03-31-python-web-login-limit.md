---
layout: post
title: "Python Web服务器登录模块如何防止被字典攻击？"
categories: python
tags: login
---

* content
{:toc}


rds = redis.Redis() # 这里用到了redis
```
# 从收到登录请求开始...
...
# ****** 后台登录次数限制 ******
# 两分钟内只能请求10次, 不同ip不会相互影响，防止被攻击后影响正常用户
cur_timestamp = int(time.time())
timestamp_key = "login_timestamp" + request.remote_addr
times_key = "login_times" + request.remote_addr
if rds.get(timestamp_key) is None:
	rds.set(timestamp_key, cur_timestamp, ex=10 * 60)

if rds.get(times_key) is None:
	rds.set(times_key, 0, ex=10 * 60)

if cur_timestamp - int(rds.get(timestamp_key)) > 2 * 60:
	rds.set(times_key, 1, ex=10 * 60)
	rds.set(timestamp_key, cur_timestamp, ex=10 * 60)
else:
	if int(rds.get(times_key)) > 10:
		return '{"status":%d, "errmsg":"登录太频繁了，请2分钟后重试！"}' % ERR_UNKNOWN
	rds.incr(times_key, 1)
# ****** 后台登录次数限制 ******
# 后续验证账户密码匹配等操作...
...
```