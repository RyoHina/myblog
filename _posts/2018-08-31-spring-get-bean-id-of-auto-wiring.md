---
layout: post
title: "Spring框架 - 怎样获取自动装配bean ID"
categories: java
tags: java spring
---

* content
{:toc}

先定义一个接口Car
```
package com.example.demo;

public interface Car {
    void run();
}
```

再分别定义两个实现类

```
package com.example.demo;

import org.springframework.stereotype.Component;

@Component
public class FerrariCar implements Car {
    public void run() {
        System.out.println("FerrariCar is running.");
    }
}


/////////////////////////////////////
package com.example.demo;

import org.springframework.stereotype.Component;

@Component
public class BMWCar implements Car {
    public void run() {
        System.out.println("BMW is running.");
    }
}

```

定一个土豪类
```
package com.example.demo;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class RichMan {

    @Autowired
    private Car car;

    public void say() {
        System.out.println("############### I'm Rich!!!!##############");
        car.run();
        System.out.println("############### I'm Rich!!!####################");
    }
}

```

运行发现报错：
```
Field car in com.example.demo.RichMan required a single bean, but 2 were found:
	- BMWCar: defined in file [C:\Users\***\target\classes\com\example\demo\BMWCar.class]
	- ferrariCar: defined in file [C:\Users\***\target\classes\com\example\demo\FerrariCar.class]
```

意思是自动装载Car时，发现有两个Car实例（BMWCar，FerrariCar）, 不知道怎么办了。为了解决这个问题，我们引入@Qualifier注解，该注解接受一个字符串参数，为bean id。

修改RichMan代码
```
package com.example.demo;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Component;

@Component
public class RichMan {

    @Autowired
    @Qualifier("ferrariCar")
    private Car car;

    public void say() {
        System.out.println("############### I'm Rich!!!!##############");
        car.run();
        System.out.println("############### I'm Rich!!!####################");
    }
}
```

发现一切正常。尝试修改为@Qualifier("bMWCar")，运行报错了，说找不到bean，这到底是为什么呢？
我们知道@Component是可以指定bean id的，尝试一下手动指定bean id, 然后保持与@Qualifier参数一致，发现是ok的。这说明@Component默认指定的bean id规则并不是无脑把第一个字母小写，为了验证，我们实现BeanNameAware接口，代码如下：
```
package com.example.demo;

import org.springframework.beans.factory.BeanNameAware;
import org.springframework.stereotype.Component;

@Component
public class BMWCar implements Car, BeanNameAware {
    public void run() {
        System.out.println("BMWCar is running.");
    }

    public void setBeanName(String name) {
        System.out.println("BMWCar bean Name:" + name);
    }
}

```

发现果然是@Component默认指定的bean id规则并不是无脑把第一个字母小写。

### @Component默认指定的bean id规则: 如果类名由两个连续大写字母开头，则bean id与类名保持一致。否则将类名第一个字母小写作为bean id。
