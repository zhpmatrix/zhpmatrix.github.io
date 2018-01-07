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

针对二分类问题，假设每个样本符合二项分布B(1,p)，其中p表示该样本是正类的概率，则似然函数就是所有样本的分布的乘积，也就是目标函数。接下来就是最大化似然函数的值了。在逻辑回归中，用Sigmoid函数来表示p，用梯度上升法求解参数的值。

可以参考[LR的推导过程加强理解](http://blog.csdn.net/ligang_csdn/article/details/53838743)，在[Softmax函数与交叉熵](https://zhuanlan.zhihu.com/p/27223959)中提到，对于LR问题，需要最大化似然函数，如果在似然函数前加一个负号作为目标函数，就需要最小化目标函数的值，此时这个目标函数就称为交叉熵损失函数，这种命名似乎在DL中比较常见。同时给出了相对熵(KL散度)和交叉熵的关系。

5.[GBDT和LR在泛函空间的相似性联系](http://blog.csdn.net/xsqlx/article/details/51330627)

Boosting别名：函数空间梯度下降。Boosting的可加性体现在根据决策树模型得到预测值的可加。决策树和线性回归只是相同算法框架下的不同假设，从这个角度来说，回归和分类也是共生于一个通用的算法框架。

6.[Multinomial回归多分类推导](http://blog.csdn.net/xsqlx/article/details/76599171)

7.[Linear SVM和LR的异同](https://www.zhihu.com/question/26768865/answer/247134855)

不同点：

LR不依赖于数据的距离测度；Linear SVM依赖数据的距离测度，需要对数据做Normalization；

LR受所有数据点的影响，要做不平衡处理；Linear SVM不依赖数据分布(假设分类平面确定了，某一类加减一些样本后，分类平面不受影响)；

共同点：

Linear SVM依赖惩罚项的系数；LR依赖L1 regularization；

Linear SVM和LR都对Outlier敏感；

关于为什么要做归一化，这里有个非常棒的[回答](https://www.zhihu.com/question/37129350)。

站在优化的角度，如果不归一化，各维特征跨度很大，目标函数是“扁”的，梯度优化过程会发生震荡；如果归一化，目标函数是“圆”的，每一步梯度的方向都会基本指向最小值，可以大踏步前进，Momentum是从优化方法本身来解决这个问题的。

8.[分类学习算法-一个统一的视角](https://zhuanlan.zhihu.com/p/30745139)

按照最小化期望损失分为概率框架和非概率框架。在概率框架下，根据**估计条件分布**，分为判别模型和生成模型。判别模型直接对条件分布建模，有两种建模方法，分为参数方法和非参数方法。参数方法需要假设分布的具体形式，用参数估计的方法去求解参数。非参数方法不需要显式假设分布的具体形式，使用全部样本去表示条件分布。生成模型间接对条件分布建模。非概率框架下，直接学习假设分布。

概率框架:   选定分布距离的度量方法->最小化分布距离
                                                |KL距离对应LR的损失函数(不严格的说)|
非概率框架:  选定替代损失函数->期望风险最小化

概率框架->非概率框架？条件是什么？

所有上述的分析可以讨论：KL距离和Logistic损失函数之间的关系。

9.[朴素贝叶斯与单层神经网络关系](https://zhuanlan.zhihu.com/p/30824582)

链接中的专栏并没有讲清楚。

10.[极大似然估计和贝叶斯估计之间的关系](http://blog.csdn.net/guohecang/article/details/52313046)

最大似然估计(MLE)只考虑某个模型能产生某个给定观察序列的概率，而不考虑该模型本身的概率，这是与贝叶斯估计的区别。最大后验估计(MAP)融入了估计量的先验分布，从形式上看是贝叶斯估计。[详解MLE，MAP，和贝叶斯公式的理解](http://blog.csdn.net/u011508640/article/details/72815981)对MLE和MAP问题的区别和联系解释的非常棒！

这个Blog和Blog 8结合起来看，可能会更棒。

11.K-means算法和其他模型/算法之间的关系

高斯混合模型(GMM)是EM算法的特例，而K-means是GMM的一个特例。EM/聚类从解决无监督问题来看是相似的。

12.[传统算法如何转化成神经网络?](http://www.sohu.com/a/210423018_114877)

附带一个很好的基础Blog：[神经网络容易忽视的基础知识](https://www.leiphone.com/news/201711/MWEDFvRMdOyN7Evm.html?ulu-rcmd=0_5021df_rfill_2_72a03ae49ee64aeb96fb79c6dc33f672)

13.最大熵模型和LR模型的关系

最大熵和SVM都用到对偶理论。

参考一篇论文《The equivalence of logistic regression and maximum entropy models》

14.L2(Ridge Regression，L2 weight decay)等价于Early Stopping？

[知乎问题-寻找全局最小值和防止过拟合是不是矛盾？](https://www.zhihu.com/question/264607356/answer/283856609)

@废柴大蜗牛的回答，尝试性的解决了上述问题。深度学习社区早期一直在推动的一个事情是“局部最优是全局最优，FAIR的工作证明了不是。可以参考他的年度总结[2017年度总结](https://zhuanlan.zhihu.com/p/32380031)

15.[贝叶斯观点下的拉普拉斯平滑](https://zhuanlan.zhihu.com/p/24291822)

[朴素贝叶斯分类器的应用](http://www.ruanyifeng.com/blog/2013/12/naive_bayes_classifier.html)

这篇文章试图用贝叶斯统计的方法来推导出朴素贝叶斯方法的整个体系，如何推导出拉普拉斯平滑方法用于处理朴素贝叶斯方法中可能出现的零概率问题。

朴素贝叶斯假设特征独立，在计数过程中，发现某个特征从没有出现过，会导致待估计的目标为零。为了解决这种零概率问题(上文引入了一个投硬币的例子)，引入参数的先验概率估计，成为最大后验概率估计问题；当先验概率估计的分布为均匀分布的时候，MAP就是MLE。

假设引入的先验分布使得后验分布和先验分布属于相同的分布族(好处是可以得到解析解)，先验分布则称为共轭先验分布。比如二项分布(二分类问题，相应的多项分布)的共轭是Beta分布。

为了解决零概率问题，引入的平滑贝叶斯方法不仅仅是一个Trick，而是有很深的原理在里面。

关于极大后验和期望后验的讨论在文章中的讨论区，

@Mo.bius说的一段话：选择极大后验和期望后验反映了两种统计思想，选择“众数”和选择平均数，但在贝叶斯学派下统称为贝叶斯解，目的都是为了minimum loss function，统称为贝叶斯解。至于如何选择取决于损失函数的定义，比如说平方损失函数最小时，选择的是期望后验。


16.[LR的生成模型观察](http://www.bilibili.com/video/av10590361/#page=11)

LR在NLP领域称为最大熵模型(不严格)，当类标签只有两个的时候，最大熵模型就是LR模型。

从最大熵模型推导到LR模型，参看这个[答案](https://www.zhihu.com/question/24094554)@Semiring，从推导来看，LR处理多分类问题的时候，使用Softmax函数；而最大熵模型在定义的时候，形式和Softmax给出的形式是类似的。

李宏毅的课程对于判别模型和生成模型的对比：

1.通常人们相信判别模型效果更好；

2.生成模型有对概率分布的假设，该假设的存在使得需要更少的训练数据和对噪音更加的鲁棒；priors and class-dependent probabilities can be estimated from different sources;

常见的判别模型：LR模型(对P(Y|X)建模)

常见的生成模型：朴素贝叶斯模型(对P(X,Y)建模)

17.对比散度来近似玻尔兹曼机中难以处理的对数似然梯度

18.[岭回归(Ridge regression)和主成分分析(PCA)的关系](https://zhuanlan.zhihu.com/p/32500133)

PCA暴力地将奇异值小的维度置为0，其他维度置为1；Ridge regression的惩罚系数对奇异值不同的维度的惩罚力度不同。二者都是通过消除数据的多重共线性来提升线性回归的效果，连接桥梁是SVD分解。

19.SVD分解本质上与不带激活函数的三层自编码机等价，理解SVD分解，能够为神经网络模型寻求一个合理的概率解释，同时[SVD可以实现自动聚类](http://kexue.fm/archives/4216/)，是通过概率模型，为SVD分解赋予了聚类意义。

20.PCA和SVD以及LSA(LSI)的关系

[文章一](http://www.cnblogs.com/LeftNotEasy/archive/2011/01/19/svd-and-applications.html)，[文章二](http://www.mamicode.com/info-detail-1402028.html)


