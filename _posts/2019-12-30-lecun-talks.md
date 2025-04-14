---
layout: post
title: "《Energy-Based Self-supervised Learning》"
tags: [技术杂文]
excerpt: "最近围绕Masked LM做了一些工作，个人对此很是感兴趣。这篇博客以Yann LeCun最近的一次报告为纲，梳理一些个人相对认同的观点和结论。"
date: 2019-12-30 18:53:00
mathjax: true
---

&#160; &#160; &#160; &#160;在之前的一篇文章，[《用Masked Language Model搞事情》](https://zhpmatrix.github.io/2019/11/05/mlm/)中系统梳理了一些围绕MLM做的事情，一直觉得MLM还有很多可以深挖的东西，恰逢看到LeCun最近的一个Talk，这篇博客就围绕Talk，做一个简单的梳理。

&#160; &#160; &#160; &#160;LeCun认为，"预测是智能的本质。"，围绕预测，监督学习范式要求预先标注一定规模的数据，强化学习需要在模拟环境下的较多试错，在游戏和模拟环境下工作良好，在真实环境下不一定。有没有其他的方式呢？

&#160; &#160; &#160; &#160;自监督学习。

&#160; &#160; &#160; &#160;在早期，很多时候大家更多用无监督来描述语言模型。但是，自监督是一个更合适的表达，首先承认了是有监督的学习方式。什么是自监督学习？

&#160; &#160; &#160; &#160;自监督学习=填空

具体的表现形式有：

+ 从past预测future
+ 从visible预测masked
+ 等等

总而言之：用输入中的一部分，预测输入中的另一部分。举两个例子，分别是自回归语言模型和自编码语言模型。

自回归：给定一个句子的前半部分，预测下一个字

自编码：随机mask掉句子中的一些token，预测这些token

虽然连续性空间，例如图片，视频，语音等都可以使用上述两种方式，但是，离散空间下的文本问题，还是最有效的。

一些证明自监督学习很有效的其他一些场景，如下：

+ Word2Vec
+ FastText
+ BERT
+ Cloze-Driven Auto-Encoder
+ 等等

从反馈强度上看，LeCun认为增强学习，监督学习和自监督学习的排序为：

自监督学习 > 监督学习 > 强化学习

从每个样本可以提供的信息量上来排序，如下：

自监督学习(millions of bits) > 监督学习(10->10000 bits) > 强化学习(a few bits)

围绕自监督学习，LeCun提出了两个方向：

+ low-resource场景下的层次特征学习
+ massive networks场景下的层次特征学习

除了自监督学习，这次Talk聊的另外一个话题是，基于能量的模型。为了训练一个基于能量的模型，有两类方法：

+ contrastive methods
+ arch methods

其中，BERT正是属于第一种，本质上是:

train a function that maps points off the data manifold to points on the data manifold.

Talk给出了七种策略去学习一个能量函数，而这些目前并不准备进一步研究，所以暂且不谈。

从整个Talk来看，围绕自监督学习可以说明下面两点：

+ LeCun在赌自监督学习的未来
+ 自监督学习已经用一些很强的工作证明了自己

&#160; &#160; &#160; &#160;虽然一直以来，大家都希望在无监督方向上做出一些工作，但是无监督一直没有特别亮眼的结果。自监督尤其在NLP任务上大放异彩。想象一下，只要拿到海量的数据，就可以直接做一个强有力的模型，这个模型可以learn到句法和语义的信息，可以作为多个下游任务的base模型，实在是一件特别fancy的事情！那么，围绕如何让这个基于自监督学习的模型学到更多自己想要的信息，很多人做了很多工作，[《用Masked Language Model搞事情》](https://zhpmatrix.github.io/2019/11/05/mlm/)中谈到一些，包括ICLR20，王威廉组仍旧会有一些工作，在这篇博客中同样有提到。

&#160; &#160; &#160; &#160;但是，自监督应该不是唯一的方法，尤其是自编码。可能在后续，会有一些更强有力，更加fancy的方法出现。

参考：

1.[Energy-Based Self-Supervised Learning](http://helper.ipam.ucla.edu/publications/mlpws4/mlpws4_15927.pdf)

2.[From System 1 Deep Learning to System 2 Deep Learning，Bengio, NeurIPS20](https://www.bilibili.com/video/av79356369)

3.[Self Supervised Representation Learning in NLP](https://amitness.com/2020/05/self-supervised-learning-nlp/)

用可视化的方式讲解了SSL在NLP中的几种范式。

4.[Self-Supervised Representation Learning](https://lilianweng.github.io/lil-log/2019/11/10/self-supervised-learning.html)

5.[自监督在NLP领域中的应用](https://www.zhihu.com/question/380119832?utm_source=qq&utm_medium=social&utm_oi=52727124066304)

6.[自监督学习的一些思考](https://zhuanlan.zhihu.com/p/150224914?utm_source=qq&utm_medium=social&utm_oi=52727124066304)

讨论自监督学习在CV上的应用，讨论了关于SSL的几个关键问题：

（1）如何定义自监督学习（没有标注数据；通过proxy task希望学到一些能够泛化的feature）

（2）为什么自监督学习能够学到信息？（先验；连贯；数据内部结构）

（3）设计一个自监督学习任务还需要考虑什么？（shortcut；歧义；任务难度）

7.[Self-supervised Learning 再次入门](https://zhuanlan.zhihu.com/p/108906502?utm_source=qq&utm_medium=social&utm_oi=52727124066304)

提出一个核心问题：如何将SSL和特定任务结合是一个有价值的方向。