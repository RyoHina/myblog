---
layout: post
title: "<上拉加载更多>的一种极简实现方式"
categories: js
tags: html js
---

* content
{:toc}

上拉加载更多功能我们经常会用到，这里实现一种极简的实现方式。
思路：
监听某一个div是否在可视区域回调，如果在可视区域则出发加载更多函数。

CODE：

```
	<body>
	<div id="content-parent"></div>
	<div><p id="loadmore">努力加载中...</p></div>
	</body>

    var AJAX_LOAD_STEP = 6;
    var is_loading = false;
    var start_index = 0;
    var has_more_item = true;

    $(document).ready(function () {
        $(window).scroll(function () {
            if (!has_more_item) {
                return;
            }

            var a = document.getElementById("loadmore").offsetTop;
            var wst = $(window).scrollTop();
            if (a >= wst && a < (wst + $(window).height())) {
                if (is_loading) {
                    return;
                }
                setTimeout(function () {
                    ajax_get(start_index);
                }, 300);
            }
        });

        ajax_get(start_index);
    });

	function ajax_get(start) {
        is_loading = true;
        $.ajax({
            url: '/getitem',
            type: 'POST',
            dataType: 'json',
            async: false,
            data: {
                step: AJAX_LOAD_STEP,
                startindex: start
            },
            success: function (res) {
                is_loading = false;
                start_index += AJAX_LOAD_STEP;
                switch (res.status) {
                    case -1:
                        alert("failed:" + res.errmsg);
                        break;
                    case 0:
                        if (res.items.length < AJAX_LOAD_STEP) {
                            has_more_item = false;
                            $("#loadmore")[0].innerHTML = "没有更多文章了...";
                        }
                        var html_str = "";
						// html_str = ...
                        if (start_index === AJAX_LOAD_STEP) {
                            $("#content-parent").html(html_str);
                        } else {
                            $("#content-parent")[0].innerHTML += html_str;
                        }
                        break;
                }
            },
            error: function (httpReq, status, exception) {
                is_loading = false;
                alert(status + ";" + exception);
            }
	}
```
