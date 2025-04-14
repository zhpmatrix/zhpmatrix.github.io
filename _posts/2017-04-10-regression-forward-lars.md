---
layout: post
title: "Regression Forward Lars"
tags: [深度学习]
excerpt: "论文阅读。这篇文章主要讨论了回归问题中的LARS算法。"
date: 2017-04-10 18:00:00
mathjax: true
---
<script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=default"></script>

首先给出线性回归的问题描述：

设\\(X^T = (X_1,X_2,\cdots,X_p),\theta^T = (\theta_1,\theta_2,\cdots,\theta_p)\\),我们希望找到这样一个回归函数:

$$h_\theta(X) = X^T\theta$$

我们的loss function构造如下:

$$J(\theta) = \frac{1}{2}(h_\theta(X) - Y)^T(h_\theta(X) - Y)$$

要使得loss function最小，我们可以直接得到一个closed solution或者采用基于梯度的优化算法。下面直接给出在\\(L_2\\) regularizer和没有regularizer的情况下对应的\\(\theta\\)：

有正则项+Gradient: \\(\theta = \theta - (\beta X(X^T\theta - Y)+\alpha\theta)\\)

有正则项+closed solution: \\(\theta = (XX^T+\alpha E)^{-1}XY\\)

无正则项+Gradient：\\(\theta = \theta - \beta X(X^T\theta-Y)\\)

无正则项+closed solution:\\(\theta = (XX^T)^{-1}XY\\)

假设使用\\(L_1\\)范数的情况呢？在这种情况下，我们依然可以得到closed solution，但是由于\\(L_1\\)范数在零点不可导，故不能使用基于梯度的方法。那么解决这类问题的典型方法是坐标下降算法和最小角回归算法。坐标下降算法和最小角回归不是只能用来解决LASSO回归问题，例如最小角回归还可以结合混合高斯做聚类。

最小角回归是前向选择回归算法和前向逐段回归算法的结合。这部分内容结合三张图来说明：

**forward selection:**

![1](http://wx2.sinaimg.cn/mw690/aba7d18bgy1fehtouo56gj20eu07bglt.jpg)

在上图中，\\(X_1,X_2,X_3\\)代表训练样本的一个feature，\\(Y\\)是目标向量，从未被选择的feature集合中，开始选择和Y的距离最近的feature，在选定的feature上做Y的投影向量，然后继续从未被选择过的feature集合中，选择和（Y-Y在选定feature上的投影）向量距离最近的向量，直到所有feature都被选择过或者(Y-Y在选定feature上的投影)为0。这里（Y-Y在选定feature上的投影）代表残差，由于在选择feature的时候，采用比较暴力的方式(投影相比于下个算法的伸缩)，故结果精度较差。

**forward stagewise:**

![2](http://wx2.sinaimg.cn/mw690/aba7d18bgy1fehtophdg0j20db0823yy.jpg)

该算法和上述算法不同的地方在于，每次选择完距离最近的feature向量后，不是做投影，而是沿着选定feature的方向做伸缩后得到一个新的向量，然后重新选择feature向量，这样，已经被选择过的向量可能重新被选择。对于与上述算法，该算法精度较高但是迭代次数较多。

**lars:**

![3](http://wx3.sinaimg.cn/mw690/aba7d18bgy1fehts4mgoyj20sg0lc766.jpg)

lars算法是结合上述两个算法的各自优点以达到快速，精度高的目的，具体过程不在描述，可参考给出的文章，上图是自己画的一个三维场景下的算法过程(似乎网友贡献的都是二维的，论文中的图也是二维的)，可以帮助理解。

**思考总结**: 针对上述算法，一个很自然的想法是做数据并行，在选择距离最近feature的时候，可以并行的处理这个问题。但是，更进一步的考虑是，能够将feature进行分组，然后各组同时进行，最后结果汇总，就是一个分治的过程，如果这样得到的结果和期望结果gap比较大，存不存在一个可接受gap的松弛算法?

**参考**：

1.[《LEAST ANGLE REGRESSION》](http://statweb.stanford.edu/~tibs/ftp/lars.pdf)

这是一篇原始论文，大四做毕设的时候第一次接触到，还没有系统的读过。

2.[LASSO回归网友笔记版](http://www.cnblogs.com/pinard/p/6018889.html)

3.[向量投影](http://www.cnblogs.com/graphics/archive/2010/08/03/1791626.html)

我的一个理学院的朋友和他聊问题的时候，竟然要翻下这个概念，被打脸，囧。

4.[郝智恒在统计之都的几篇文章](https://cos.name/author/bigknife/)
