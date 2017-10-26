---
layout: post
title: "Cookie字段解释"
categories: cookie
tags: cookie
---

* content
{:toc}

HTTP请求Response Header字段如下
```
accept-ranges:bytes
cache-control:public, max-age=43200
date:Thu, 26 Oct 2017 05:33:47 GMT
etag:"1508741996.79-8997-4145288068"
expires:Thu, 26 Oct 2017 17:33:47 GMT
server:nginx/1.10.3 (Ubuntu)
set-cookie:session=eyJfcGVybWFuZW50Ijp0cnVlLCJhcHBfbWFuYWdlcl9zZXNzaW9uX2tleSI6eyIgYiI6IlJYVnNRV3RFTUhnelpHNXZOWEZOU0ZwVldqUXdXRGwyVUROQlVXMWtSWGRyT0VrMiJ9fQ.DNMFOw.xywAq7tBglj_NPgLRPZaptNB_N0; Expires=Thu, 02-Nov-2017 05:33:47 GMT; HttpOnly; Path=/
status:304
strict-transport-security:max-age=63072000; includeSubdomains; preload
x-content-type-options:nosniff
x-frame-options:DENY
```

这里主要解释set-cookie字段内容
```
session=eyJfcGVybWFuZW50Ijp0cnVlLCJhcHBfbWFuYWdlcl9zZXNzaW9uX2tleSI6eyIgYiI6IlJYVnNRV3RFTUhnelpHNXZOWEZOU0ZwVldqUXdXRGwyVUROQlVXMWtSWGRyT0VrMiJ9fQ.DNMFOw.xywAq7tBglj_NPgLRPZaptNB_N0; Expires=Thu, 02-Nov-2017 05:33:47 GMT; HttpOnly; Path=/
```
session值,其实就是我们常说的sessionid

Expires是指过期时间

HttpOnly是指不允许使用js(类似document.cookie)获取cookie数据，能有效防止XSS攻击，降低cookie被窃取的风险。

Path是指浏览器存储cookie路径

secure是指必须使用https通信，http通信将不附带cookie数据


session字段数据被'.'分为三个段

第一段是cookie内容（通常是服务端session存储的内容）

第二段是时间戳
```
import time
from itsdangerous import base64_decode, bytes_to_int, EPOCH

# 时间戳
timestamp = bytes_to_int(base64_decode("DNMFOw")) + EPOCH  # EPOCH是一个常量时间戳(2011.1.1)，设计目的是减少数据传输
# 日期
print time.strftime('%Y-%m-%d %H:%I:%S', time.localtime(timestamp))
```

第三段是通过HMAC算法签名的校验信息。也就是说即使你修改了前面的值，由于签名值有误，flask不会使用该session。签名过程用到了SECRET_KEY。所以一定要保存好SECRET_KEY。一旦让别人知道了SECRET_KEY，就可以通过构造cookie伪造session值。
