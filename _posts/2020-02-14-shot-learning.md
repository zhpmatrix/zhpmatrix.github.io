---
layout: post
title: "[NLP]Few/Zero Shot Learning简单梳理"
excerpt: "同样是工业界的硬核问题。假设问题是有N个类，N很大，比如5000，每个类的样本只有10个。那么，任给一个样本，做5000分类，怎么办？"
date: 2020-02-14 10:25:00
mathjax: true
---

实际场景下的一个问题：比如在多分类问题中，某些类别的样本，特别少，但是仍旧要保持不错的效果。直觉上，这和DL方法论下的一般理解似乎不同，缺少数据，搞个锤子？这里有一个回答，[FSL满足PAC吗？](https://www.zhihu.com/question/325125054)此外，该方向上的工作，也可以作为AutoML的一个子分支。

整体上，不像Continual Learning，FSL/ZSL在NLP领域中的工作还是相对较多的。例如，FewRel数据集上的SOTA， ACL2019的工作，《Matching the Blanks: Distributional Similarity for Relation Learning》等。

[Humpback Whale Identification第一名的解决方案](https://www.kaggle.com/c/humpback-whale-identification/discussion/82366)

经典FSL建模的设定是什么？

怎么使用？

#### 基于度量的方法（最主要）

一般认为，FSL场景下，以DL模型为代表的参数化模型容易overfitting，因此，理想情况下需要一个非参数化的模型，代表如最近邻，K-近邻，K-means等。其实这些也是Metric Learning问题中经常讨论的方法。应用层上，人脸识别领域的工作较多。

+ 《Siamese Neural Networks for One-shot Image Recognition》

假设有N个类别，那么，首先可以构建Nx(N-1)类输入做负样本，也就是说，每次模型的输入是一个Pair，来自不同类，而正样本来自相同的类，作二分类任务。可以从几个角度思考：

第一：缺乏数据。假设N很大，同时每类样本很少，那么训练一个模型就很困难。这个时候，上述样本构造方式其实增加了样本量。

第二：简单模型。假设数据不缺乏的前提下，可以训练一个多分类模型，分类层会很重。现在用一个小模型，分类层很轻。也就是整体上，扩充了数据，减少了模型，最终得到的是一个特征抽取器。

那么，这个特征抽取器怎么用呢？

第一：抽取样本的特征，也即是一个多维向量，后接一个普通的分类器。一种理解是该特征抽取器压缩且抽取了原始样本的重要特征为一个多维向量。 这个时候再去训练一个分类器比原始样本直接开始训练要相对容易。

第二：任给一个样本，判断类别。本质上还是抽取特征，不过在预测类别的时候，需要该样本的特征和训练集中的样本的特征做对比，选择最相似的，这是一种离线的表达。操作上，可以是在线的待预测样本和训练集中样本进网络，判断相似度。

+ [《Matching Network for One Shot Leanring》](https://arxiv.org/abs/1606.04080),DeepMind

+ 《Prototypical Networks for Few-shot Learning》

+ 《Learning to Compare: Relation Network for Few-Shot Learning》

+ 《Induction Networks for Few-Shot Text Classification》

+ 《A Closer Look at Few-Shot Classification》，ICLR2019

#### 基于优化的方法

主要的观点认为：普通的梯度下降算法无法很好的处理FSL场景下的问题。

#### 基于模型的方法

Memory Argumented Model将训练数据当成sequence，来进行学习，是一个新奇的想法。


相关参考：

1.[Few-shot learning in NLP: many-classes classification from few examples](https://data4thought.com/fewshot_learning_nlp.html)

2.[论文笔记：Few-Shot Learning](http://www.zmonster.me/2019/12/08/few-shot-learning.html)，总结的非常全面的一篇论文，讲清楚了基本概念。

3.[阿里小蜜的意图分类平台的应用](https://mp.weixin.qq.com/s?__biz=MzI0NTE4NjA0OQ==&mid=2658360388&idx=2&sn=cf49a5d9810687eab3f6f7f8341dd6eb)，这篇文章梳理了几个工作，虽然文章提到是用于自学习平台上的一个挑战，但是似乎并没有提到很多关于相关工作在平台上的实际运行的效果。

4.《A Survey of Zero-Shot Learning: Settings, Methods, and Applications》

5.[Zero-Shot Learning in Modern NLP](https://joeddav.github.io/blog/2020/05/29/ZSL.html)

非常棒的总结，同时算是对文本分类任务在modeling方式上的一个探讨。当然可以用完形填空的方式做文本分类的任务。

6.[Meta-Learning is All you need](https://medium.com/@james_aka_yale?source=post_page-----3bd0bafdf289----------------------)

系统梳理了meta-learning的formula。