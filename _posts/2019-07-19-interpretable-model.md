---
layout: post
title: "《Interpretable Machine Learning》"
tags: [读书笔记]
excerpt: "A Guide for Making Black Box Models Explainable"
date: 2019-07-19 12:54:00
mathjax: true
---

看到这本书，特意翻了下微博**妖僧老冯_**之前的一条微博，这样写道：**"在机器学习里，Explainable 和 Interpretable 是不一样的。Explainable ML指的是构建另一个模型来解释一个黑盒模型，而Interpretable ML指的是模型本身在设计的时候就具备解释自己的功能。 ​​​​"**

所以，乍一看书名，齐了。暂且不去纠结到底该用哪个术语来表达问题，专注一下内容。想到上个月在微博乱写，**“当谈到解释性时，都在讨论什么？[doge]决策树，线性（Logistic）回归，Attention，Conv可视化，知识图谱(表示和推理)... ​​​​”**，恰巧看到这本书，就简单浏览一下，写了点笔记。

### 0.可解释方法的评判标准

>第一个角度：intrinsic or post hoc?

intrinsic是指：模型内在具有可解释性。比如一个决策树模型。这类模型一般称为intrinsically interpretable models。

post hoc是指：	先去训练一个黑盒模型，比如一个深度模型，然后应用一些可解释性的方法，比如度量特征的重要性。故又称之为model-agnostic interpretablility methods。


>第二个角度：outcome of the interpretability method

从解释性的输出来判断，可以输出为特征重要性统计，可视化，输入/输出对的分析等。


个人理解，能够从第一个角度做区分就可以了。那么知道如何区分之后，就可以具体看看这件事如何做了？分为三个路子，具体如下。

### 1.intrinsically interpretable models

具体包括Linear Model, Logistic Regression, Decision Tree, Decision Rule(if-then), RuleFit(不严格地，可以当成Tree来理解)，Naive Bayes, K-Nearest Neighbours等。 


### 2.model-agnostic interpretablility methods

好的的model-agnostic explanation system的三个特点：

(1)model flexibility: 不但对随机森林适用，同样适用于深度模型；

(2)explanation flexibility: 不受限于特定的解释形式，可以是线性，树形，和图；

(3)representation flexibility: 用来解释的特征表示形式是灵活的；

具体可用的方法包括如下：

**第一:**partial dependence plot

也就是衡量单一特征对output的影响。

**第二:**individual conditional expectation

衡量特征变化和实例预测输出的关系。

**第三:**feature interaction

**第四:**feature importance

三和四不做过多说明了。

**第五:**global surrogate models

这个比较有意思一些。用全局代理模型来解释一个黑盒模型。也就是用相同的数据训练一个intrinsically interpretable model，比如决策树等，假设输入和预测相同，就可以通过这个容易解释的模型来解释黑盒模型。

**第六:**local surrogate models

整体思路同上，不过是基于感兴趣样本进行的。通过在**距离感兴趣样本附近的一些样本上**重新训练一个容易解释的模型来实现目标。

**第七:**shapley value explanations

与博弈论有关的一个方法。每个特征是'game'中的一个'player'，预测是'payout'，通过shapley value可以告诉我们怎样公平地将'payout'分布到每个'player'上。

### 3.example-based explanations

**第一:** counterfactual explanations

**第二:** adversarial examples

对抗样本和反事实解释的方法类似，目的不同。前者希望构造样本去欺骗一个模型，后者希望去解释一个模型。不过对模型理解都是可行的。

**第三:** the cybersecurity perspective

与黑盒模型的攻击和防御相类似的是，网络安全的攻防。

**第四:** prototype和criticism

prototype是数据中最具有代表性的样本，criticism是数据中最不具有代表性的样本，后者对与insight的提供非常有帮助。

**第五：**influential instances

一些样本从训练数据中删除之后，对模型的参数影响较大，该类样本就是influential instances了。

**总结：**个人理解，对于容易解释的模型，一种是直接使用，另一种是辅助黑盒模型的解释。那么除此之外，对于黑盒模型的解释，可以“推推动动，拨拨转转”。需要考虑“推”什么？“拨”什么？这个可以从样本和特征的维度来做。“动”成什么样了？“转”到哪儿了？可以通过可视化的方式来做。目的是考虑“如何动”？和“如何转”？函数表达以及可能的因果关系。

这篇笔记中讨论了很多可行的方向。多数情况下，个人觉得比较实际的是做Case分析带来一些insight，有助于过程迭代，模型改进，模型解释。

参考：

1.[书的地址](https://leanpub.com/interpretable-machine-learning)

开源图书，同时有售卖。整体上的一个感受是，内容组织上有些乱，不过算是相对全面的该方向上的总结。

2.[用Attention机制作为解释性的手段](http://www.heatmapping.org/slides/2017_GCPR.pdf)