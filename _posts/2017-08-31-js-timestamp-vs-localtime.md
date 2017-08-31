---
layout: post
title: "js中时间戳转换为本地时间(北京时间)"
categories: js
tags: html js
---

* content
{:toc}

Code：

```
var = 1504159185;  //2017-08-31 13:59:45

// 时间戳转换为北京时间
function timestamp2timestr(timestamp) {
    var date = new Date(timestamp * 1000 + 8*60*60*1000);
    return date.getUTCFullYear() + "-" + fix(date.getUTCMonth() + 1, 2) + "-" + fix(date.getUTCDate(), 2);
}

// 如果代码会在其他国家跑，需要取当地时间
// 时间戳转换为本地时间
function timestamp2timestr(timestamp) {
    var toffset = new Date();
    var date = new Date(timestamp * 1000 - toffset.getTimezoneOffset() * 60 * 1000);
    return date.getUTCFullYear() + "-" + fix(date.getUTCMonth() + 1, 2) + "-" + fix(date.getUTCDate(), 2);
}
```
