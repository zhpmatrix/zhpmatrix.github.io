---
layout: post
title: "关于K-means变种的论文阅读"
tags: [论文笔记]
excerpt: "K-means是特殊情况下的高斯混合模型，关于K-means的各种改进论文，看作者看会议，真的有意思。K-means看似逻辑简单，关于该算法的研究一直没有停止过，ICML 2017就有三篇"
date: 2017-06-15 21:22:00
mathjax: true
---
<script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=default"></script>

(原始)K-means的几个主要问题如下：

1. 聚类个数需要人工指定

2. 依赖初始中心点(seeding)的选择

3. 时间复杂度高

k-means++是一种基于采样方法(称为**D^2-sampling**)的中心点选择方法，想法是：初始中心点尽可能远离。具体做法是：随机选择第一个初始中心点，计算其他点与该中心点的距离，按照距离远的以较大的概率被选中来选择第二个初始中心点，按照上述过程，顺次选择第三个，第四个，第K个(K为聚类个数)初始中心点。

从直觉上来看，这种想法是和聚类的目标保持一致，类内样本距离小，类间样本距离大。这种方法在一定意义上可以得出好的seedings，有助于问题2的解决。

附上原始文献：《k-means++: The Advantages of Careful Seeding》

很显然，上述方法在选择seeding的时候本来就是个**计算量大**的任务。为此有人提出基于MCMC的采样方法，具体做法是：随机选取一个seeding，然后用MCMC的方法采样出长为**M**的数列，取最后**（K-1）**个数作为中心点，target distribution是距离的函数，满足距离越远，概率越大(表达的含义同k-means++)，proposal distribution是一个常函数，1/样本数。

关于时间复杂度的表述，见原始文献(AAAI)：《Approximate K-Means++ in Sublinear Time》

是不是觉得上述的proposal distribution很特别(均匀分布)？上述的作者们换了这个proposal distribution，将与**距离有关的分布**作为一个term加入原始的分布中，据文章描述，这个提高了聚类的鲁棒性，也就是可以适应更多的数据分布假设，而非原来的一种均匀分布(严格地说是**产生数据**的分布)。

附上原始文献(NIPS)：《Fast and Provably Good Seedings for k-Means》

是不是觉得，这个自己也可以做？(不但要实验证明，还要有理论上的分析)从原始文章中看到，proposal distribution中关于距离的term和样本数目的term前的weight是1/2，会不会有些新的想法出现？此外，能否找到其他的采样分布进一步降低时间复杂度的同时，具有较好的鲁棒性？

我还没有进一步follow的想法。

附(我运行了AFK-MC2的源码，也就是NIPS中提到的算法)：

#### AFK-MC2源码运行配置

安装Cython模块：

    pip install cython

Cython解释器(生成kmc2.c文件)：

    cython kmc2.pyx

编译(.c)文件:

    sudo python setup.py build

安装(.c)文件:

    sudo python setup.py install

使用:

    import kmc2


参考:

1.[LDA-math-MCMC和Gibbs Sampling](https://cos.name/2013/01/lda-math-mcmc-and-gibbs-sampling/)

这篇文章讲了MCMC->MH->Gibbs的发展历程，同时谈了算法背后的直觉。文章存在明显的笔误。

2.[MCMC](http://blog.csdn.net/google19890102/article/details/51755242)

**概率转移矩阵是如何和一个对称分布对应的？** 参考[6]

3.[MH](http://blog.csdn.net/google19890102/article/details/51785156)

4.[Gibbs](http://blog.csdn.net/google19890102/article/details/51755245)

上述三篇是null的CSDN博客，很棒的博客。

5.[从随机过程到马尔科夫链蒙特卡洛方法](https://www.cnblogs.com/daniel-D/p/3388724.html)

回顾了几种典型的采样算法。

6.[MCMC: The Metropolis Sampler](http://www.cnblogs.com/yinxiangnan-charles/p/5018876.html)

解释了为什么需要使用对称分布去产生新的样本(状态)。

7.[蒙特卡罗积分](https://wenku.baidu.com/view/a3ee6a303968011ca30091e4.html)

举了一个比较详细的例子说明蒙特卡罗积分方法。

8.[漫谈Clustering](http://blog.pluskid.org/?p=39)

pluskid的博客文章，思考很有深度，读起来很爽。

9.[K-MC2](http://www.evanlin.com/til-2017-01-12/)

台湾人民的论文笔记

10.[fast-and-provably-good-seedings-for-k-means](https://zhuanlan.zhihu.com/p/25037146)

中国人民的论文笔记