---
layout: post
title: "[论文笔记]《A Brief Introduction to Weakly Supervised Learning》"
excerpt: "data hungry场景下，也许需要弱监督。"
date: 2019-07-14 17:29:00
mathjax: true
---

最近着手实现一个公司内部使用的关系抽取框架，看了下开源的一些工作，主要关注点在模型。个人认为工业可用的框架要从数据层开始，甚至数据层要优于模型层。初步打算从snorkel开始，snorkel的一个核心就是用weak supervision做更多的数据。之前写过snorkel的文章，[snorkel相关论文阅读
](https://zhpmatrix.github.io/2019/06/05/snorkel/)，单纯讲模型的可以看之前的这篇博客，[神经关系抽取](https://zhpmatrix.github.io/2019/06/30/neural-relation-extraction/)，恰巧前不久看了周志华老师的这篇文章，今天又读了读，写点笔记。

这篇文章主要关注三种类型的弱监督问题：

>(1)incomplete: only a subset of training data are given with labels

比如说，为了做一个情感分析模型，可以从点评类网站上爬数据，这种数据自带标签值(点赞数，得分等)。但是爬取的数据仍旧有可能是不够的。

>(2)inexact: the training data are given with only coarse-grained labels

标签的力度太粗。比如要做一个命名实体识别模型，希望识别出“中国公司”，“国外公司”两种类型的实体，可是标签中只有“公司”一种类型。


>(3)inaccurate: the given labels are not always ground-truth

标签不准确。原因比较多，不需过多解释。

结合实际问题，上述三种类型甚至经常性的一块出现。出现问题就需要解决，解决方式如下：

>(1)incomplete: only a subset of training data are given with labels

active learning:

在给定标签的数据上训练一个模型，然后用该模型预测未打标签的数据，对置信度比较低的未打标签的数据，请求人类来打标签，然后将该数据加入原始训练数据集，继续循环。那么整个过程的目标就是：尽可能减少给一个未打标签的数据打上正确标签的向人类询问的次数。那么这里其实有两个目标：第一个是打正确标签，这要求训练的模型要好，要得到一个好的模型，需要训练数据要好，也就是提高每次选择的请求打标签的数据的质量，进一步说需要好的选择策略。第二个目标就是尽快结束整个循环过程。

semi-supervised learning(self-training):

和active learning方法不同的是，这个不需要人来打标签。也即是模型给未打标签的数据打上标签之后，直接放进训练数据集中循环。这里的一个关键问题是：为啥这部分直接加入的数据可以帮助学习？比起active learning，并没有来自人类的显式的信号输入。这里依据两个基本的假设，cluster assumption和manifold assumption，都是关于数据分布的假设，具体不再展开，可以看维基百科的具体解释(猜测周老师的这部分内容应该参考了不少维基百科的内容)。

在半监督的学习范式下，共有四类方法：

generative method:这类方法的出发点是未打标签的数据和打标签的数据应该生成自一个相同的模型，因此可以训练一个生成模型。

graph-based method:node表示样本，edge表示样本之间的关系，沿图进行标签传播。（在之前“拍拍贷”的一个问题相似度比赛中，就尝试了这种方式。）

low-density separation methods: 该类方法鼓励分类的决策边界沿着样本输入空间中密度较低的区域，主要代表方法是SVM相关的。

disagreement-based methods:这类方法通过产生多个模型，通过多个模型的合作给数据打标签，经典的Ensemble思想的运用，代表性方法是co-training，tri-training等。

**高能预警：**semi-supervised不是在所有场景下都有效的，也就是并不是一个安全的范式。文章中的表述是：

	We now understand that the exploitation of unlabeled data naturally leads to more than one model option, and inadequate choice may lead to poor performance.


transductive learning（semi-supervised的特例，测试集=未打标签的数据集）:


>(2)inexact: the training data are given with only coarse-grained labels

multi-instance learning，该类方法的理论分析较困难，几乎每个监督学习算法都有multi-instance版本(额，想想有点奢侈)。

假设训练数据集中的每个样本是一个包(Bag)，每个包都是一个示例(instance)的集合，每个包都有一个训练标记，而包中的示例是没有标记的；如果包中至少存在一个正标记的示例，则包被赋予正标记；而对于一个有负标记的包，其中所有的示例均为负标记。

这里可以分析的内容可以有很多，暂且提一下。


>(3)inaccurate: the given labels are not always ground-truth


learning with noise:目的在于识别，删除，修正可疑样本(标签可能是错的样本)。

crowdsourcing:voting等策略。

**结论：**除了上述三种弱监督类型，还有time-delayed supervision等其他类型；将二分类问题扩展到多分类，进一步到多标记问题时，上述讨论的方法会进一步变得复杂。




