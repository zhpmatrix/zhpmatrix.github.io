---
layout: post
title: "[ML&DM]sklearn中的并行和串行"
excerpt: "聊聊pipeline,featureunion,gridsearch等话题"
date: 2017-03-20 14:27:00
---

在阿里口碑商家流量预测大赛中，聊过训练速度的问题。实际上我们的训练数据并不大，在实际训练数据较大的时候，训练时间就会成为一个棘手的问题，因为sklearn作为一个通用算法包，并不针对于分布式训练。实际上在源代码中，我们也会看到一些并行的实现，同时contributors们已经将这种抽象放在了用户面前，代表是FeatureUnion和GridSearchCV。

先聊聊Pipeline，按照文档中的说法：通过pipeline可以实现一次fit调用而使用多个transformers,同时和GridSearchCV结合可以实现并行调参。让我们看代码：

<script src="https://gist.github.com/zhpmatrix/1dde70122592d941159e1735775a990f.js"></script>

在代码中，我们使用的transformer有PCA,SelectKBest,log1p,通过和一个estimator是SVC进行组合，形成一个Pipeline，在GridSearchCV中得以使用。注意：Pipeline的最后一个元素必须是estimator!我们进行transform的目的不就是estimate吗。

GridSearchCV通过使用默认的3折交叉验证，并行调参。串行情况下是几个for循环的代码，其实在用C++实现参数选择的时候，单机多核环境下可以利用OpenMP实现同样的效果，不过GridSearchCV在帮助我们完成模型选择的同时，通过引入Pipeline的使用，提供给了我们更加灵活的调整方式。通常的思路是在参数调整的过程中，训练数据是经过特征处理过的数据，而通过Pipelline的使用，我们设置可以灵活地调整特征处理过程。

回到FeatureUnion并行处理数据。按照字面意思，Union是合并的意思，执行的过程是对输入的原始数据，进行并行特征处理，处理之后的数据直接合并成一张大的数据表(矩阵)。很明显，这里存在一个很不方便的地方在于，我们不能对训练数据的部分列进行并行处理，FeatureUnion在0.18版只支持输入的整个数据。在参考中，1给出了在0.17版中的解决方案，就是FeatureUnion的fit_transform方法重写，引入数据列索引数据，但在0.18版的源代码中，此方法被重写。同时参考2给出了关于该问题的项目issue。

在FeatureUnion的源代码中可以看到，其实现是利用joblib的Parallel和delayed方法，Parallel是对multiprocessing的封装，在之前的博文中，我们利用multiprocessing做了比赛代码的加速实验。同时也有人指出，RandomForest的实现中也利用了此种方式实现一定意义上的并行。举个例子：

    from math import sqrt  
    from joblib import Parallel, delayed  
    Parallel(n_jobs=2)(delayed(sqrt)(i ** 2) for i in range(10))  

输出：

    [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]  

在上述代码中，Parallel对象创建一个进程池，在多进程中环境中执行每一个列表项，函数delayed则是一个创建元组(function, args, kwargs)的技巧，新技能Get到了吗？

总结：

实际上从给出的代码来看，似乎Pipeline，FeatureUnion和GridSearchCV搭配干活儿的样子很好看。但是考虑到有时候，我们的特征工程是单独拉出来做的，而且面临的数据量可能非常大，为了tuning，把特征工程再给做一遍吗？此外，在数据挖掘竞赛中，模型融合似乎很受欢迎，在多模型情境下，如何更好的利用上述工具进行tuning？不过，在单模型和简单特征处理的任务场景中，的确很赞！

参考：

1.[jasonfreak](http://www.cnblogs.com/jasonfreak/)(_jasonfreak的文章比较扎实_)

2.[关于FeatureUnion的部分并行的issue](https://github.com/scikit-learn/scikit-learn/issues/2034)






