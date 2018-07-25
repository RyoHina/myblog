---
layout: post
title: "子div使用margin-top自己不生效，却对父div生效？"
categories: html
tags: html css
---

* content
{:toc}

先看代码：

```
<html>
<head>
    <style>
        body {
            margin: 0px;
        }
        
        .basediv {
            height: 200px;
            background-color: aquamarine;
        }
        
        .childdiv {
            width:60px;
            height: 20px;
            background-color: red;
            /* 自己不生效，却对父div生效 */
            margin-top:100px;
        }
    </style>
</head>
<body>
    <div>
        <div class="basediv">
            <div class="childdiv">
            </div>
        </div>
    </div>
</body>
</html>

```

<!--more-->

结果图：<br>

![](https://blog.kyle.net.cn/child-div.png)

明明对childdiv设置margin-top自己没生效，却对父div生效。
这是因为当父级元素没有设置border-top或者padding-top的时候，他的第一个子节点（这里包括元素节点和文本节点）如果设置了margin-top，那么这个margin-top会一层层往上越级直到遇到以下情况之一才停下：<br>
* (1)一个设置了border-top或者padding-top的父元素
* (2)直到遇到body
* (3)此父级元素的第一个子节点不为他或他的父元素

（这里表述不清，请自己写code体会，注意每个div里面文本的位置）解决方法：给父元素设置一个border-top或者padding-top把子元素管住就可以防止越级了。比如给#a加上border-top: 1px solid transparent;或者padding-top:1px;外边距合并并不是浏览器的bug，因为所有的现代浏览器都有这个行为，而且在标准里面也写了。

参考：[https://www.zhihu.com/question/24279692/answer/27272393](https://www.zhihu.com/question/24279692/answer/27272393)
