---
layout: post
title: "pandas引用和复制的PK"
tags: [Python]
excerpt: "经常会遇到一个warning，叫做SettingWithCopyWarning，本文尝试弄清楚pandas在各种场景下的引用和复制的问题，也就是view和copy的对比。"
date: 2017-08-13 17:01:00
mathjax: true
---

给出一个warning的提示如下：

    main.py:42: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame.
    Try using .loc[row_indexer,col_indexer] = value instead

    See the caveats in the documentation: http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-view-versus-copy
    d1[0] = 999

其中**main.py:42**是发生这个warning的代码行，**d1[0]=999**是warning发生的具体代码，同时给出了建议的替代方式和官方参考文档的链接。

在这篇博客[pandas的引用和复制](http://blog.csdn.net/qtlyx/article/details/70500145)中作者总结了7种引用和复制的场景，个人感觉没有从本质上解决问题，但是提供了一个很好的研究范例。假设改变**数据产生函数**的定义，各种情景又会不同，例如给出一种数据产生函数的定义：

    def data_gen():
        data = {'a':[1,2,3],'b':[5,6,7],'c':[6,6,6]}
        df = pd.DataFrame(data)
        return df

此外，在交互式命令行下和python脚本下的执行也会不同。例如，代码41行在交互式模式下运行会给出警告，但是如果直接执行python脚本则没有警告。

[补充: 天池-蚂蚁金服：商场中精确定位用户所在店铺 实验对比]

给定Pandas元素赋值，有三种方式如下：

* df.set\_value(行名称，列名称，新值):

* df.loc\[行名称，列名称\] = 新值

* df.iloc\[行标\]\[列标\] = 新值

在脚本环境中，方式一和方式二能够成功赋值，交互式环境下三种方式都OK!（为什么第三种方式在脚本环境下不能赋值？）

处理**483931个object类型(字符串类型)**，方式一用时330s，方式二用时远远超过330s(为啥没有具体结果，因为没有耐心等到结果出现，逃)。


[补充：Pandas大规模值替换的一个例子(200w样本，1s左右)]

    df.col_name = df.col_name.map({value0: new_value0, value1: new_value1})

在IJCAI2017比赛中的特征处理时的一行代码：

    m2Data.loc[:,'dayofweek'] = map(lambda x:x.dayofweek,m2Data['time_stamp'])


[补充：现在有一个pandas的Series和一个python的list，想让Series按指定的list进行排序，如何实现？]

reorder\_categories和set\_categories，可以参考[这篇文章](http://www.jianshu.com/p/2d3dd3e30d51)。

看到更简单的代码：

    s = pd.Series([4.5, 2.7, 8.9, -0.4], index = ['d', 'b', 'a', 'c'])
    
    s.reindex(['a', 'b', 'c', 'd', 'e'])

关于引用和复制的问题，可能会造成很难发现的错误。也就是数据是"正确"的，运行不出错，但是和期望结果会相差很多，很难发现。一种可能的方式是采用类似"梯度校验"的方式，进行数据验证，但是难免繁琐，所以总结一句，不能轻易放过代码的任何一个warning，因为任何warning都是潜在错误的表现。















