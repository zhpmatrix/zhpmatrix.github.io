---
layout: post
title: "[ML]机器学习模型关系分析和探讨"
excerpt: "这篇博客梳理了机器学习常见模型之间的关系，涉及到从不同的角度看同一个模型，或者从同一个角度看不同的模型。"
date: 2017-12-27 13:41:00
mathjax: true
---

1.单层感知机(不含有隐藏层)是一种线性分类器。

2.对自组织映射网络，如果使其邻域交互作用设为0，则等价于K均值聚类算法。

3.很多情况下，多层感知机的输出可以看作是对贝叶斯后验概率的估计。

4.[二项分布，信息熵，逻辑回归的Loss函数关系](http://blog.csdn.net/xsqlx/article/details/51120485#t2)

5.[GBDT和LR在泛函空间的相似性联系](http://blog.csdn.net/xsqlx/article/details/51330627)

6.[Multinomial回归多分类推导](http://blog.csdn.net/xsqlx/article/details/76599171)

7.[Linear SVM和LR的异同](https://www.zhihu.com/question/26768865/answer/247134855)

8.[分类学习算法-一个统一的视角](https://zhuanlan.zhihu.com/p/30745139)

按照最小化期望损失分为概率框架和非概率框架。在概率框架下，根据**估计条件分布**，分为判别模型和生成模型。判别模型直接对条件分布建模，有两种建模方法，分为参数方法和非参数方法。参数方法需要假设分布的具体形式，用参数估计的方法去求解参数。非参数方法不需要显式假设分布的具体形式，使用全部样本去表示条件分布。生成模型间接对条件分布建模。非概率框架下，直接学习假设分布。

所有上述的分析可以讨论：KL距离和Logistic损失函数之间的关系。

9.[朴素贝叶斯与单层神经网络关系](https://zhuanlan.zhihu.com/p/30824582)

10.[极大似然估计和贝叶斯估计之间的关系](2017-10-14-relationships-models.md)

这个Blog和Blog 8结合起来看，可能会更棒。

11.[K-平均算法和其他模型/算法之间的关系](2017-10-14-relationships-models.md)

12.[传统算法如何转化成神经网络?](http://www.sohu.com/a/210423018_114877)

附带一个很好的基础Blog：[神经网络容易忽视的基础知识](https://www.leiphone.com/news/201711/MWEDFvRMdOyN7Evm.html?ulu-rcmd=0_5021df_rfill_2_72a03ae49ee64aeb96fb79c6dc33f672)

13.最大熵模型和LR模型的关系

最大熵和SVM都用到对偶理论。

14.L2(Ridge Regression，L2 weight decay)等价于Early Stopping？

[知乎问题-寻找全局最小值和防止过拟合是不是矛盾？](https://www.zhihu.com/question/264607356/answer/283856609)

@废柴大蜗牛的回答，尝试性的解决了上述问题。深度学习社区早期一直在推动的一个事情是“局部最优是全局最优，FAIR的工作证明了不是。可以参考他的年度总结[2017年度总结](https://zhuanlan.zhihu.com/p/32380031)

15.[贝叶斯观点下的拉普拉斯平滑](https://zhuanlan.zhihu.com/p/24291822)

[朴素贝叶斯分类器的应用](http://www.ruanyifeng.com/blog/2013/12/naive_bayes_classifier.html)

16.[LR的生成模型观察](http://www.bilibili.com/video/av10590361/#page=5)

17.对比散度来近似玻尔兹曼机中难以处理的对数似然梯度

18.[岭回归(Ridge regression)和主成分分析(PCA)的关系](https://zhuanlan.zhihu.com/p/32500133)

PCA暴力地将奇异值小的维度置为0，其他维度置为1；Ridge regression的惩罚系数对奇异值不同的维度的惩罚力度不同。二者都是通过消除数据的多重共线性来提升线性回归的效果，连接桥梁是SVD分解。



