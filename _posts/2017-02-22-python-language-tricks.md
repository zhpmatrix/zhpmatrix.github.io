---
layout: post
title: "若干有意思的知识点"
tags: [Python]
excerpt: "鸭子类型，装饰器，闭包，生成器"
date: 2017-02-22 12:00:00
---

#### 鸭子类型(Duck Type)

“当看到一只鸟走起来像鸭子、游泳起来像鸭子、叫起来也像鸭子，那么这只鸟就可以被称为鸭子。”，这被称为“鸭子测试”。看代码，[这里有惊喜](https://en.wikipedia.org/wiki/Duck_typing#In_C.2B.2B)：

    class Duck:
        def quack(self):
            print("Quack, quack!")
        def fly(self):
            print("Flap, Flap!")

    class Person:
        def quack(self):
            print("I'm Quackin'!")

        def fly(self):
            print("I'm Flyin'!")

    def in_the_forest(mallard):
            mallard.quack()
            mallard.fly()

    in_the_forest(Duck())
    in_the_forest(Person())

首先想到的是C++中的"多态"？鸭子类型是动态类型的一种风格，在鸭子类型中，关注的不是对象的类型本身(弱类型)，而是使用方法。至于是鸟还是鸭子，可能并不太关心，只要，走起来，游起来，叫起来像鸭子，那它就是鸭子了。

#### 数据属性

这点和C++不一样，数据属性分为**类数据属性**和**实例数据属性**(通常意义上的私有变量)。上代码：

    class TreeMethod():
        n_estimators = 10
        max_depth = 5
        def __init__(self,learning_rate,min_child_num):
            self.learning_rate = learning_rate
            self.min_child_num = min_child_num

上述代码中，类数据属性就是n_estimators和max_depth了，实例数据属性是learning_rate和min_child_num。对于类数据属性和实例数据属性，可以总结为：

1.类数据属性属于类本身，可以通过类名进行访问/修改。

2.类数据属性也可以被类的所有实例访问/修改。

3.在类定义之后，可以通过类名动态添加类数据属性，新增的类属性也被类和所有实例公有。

4.实例数据属性只能通过实例访问。

5.在实例生成后，还可以动态添加实例数据属性，但是这些实例数据属性只属于该实例。

#### @property & @setter

利用这两个装饰器实现getter和setter方法，其实从代码量层面，没有减少。但是从可读性上来说，似乎好了一点儿。上代码：

    class  Person():
        def __init__(self):
            self._name = 'zhpmatrix'
        @property
        def name(self):
            return self._name
        @name.setter
        def name(self,nameStr):
            if isinstance(nameStr,str):
                self._name = nameStr
            elif:
                raise ValueError('name must be string!')

#### @staticmethod & @classmethod

python中有三种方法，实例方法，类方法，静态方法。这三种方法的主要区别在于参数，比如，**类方法的第一个参数必须是一个实例**。实例方法被绑定到一个实例，只能通过实例进行调用；但是对于静态方法和类方法，可以通过类名和实例两种方式进行调用。

#### 迭代器和生成器

用[]推导出来的是列表，列表是可迭代的,用()推导出来的是生成器。比如下述两行代码：

    _iter = [x for x in range(3)]   #type: list

    _gen = (x for x in range(3))   #type: generator

对list迭代要求**所有迭代数据**存储于内存中，生成器迭代每次**只暂存要使用的当前数据**。当要迭代的数据非常大以至于内存装不下，想想生成器。我自己的一个经验是对于python内容的理解，**多从用法角度出发**去看问题。()推导出来的不是tuple，自然不能使用index进行元素的访问，也就是在一定程度上没有访问历史元素的功能, 同时这也是**延迟计算或者惰性求值**(lazy evaluation)的体现。来段代码：

    def gen(n):
        while n > 0:
            yield n   #key word for generator
            n -= 1
    _gen = gen(n)
    for val in _gen():
        print val

#### 闭包

闭包可以实现先将一个参数传递给一个函数，而并不立即执行，以达到**延迟求值**的目的。满足以下三个条件：必须有一个内嵌函数；内嵌函数必须引用外部函数中变量；外部函数返回值必须是内嵌函数。来读代码:
    
    def delay_add(x,y):
        def cal():
            return x + y
        return cal
    add = delay_add(x = 3,y = 4)
    add()

#### 装饰器

在谈装饰器之前，先看看**"\*args"**和**"\*\*kwargs"**，这二位都是python中的可变参数，用于接受参数的传递，**"\*args"**表示任何多个无名参数，它是一个元组，**"\*\*kwargs"**表示关键字参数，它是一个字典。同时使用**'\*args'**和**"\*\*kwargs'**时，必须**'\*args'**在**'\*\*kwargs'**之前。

装饰器的功能是将被装饰的函数当作参数传递给与装饰器对应的函数（名称相同的函数），并返回包装后的被装饰的函数。实际上也是一个语法糖，目的在于简化代码，提高可读性。

谈完闭包，谈完装饰器，给一段在天池比赛中我们的一段代码：

    def time_wrapper(func):
         def wrapper(*args,**kwargs):
                 import time
                 start = time.time()
                 func(*args,**kwargs)
                 end = time.time()
                 print 'COST:{}'.format(end - start)
         return wrapper

    @time_wrapper
    def deal(params):
        #do something

参考：

1.[python中的类(上)](http://python.jobbole.com/82297/)

2.[python进阶之"属性(property)"详解](http://python.jobbole.com/82297/)

3.[深入理解python中的生成器](http://python.jobbole.com/81911/)