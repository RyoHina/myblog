---
layout: post
title: "怎样将Java工程编译成jar文件"
categories: java
tags: java
---

* content
{:toc}

Main.java内容为：

```
package com.company;

public class Main {
    public static void main(String[] args) {
        System.out.println("Hello Java!");
    }
}
```

原始目录结构：
com/company/Main.java
```
cd com/company
javac *.java
得到Main.class, 然后删掉Main.java(否则最终jar包里会有源码)
```

在com同级创建manifest.txt文件，内容为：
```
Manifest-Version: 1.0
Main-Class: com.company.Main

```
***注意manifest.txt最后一定要留一个空行， 而且不要用记事本编辑， 最好用notepad++编辑， 因为jar命令不认\r\n换行符***

目录结构为：
```
manifest.txt
com/company/Main.class
```

在根目录下执行：

jar -cvfm a.jar manifest.txt com
(此时会生成a.jar)

java -jar a.jar
(此时在控制台打印出:Hello Java!)
