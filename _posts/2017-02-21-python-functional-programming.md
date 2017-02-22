---
layout: post
title: "[Python]后知后觉函数式编程"
excerpt: "文中主要谈了匿名函数,filter,map,reduce等，同时给出了一些短小精美的代码。"
date: 2017-02-22 21:00:00
---

##### 匿名函数(lambda)

python中使用lambda关键字创造匿名函数，使用匿名函数，可以在调用时**绕过函数的栈分配**。具体语法：

    lambda 参数:表达式

注意：参数可以是无参数，带参数，带参数默认值，变长参数。给出一个变长参数的例子:

    func = lambda *val:set(val)
    func(1,2,2,3)
    func(1,2)

##### filter

给出filter的格式声明：

    filter(func,seq)

func函数是一个布尔函数，filter调用这个布尔函数，将每个seq中的元素依次过一遍筛子，选出使func返回值是Ture的元素的序列。很容易想到，如果使用列表推导也可以实现，但是问题在于，你写个复杂的过滤条件试试？filter给我们提供了一个封装复杂过滤条件的方式(函数)。举个栗子：

    ages = [12,34,80]
    def age_filter(age):
        return age >= 10 and age <= 20
    #common method
    filtered_age = []
    for age in ages:
        if age_filter(age):
            filtered_age.append(age)
    #filter method
    filter(age_filter,ages)
    #list method
    [age for age in ages if age >= 10 and age <= 20]


##### map

关于map，首先给出格式声明：

    map(func,seq1[,seq2...])

map()函数的作用是将func作用于seq中的每一个元素，并用一个列表给出返回值。既然谈到了匿名函数，这个func当然可以是匿名函数。注意，当map多个可迭代序列时，是并行处理的。欣赏几段代码：

    print map(lambda x: x+2,range(6))

    print [x+2 for x in range(6)]

    print map(lambda x,y:x+y,[1,2,3],[4,5,6])

    print map(lambda x,y,(x+y,x-y),[1,2,3],[4,5,6])

看到第四行代码，注意到了什么吗？下列三行代码是等价的哦！

    print map(lambda x,y:(x,y),[1,2,3],[4,5,6])

    print map(None,[1,2,3],[4,5,6])

    print zip([1,2,3],[4,5,6])

在天池比赛的特征工程处理中，这种用法非常常见，特别是人工特征的时候，需要对每个样本进行特征生成。

##### reduce

reduce的格式是：

    reduce(func,seq[,init])

每次迭代，将上一次的迭代结果（第一次时为init的元素，如没有init则为seq的第一个元素）与下一个元素一同执行一个二元的func函数。在reduce函数中，init是可选的，如果使用，则作为第一次迭代的第一个元素使用。给出常见的代码：

    n = 5
    print reduce(lambda x,y:x * y,range(1,n + 1))  # 120



    m = 2
    n = 5
    print reduce(lambda x,y:x * y,range(1,n + 1),m)  # 240

其中的一个应用场景是：在[代码优化](https://zhpmatrix.github.io/2017/02/19/speed-up/)中，我们做了多线程和多进程的处理，比如分成4进程，每个进程处理500个商家的预测，那么由于最终我们需要得到一个总的loss，故整个计算过程其实是sum累和。我估计，mapreduce在分布式场景下原理类似。


参考：

1.[Charming Python:Functional programming in Python](http://blog.jobbole.com/35045/)


