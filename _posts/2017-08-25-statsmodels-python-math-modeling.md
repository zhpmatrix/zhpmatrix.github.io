---
layout: post
title: "利用statsmodels做数学建模比赛"
tags: [Python]
excerpt: "最近备战华为杯数学建模竞赛，作为一个Pythoner，偏向于通过coding进行统计分析，主要是因为SAS和SPSS不会用，囧。"
date: 2017-08-25 12:20:00
mathjax: true
---

声明：数据挖掘和机器学习的背景并不是做数学建模的优势，数据挖掘和统计分析不同，统计分析有自己的一套方法论，诸如方差分析，相关分析，回归分析等。在工业界的数据挖掘比赛中，statsmodels可以用来做时间序列预测。

#### 一. 基本概念

1.某些分析的前提假设是数据服从正态分布，峰度和偏度是两个衡量指标，但是对峰度和偏度的使用要持批判态度。这两个概念读[这篇文章](http://blog.sciencenet.cn/blog-1148346-786610.html)就可以。

2.统计分析的内容补充。[想要学人工智能，你必须得先懂点统计学](http://www.toutiao.com/i6445836069198889485/), 这是一个短文系列，回顾了统计分析的基本概念，简单扼要，链接给出的是回归系数的显著性检验部分。

#### 二. 基本目标

1. 通过评估模型的拟合程度，判断模型对因变量的解释能力。
2. 模型预测因变量变化的显著性。
3. 自变量预测因变量变化的显著性。

对应的方法分别是**R^2，F检验，t检验**，相关重要指标是**p-Value**，QQ图。

#### 三. statsmodels的API

1.statsmodels.api:              基本API

2.statsmodels.formula.api:      公式API（支持用户自定义函数）
    
3.statsmodels.graphics.api:     图形界面API

#### 四. 统计分析思路(敲黑板！)

1.数据预处理：例如16年B题，按照碱基对的频率对碱基对编码数字化。

2.模型选择：基本没啥大的选择空间。分析清楚两点，第一，数据的假设分布是正态分布吗？LR的假设分布不是正态分布，但是线性回归要求是正态分布。第二，是分类还是回归，偶尔还要考虑一下因变量是离散类型还是连续类型。

3.分析summary中的关键指标：

R^2, p值(选择p值小的因变量)。辅助看一下t检验和F检验。

---
老司机分界线：

4. 好的线性回归理论上残差分布理论上应该符合正态分布(原假设)，要进行检验。

检验方法A：
   
    from scipy import stats
    z, p = stats.normaltest(logit.resid.values)

如果p值很小，拒绝原假设，即残差不服从正态分布，也就意味着并不是一个好的拟合，当然这个结论和R^2互相印证。

检验方法B：
    
    smg.qqplot(logit.resid)

如果数据基本分布在对角线上，则残差符合正态分布。

---

#### 五. 参数解释

线性回归的系数解释比较直观，但是由于Logit对线性组合做了映射，对系数解释没有很直观。在statsmodels中，通过边际效能函数**get_margeff()**来进行评估，边际效能函数是宏观经济学中的专有名词，数学意义就是导数了，或者说变化率。

statsmodels获取sumamry()结果，参照[这篇文章](http://www.statsmodels.org/dev/generated/statsmodels.regression.linear_model.RegressionResults.html)。一种具体的应用场景是，在进行变量选择的时候，获取所有变量的p值，然后作图或者排序。


#### 六. 赛题思路

回到赛题：考虑到本文主要服务于团队小伙伴们，故不对赛题背景进行说明。

寻找与是否患病相关的位点，可以基于模型，也可以基于检验。考虑到样本容量是1000, 样本维度是9445, 如果使用回归分析，维度添加一维(bias=1.0)，**样本矩阵奇异**。关于奇异，存在一个疑问？statsmodels中Logit模型默认Optimzer是Newton-Raphson方法(数值解)，不是解线性方程组(解析解或者闭式解),为什么还会出现Singular Matrix的问题？

自己Coding中采取了基于检验的方法，**X^2检验**。关于这种方法，参考[这篇文章](http://www.cnblogs.com/emanlee/archive/2008/10/25/1319569.html)，简单来说就是做统计，算期望。考虑到和机器学习的关系，这道题的这个小问可以归于变量(特征)选择。关于机器学习中的变量选择，这是目前自己看到的一个比较完整的[文章](http://www.cnblogs.com/jasonfreak/p/5448385.html)。检验方法如下：

    from sklearn.feature_selection import SelectKBest
    from sklearn.feature_selection import chi2

    #选择k(=2)个最好的特征，返回选择特征后的数据
    SelectKBest(chi2, k=2).fit_transform(X,Y)

分析基因(每个基因包含数目不等的位点)与是否患病的关系时，可以采取的一种思路是：针对每个基因进行分析，建立Logit模型，共300个Logit模型，Logit模型的输入是1000个样本，样本维度为该基因对应的位点。最后对300个模型进行**t检验**，按照p值进行基因选择。t检验评估的是模型对因变量的解释能力，解释能力强的模型(p值小)也意味着该基因与是否患病相关。

分析10个性状和是否患病的关系，思路同上。

从整体上感受这道题目：位点检测可以使用F检验+p值讨论，数据维度多，基因检测可以使用t检验+p值讨论，在数据子空间进行讨论(转换问题分析视角，降维)，性状分析和上述问题同质，数据量大。当然还有其他方法，限于时间关系，自己也没有去深入研究，比如讨论了位点的关系，可以直接利用位点的p值去讨论基因的p值，但是问题的关键是做检验。(_如何做检验，从这道题目来看，感觉自己刚上车呀。_)

具体代码(不完整)：移步我的Github, [点我读代码呀！](https://github.com/zhpmatrix/math-modeling-statsmodel)

欢迎开启数学建模之旅...🌹🌹🌹！！！

参考：

1.[线性模型学习笔记](http://www.cnblogs.com/NaughtyBaby/p/5603309.html)

主要学习用statsmodels模块进行线性回归、逻辑回归和时间序列分析。新手入门，快速数学建模比赛，这篇文章OK！如果想进一步深入理解一些概念，最好读一读统计学的相关教材。

2.[SelectKBest](http://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.SelectKBest.html)

3.两篇没有来得及读的文章

[文章0](https://www.datarobot.com/blog/ordinary-least-squares-in-python/)
[文章1](https://www.datarobot.com/blog/multiple-regression-using-statsmodels/)

4.[统计检验的一个小例子](http://www.chinadmd.com/file/stoxwtsxrxcwxsisrprxcwap_1.html)

5.[模型性能的比较检验](http://blog.csdn.net/sinat_33761963/article/details/55190474)

通常对于ML/DL中的模型的优劣比较是不通过统计检验的，但是这篇Blog总结了一些统计检验的手段。