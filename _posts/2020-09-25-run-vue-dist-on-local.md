---
layout: post
title: "本地运行Vue项目编译后的dist文件夹"
categories: web
tags: web
---

* content
{:toc}

1. 全局安装serve
```
npm i serve -g
```

2. 在dist目录下执行
```
serve
```

还有一种方法，修改vue.config.js，这样打包出来的资源引用就使用相对路径
```
module.exports = {
    "publicPath": ""
}
```
