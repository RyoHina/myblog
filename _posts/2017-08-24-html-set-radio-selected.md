---
layout: post
title: "html使用js设置radio类型input控件选中的两种方法"
categories: html
tags: html radio
---

* content
{:toc}

Code：

```
<html>

<head>
    <script src="https://cdn.bootcss.com/jquery/2.1.1/jquery.min.js"></script>
</head>

<body>
    <div>
        <input type="radio" checked="checked" onclick="click_radio()">1</input>
        <input type="radio" onclick="click_radio()">2</input>
        <input type="radio" onclick="click_radio()">3</input>
        <br>
        <button id="btn1">1</button>
        <button id="btn2">2</button>
        <button id="btn3">3</button>

    </div>
    <script type="text/javascript">
        $(function() {
            $("#btn1").click(function() {
                $("input[type='radio']").removeAttr("checked");
                // 方法1，会产生一个onclick事件
                $("input[type='radio']").eq(0).click();
                //$("input[type='radio']").eq(0).prop('checked', true);
            });
            $("#btn2").click(function() {
                $("input[type='radio']").removeAttr("checked");
                //$("input[type='radio']").eq(1).click();
                //方法2，不会产生onclick事件
                $("input[type='radio']").eq(1).prop('checked', true);
            });
            $("#btn3").click(function() {
                $("input[type='radio']").removeAttr("checked");
                //$("input[type='radio']").eq(2).click();
                $("input[type='radio']").eq(2).prop('checked', true);
            });
        });

        function click_radio() {
            console.log("click radio.");
        }
    </script>
</body>

</html>
```
