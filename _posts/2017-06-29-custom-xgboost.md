---
layout: post
title: "[ML&DL]xgboost自定义目标函数和评估函数"
excerpt: "在有些比赛中，需要根据自己的需求来自定义目标函数和评估函数，就自己而言，目标函数需要自定义的场景不太多。为了充分发挥xgboost的框架作用，很多时候自定义评估函数的需求相对强烈。"
date: 2017-06-29 16:59:00
mathjax: true
---

<script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=default"></script>

**前言：**在有些比赛中，需要根据自己的需求来自定义目标函数和评估函数，就自己而言，目标函数需要自定义的场景不太多。为了充分发挥xgboost的框架作用，很多时候自定义评估函数的需求相对强烈。在之前的博文中提到复现Eve的时候，那篇文章主要是基于Keras，自定义了Optimizer，称为Eve。对于主流框架，模块即插即拔，因此我们需要插拔的手艺。文章主要从DMLC的demo出发，针对二分类问题，推导对数似然损失函数的导数，自定义评估函数。


二分类问题的对数似然损失函数如下：

$$
J(\theta)=-\frac{1}{m}\sum_{i=1}^{m}[y^{(i)}logh_{\theta}(x^{x(i)})+(1-y^{(i)})log(1-h_{\theta}(x^{(i)}))]
$$

一阶导数为：

$$
J^{'}(\theta)=-\frac{1}{m}\sum_{i=1}^{m}[y^{(i)}-h_{\theta}(x^{(i)})]
$$

二阶导数为：

$$
J^{''}(\theta)=-\frac{1}{m}\sum_{i=1}^{m}h_{\theta}(x^{(i)})[1-h_{\theta}(x^{(i)})]
$$

下面是DMLC中给出的一个DEMO：

<script src="https://gist.github.com/zhpmatrix/83846972e2631b94e38af4d25c2de797.js"></script>

xgboost.train中有两个重要参数: obj和feval。其中obj是目标函数，feval是评估函数。目标函数是模型优化的目标，直接用来衡量预测值和真实值之间的差距，常见的例如对数似然损失函数，均方差函数等。评估函数是对预测结果的评估，例如 R2-score等。

读上述代码，自定义了对数似然损失函数，在文档中说，自定义的函数通常要定义目标函数的一阶和二阶导数，但是二阶导数可以不定义。**XGBOOST在实现的时候用到了目标函数的二阶导数信息，不同于其他的GBDT实现，只用一阶导数信息**。在函数定义中，代码给定了grad和hess。上述结果是化简后的定义，没有化简的定义如下(_代码来自参考1_)：

<script src="https://gist.github.com/zhpmatrix/a36e185019b96b0f2349886cb9c75da0.js"></script>

feval的定义是应该预测为正的样本中预测错误的样本占总样本数目的比例。从直觉上来说，feval的定义是根据我们对预测结果的关注点来决定的。

通常的时候，可以把目标函数做为评估函数，比如RMSE。在有些数据挖掘比赛中，对于存在一阶导数和二阶导数的评估函数，看到过有些同学直接将评估函数作为目标函数。

下面是feval的f1_score定义，在二分类模型的预测评估中，当召回率(原来样本)和精确率(预测样本)发生冲突时有效评估模型质量的方式：

<script src="https://gist.github.com/zhpmatrix/48f47ce958715e7bad560f0eee05db0f.js"></script>

**总结：** 自定义是框架使用的高级技能，为了实现同样的目标，自定义不是必要的。但是通过自定义，可以用更少的代码更好的发挥框架的功能，比如，在每轮训练后打印评估函数的值。类似的事情如GridSearch实现网格搜索，并行调参。当然可以自己写cross-validation和并行处理，但是基于框架所提供的API，可以享受到诸多方便。


参考：

1.[携程比赛-客户流失率预测](http://www.cnblogs.com/silence-gtx/p/5812012.html)

[比赛](https://yunhai.ctrip.com/Games/6)中的评估函数相对特别，作者写了自己的feval。在文章中给了一个自定义obj，是对数似然损失没有化简的情形。
