---
layout: post
title: "js格式化大段文本小技巧"
categories: js
tags: js
---

* content
{:toc}

python语言定义大段文本，一般都这样写
python code:

```
str = '''
asdfdfsaasfdsadf--\n ' "
asdf
阿斯蒂芬
'''
print(str)
```

可以js语法不支持类似的写法，只好找一些小技巧了。
js code:

```
var multiple_string = function() {
    var fun = function() {
    /*line1
    line2
    line3
    \nline4*/
    }
    var lines = fun.toString();
    lines = lines.substring(lines.indexOf("/*") + 2, lines.lastIndexOf("*/"));
    /* 这里只处理一些常见的转义 */
    lines = lines.replace(/\\n/g, "\n");
    lines = lines.replace(/\\r/g, "\r");
    return lines.replace(/\\t/g, "\t");
}();

console.log(multiple_string)

```

