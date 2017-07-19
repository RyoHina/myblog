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

可是js语法不支持类似语法，但有一些小技巧
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

但不幸的是这种奇淫巧技会被代码混淆压缩等工具直接当成普通注释删掉~~~so, 还是尽量少用微妙！
