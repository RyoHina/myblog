---
layout: post
title: "Web Server开发中session应当如何存储用户登录凭据？"
categories: flask
tags: session flask
---

* content
{:toc}


#### 1. 应用场景 ####
Web Server验证用户登录成功后，拿到了用户登录凭据(能够唯一标识用户的东西)，一般来讲我们要把这个登录凭据放在session中，下次访问某连接的时候Web Server可以验证用户是否是在登录状态。
在开发微信服务号后台时，微信网页授权成功后拿到是对于此服务号唯一用户标识openid，如果直接把openid放到session中是有风险的，万一被别人拿到，就能伪装此用户做一些危险的事情。
<!--more-->

#### 2.解决思路 ####
把openid加密后存储到session中，验证时拿出来解密后就知道openid了。
	
	# coding=utf-8
	import base64
	rc4_key = 'set your rc4 key.'
	
	# rc4流加密算法
	def rc4(data, key):
	    &quot;&quot;&quot;RC4 encryption and decryption method.&quot;&quot;&quot;
	    S, j, out = list(range(256)), 0, []
	
	    for i in range(256):
	        j = (j + S[i] + ord(key[i % len(key)])) % 256
	        S[i], S[j] = S[j], S[i]
	
	    i = j = 0
	    for ch in data:
	        i = (i + 1) % 256
	        j = (j + S[i]) % 256
	        S[i], S[j] = S[j], S[i]
	        out.append(chr(ord(ch) ^ S[(S[i] + S[j]) % 256]))
	
	    return &quot;&quot;.join(out)


	# 加密字符串
	def en_str(s):
	    if not isinstance(s, str):
	        return None
	    # reverse
	    s = s[::-1]
	
	    # rc4
	    rs = rc4(s, rc4_key)
	
	    # base64
	    result = base64.b64encode(rs)
	    return result
	
	
	# 解密字符串
	def de_str(s):
	    if not isinstance(s, str):
	        return None
	    # base64
	    bs = base64.b64decode(s)
	
	    # rc4
	    rs = rc4(bs, rc4_key)
	
	    # reverse
	    result = rs[::-1]
	    return result

### 3.其他解决思路 ###
如果使用flask开发Web Server，可以尝试使用Flask-Session扩展加密登录凭据。
