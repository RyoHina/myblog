---
layout: post
title: "仿微信底部导航HTML+CSS实现"
categories: html
tags: html css
---

* content
{:toc}

点击 [ **这里** ](https://kyle.net.cn/htmls/nav-bar.html) 查看Demo效果。<br>

找了一些资料发现有些冗余，不够简洁，还是自己写吧。 <br>
在操作img标签src属性时用到了jquery，不想用jquery的可以自己想办法去掉。<br>
以下是代码：

<!--more-->


```
<!DOCTYPE html>
<html>

<head>
    <script src="https://cdn.staticfile.org/jquery/1.11.1/jquery.min.js"></script>
    <meta name="viewport" content="width=device-width">
    <style>
        .navigation-bar {
            position: fixed;
            right: 0;
            bottom: 0;
            width: 100%;
            height: 48px;
            z-index: 1000;
            background-color: #fcfcfc;
            border-top: solid 1px #e4e4e4;
        }
        
        .navigation-bar ul {
            list-style-type: none;
            margin: 0;
            padding: 0;
        }
        
        .navigation-bar li {
            float: left;
            width: 33.333%;
            /*设置img居中*/
            text-align: center;
        }
        
        .navigation-bar img {
            margin-top: 2px;
            width: 48px;
            height: 42px;
        }

    </style>
</head>

<body>
    <div>
        <div>
            <h1>Title</h1>
        </div>

        <div>
            <p>xxxxx。</p>
            <p>xxxxx。</p>
            <p>xxxxx。</p>
            <p>xxxxx。</p>
            <p>xxxxx。</p>
            <p>xxxxx。</p>
            <p>xxxxx。</p>
            <p>xxxxx。</p>
            <p>xxxxx。</p>
            <p>xxxxx。</p>
            <p>xxxxx。</p>
            <p>xxxxx。</p>
            <p>xxxxx。</p>
            <p>xxxxx。</p>
            <p>xxxxx。</p>
            <p>xxxxx。</p>
        </div>

        <div>
            <div class="navigation-bar">
                <ul>
                    <li onclick="nav_set_home_btn_active()"><img id="nav-home" src="https://blog.kyle.net.cn/nav-bar/home.png"></li>
                    <li onclick="nav_set_find_btn_active()"><img id="nav-find" src="https://blog.kyle.net.cn/nav-bar/find.png"></li>
                    <li onclick="nav_set_my_btn_active()"><img id="nav-my" src="https://blog.kyle.net.cn/nav-bar/my.png"></li>
                </ul>
            </div>
        </div>

        <script>
            function nav_set_home_btn_active() {
                nav_set_all_buttons_inactive();
                $("#nav-home").attr("src", "https://blog.kyle.net.cn/nav-bar/home-active.png");
            }

            function nav_set_find_btn_active() {
                nav_set_all_buttons_inactive();
                $("#nav-find").attr("src", "https://blog.kyle.net.cn/nav-bar/find-active.png");
            }

            function nav_set_my_btn_active() {
                nav_set_all_buttons_inactive();
                $("#nav-my").attr("src", "https://blog.kyle.net.cn/nav-bar/my-active.png");
            }

            function nav_set_all_buttons_inactive() {
                $("#nav-home").attr("src", "https://blog.kyle.net.cn/nav-bar/home.png");
                $("#nav-find").attr("src", "https://blog.kyle.net.cn/nav-bar/find.png");
                $("#nav-my").attr("src", "https://blog.kyle.net.cn/nav-bar/my.png");
            }

            //设置home默认active
            $("#nav-home").attr("src", "https://blog.kyle.net.cn/nav-bar/home-active.png");
        </script>
</body>

</html>
```
