---
layout: post
title: "[Python]pandas引用和复制的PK"
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

关于引用和复制的问题，可能会造成很难发现的错误。也就是数据是"正确"的，运行不出错，但是和期望结果会相差很多，很难发现。一种可能的方式是采用类似"梯度校验"的方式，进行数据验证，但是难免繁琐，所以总结一句，不能轻易放过代码的任何一个warning，因为任何warning都是潜在错误的表现。















