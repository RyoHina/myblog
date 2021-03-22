---
layout: post
title: "Nodejs爬虫慎用axios"
categories: node
tags: node axios
---

* content
{:toc}

1. 在循环中大量执行下面代码后，会卡死，"after axios" 出不来，查了下官方issue，2018年就有人说这事了，后来这个issue被关闭了但问题没有解决，现在都2021年了也没有解决。
[查看这个issue](https://github.com/axios/axios/issues/124)

```
console.log('before axios....')
const res = await axios({
 url,
 method: 'get',
 timeout: 1000 * 30,
 proxy: {
  host: proxy.host,
  port: proxy.port,
  auth: {
   username: proxy.user,
   password: proxy.pass
  }
 }
}).catch(err => {
 console.log('axios request failed. url:' + url)
})
console.log('after axios')
```

换成got库，就没问题了。。。真没想到这么知名的库还有这种bug!
```
const agent = tunnel.httpOverHttp({
 proxy: {
  host: proxy.host,
  port: proxy.port,
  proxyAuth: proxy.user + ":" + proxy.pass
 }
})
console.log('before got....')
const res = await got(url, {
 timeout: 1000 * 30,
 agent: {
  https: agent,
  http: agent
 }
}).catch(err => {
 console.log('got request failed. url:' + url)
})
console.log('after got')
```
