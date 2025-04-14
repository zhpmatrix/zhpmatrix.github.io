---
layout: post
title: "Idea from Bottou"
tags: [深度学习]
excerpt: "论文阅读。这篇文章主要讨论了深度学习中的优化问题。"
date: 2017-04-08 18:00:00
mathjax: true
---
<script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=default"></script>

首先，在摘要部分，作者提到了现在的两个主流研究方向：**减小随机方向的噪声(Noise Reduction)**和**利用目标函数的二阶导数近似(Second-Order Methods)**。下面是我根据论文中的内容和部分图示做的一个相对全面的图：

![optimization framework](http://wx4.sinaimg.cn/mw690/aba7d18bgy1fecyxswg57j20h30dl74a.jpg)

Schematic of a two-dimensional spectrum of optimization methods for machine learn- ing.

关于上述schematic的注解：

*1.* The horizontal axis represents methods designed to control stochastic noise; the second axis, methods that deal with ill conditioning.

*2.* The dotted arrows indicate the eﬀective regime of each method: the ﬁrst three methods can employ mini-batches of any size, whereas the last two methods are eﬃcient only for moderate-to-large mini-batch sizes.

*3.* Along this horizontal axis, one ﬁnds other methods as well. In our investigation, we classify two main groups as **dynamic sample size** and **gradient aggregation methods**, **both of which aim to improve the rate of convergence from sublinear to linear**. These methods do not simply compute mini-batches of ﬁxed size, nor do they compute full gradients in every iteration. Instead, **they dynamically replace or incorporate new gradient information** in order to construct a more reliable step with smaller variance than an SG step.An algorithm that optimizes the empirical risk R has access to an additional piece of information: **it knows when a gradient estimate is evaluated on a training example that has already been visited during previous iterations**.gradient aggregation methods make use of this information and improve upon the lower bound for the optimization of the empirical risk (though not for the expected risk). These algorithms enjoy linear convergence with low computing times in practice. Dynamic sampling approach, which, as we shall see, can match the optimal asymptotic eﬃciency of SG in big data settings. Employing a more aggressive stepsize sequence—of order \\(O(1/\sqrt{k})\\) rather than \\(O(1/k)\\), which is appealing in itself---it is this sequence of **averaged iterates** that converges to the solution. These methods are closer in spirit to SG and their rate of convergence remains sublinear, but it can be shown that the variance of the sequence of average iterates is smaller than the variance of the SG iterates.For this reason, we refer to the methods along the horizontal axis as noise reduction methods.

*4.* Along the second axis, in a broad sense, people attempt to **overcome the adverse eﬀects of high nonlinearity and ill-conditioning**.These methods improve **convergence rates of batch methods** or **the constants involved in the sublinear convergence rate of stochastic methods**, For such algorithms, we use the term second-order methods, which encompasses a variety of strategies;We discuss well known inexact Newton and quasi-Newton methods, as well as (generalized) Gauss-Newton methods, the natural gradient method,natural gradient method, which deﬁnes a search direction in the space of realizable distributions, rather than in the space of the real parameter vector w. Newton’s method is invariant to linear transformations of the variables, the natural gradient method is invariant with respect to more general invertible transformations. **Scaled gradient iterations such as RMSprop and AdaGrad are included**.**The primary advantage of Gauss-Newton** is that it constructs an approximation to the Hessian using only ﬁrst-order information, and this approximation is guaranteed to be positive semideﬁnite, even when the full Hessian itself may be indeﬁnite. The price to pay for this convenient representation is that it ignores second-order interactions between elements of the parameter vector w, which might mean a loss of curvature information that could be useful for the optimization process.(因为这篇文章是针对SGD的大规模优化问题的探讨，故在上图中没有给出Deep Learning中的相关梯度优化算法，他们主要是**基于动量的方法**，这部分内容在优化体系中占有非常重的位置！)


作者将两个主流研究方向展开为三个更为具体的问题：

(i) noise reduction methods that attempt to borrow from the strengths of batch methods, such as their fast convergence rates and ability to exploit parallelism; 

作者认为noise reduction方法是借鉴BGD(batch gradient method)的快速收敛和易并行特点。实际上，BGD确实是易并行的，并且由于利用了更多的样本信息，精度较高以至于全局最优，在博客中有关于自己实践的基于MPI的逻辑回归并行化，优化方法采用BGD，但是相比于SGD，SGD有更快的收敛速率，但是精度略差。

(ii) methods that incorporate approximate second-order derivative information with the goal of dealing with nonlinearity and ill-conditioning;

利用二阶导数信息来解决非线性问题和病态问题。

(iii) methods for solving regularized problems designed to avoid overﬁtting and allow for the use of high-dimensional models;

对含有正则项的方法的研究。

自己的研究方向是大规模机器学习系统，所以我对ml(optimization)+system(parallelism)的idea相对比较关注：

1.dynamic sampling方法。作者在文中提到，动态的mini-batch size可以做为步长衰减的替代，利用可变的mini-batch size可以在并行化的同时，充分发挥硬件的计算能力。


2.非凸问题的研究。作者给出了针对**Strongly Convex Objective/Nonconvex Objective,Fixed/Diminishing Stepsizes**的SG的bound分析，并提出analyzing the SG method when minimizing nonconvex objectives is more challenging than in the convex case since such functions may possess multiple local minima and other stationary points.针对非凸问题的研究，saddle point总是绕不过去的问题。

3.找到针对SGD的线性收敛算法依然具有吸引力，例如SVRG,SAG,本质是对梯度上界的改进(此处可参照上一篇博文)。

4.针对含有特殊regularizer的目标函数的优化，例如li Ita@Zhihu的NIPS 2016投稿。

5.SGD在分布式环境下对w的高频访问导致了通信负载，这对这个问题，现在有一些松弛后的同步算法或者一些异步算法。

6.纯优化问题：SG的渐近性能的脆弱性, SG与目标病态的关系, second-order methods improve the **constants** involved in the sublinear convergence rate of stochastic methods,Hessian matrix和generalized Gauss-Newton matrix的问题研究，典型的比如矩阵近似问题等。

7.针对坐标下降的非梯度算法的并行化(已经有人做过相关工作，比如利用CD求解LASSO问题),从直觉上来看，CD同样的简单，而且似乎CD也可以很好的做并行化。




