---
layout: post
title: "Learning to Rank用于问答匹配/答案推荐建模"
tags: [NLP]
excerpt: "讨论问答匹配和答案推荐建模想法"
date: 2020-08-02 15:09:00
mathjax: true
---

"TopN推荐"是一个经典课题。一般来说，有三种经典的研究范式：

+ 回归建模。也就是给每个推荐品打个分。
+ 分类建模。针对二分类，预测推荐品用户是否喜欢；多分类，类别个数就是推荐品的个数，一种场景是根据用户的历史行为预测喜欢的物品[YouTube2016年的工作]。
+ 排序学习。

（1）point-wise/pair-wise/list-wise

在Ranking中，分类等价于point-wise。pair-wise的样本是由一个正样本+一组负样本构成，这里有两个样本的概念上的区别。list-wise是由一组有序样本构成。对于不同的问题，可以有不同的理解，在[文章](http://kubicode.me/2016/02/15/Machine%20Learning/Learning-To-Rank-Base-Knowledge/)中给出了一种针对给定Query下的三种方式解释。

在问答匹配场景下，理解如下：

|point-wise|pair-wise|list-wise|
|------|------|------|
|q0,a0,1|q0,a0,1;q0,a1,0;q0,a2,0|q0,a0,0.8;q0,a1,0.2;q0,a2,0.1（pair-wise是特例）|


（2）基于BERT和基于GBDT的Rank方式的区别

基于BERT的Rank方式主要体现在pair-wise的建模，样本构造方式同上，损失函数可以是基于margin的/基于ce的。

基于GBDT的模型主要以LambdaMART为代表，本质上借助于树结构在优化NDCG指标。模型在预测阶段的产出和上述基于margin的损失建模的产出相似，都是一个得分的形式。细节上，基于ce的理论上可以直接用于分类，但是理论上基于margin的可以通过对得分做变换（learning的方式/直接卡阈值）实现分类。

（3）问答匹配中的建模和答案推荐中的建模

问答匹配是指问题和答案的匹配，是一个较难的任务。理论上的建模方式上述三种都是可以的。但是考虑到样本标注的成本，point/pair是相对可行的方式。

在[答案推荐的评估指标设计](https://zhpmatrix.github.io/2020/08/02/answer-recommend-metric/)中设想了答案推荐的场景。理论上，point/pair/list都可以是该问题的候选建模方式。在该场景中的研究对象是问题和答案，因此特征的构建也要围绕二者，如下：

|类别|特征名称|特征解释|
|-------|------|------|
|问题/答案|长度|长的答案更好|
||TF-IDF/BM25/Embedding|句子本身的表征|
||频次|出现越多，越通用|
||时间|时效性|
|问题-答案|WMD||
||编辑距离||
||相关性得分|相关性模型|
||相似性得分|相似性模型或者基于向量检索的模型|

初步的流程图如下：

![img_](https://github.com/zhpmatrix/zhpmatrix.github.io/blob/master/images/%E7%AD%94%E6%A1%88%E6%8E%A8%E8%8D%90(L2R).png?raw=true)

补充：

《RankQA: Neural Question Answering with Answer Re-Ranking》，ACL2019的工作，在该工作中，给出了一些关于特征构造的启发。

![img_feature](https://github.com/zhpmatrix/zhpmatrix.github.io/blob/master/images/feature.jpg?raw=true)

参考：

1.[Learning to Rank学习基础](http://kubicode.me/2016/02/15/Machine%20Learning/Learning-To-Rank-Base-Knowledge/)

这篇博客中有关于pointwise/pairwise/listwise的图总结的不错。

2.[MatchZoo-py](https://github.com/NTMC-Community/MatchZoo-py)

3.[RankLib](http://people.cs.umass.edu/~vdang/ranklib.html)，结合具体例子讲解的两篇文章:

https://www.cnblogs.com/wowarsenal/p/3900359.html

https://www.cnblogs.com/wowarsenal/p/3906081.html

[lambdaMART在RankLib中的实现流程](https://blog.csdn.net/huagong_adu/article/details/40710305)

[一个具体例子讲解MART](https://zhuanlan.zhihu.com/p/81016622)

4.[ES中的_score得分计算](https://blog.csdn.net/paditang/article/details/79098830)

5.[投资知道：基于BERT的中文问答匹配检测](https://blog.csdn.net/zp563987805/article/details/104350670)

6.[投资知道：基于BERT的中文最佳答案推荐](https://blog.csdn.net/zp563987805/article/details/104406026)

7.《Dynamic Updating of the Knowledge Base for a Large-Scale Question Answering System》

主要内容：自动化问答库构建（主要是QA匹配的工作讨论）

作者：晓多科技（智能客服赛道的大玩家），江岭

亮点：有真实线上数据反馈

8.[(美团)深入浅出排序学习：写给程序员的算法系统开发实践](https://tech.meituan.com/2018/12/20/head-in-l2r.html)


**Expected Reciprocal Rank(ERR)**

与DCG相比，除了考虑位置衰减和允许多种相关级别（以R1，R2，R3…来表示）以外，ERR更进了一步，还考虑了排在文档之前所有文档的相关性。**举个例子来说，文档A非常相关，排在第5位。如果排在前面的4个文档相关度都不高，那么文档A对列表的贡献就很大。反过来，如果前面4个文档相关度很大，已经完全解决了用户的搜索需求，用户根本就不会点击第5个位置的文档，那么文档A对列表的贡献就不大。**

最直观的方案是Pointwise算法，例如对于广告CTR预估，在训练阶段需要标注某个文档的点击概率，这相对来说容易。<u>Pairwise算法一个重要分支是Lambda系列，包括LambdaRank、LambdaMart等，它的核心思想是：很多时候我们很难直接计算损失函数的值，但却很容易计算损失函数梯度（Gradient）。这意味着我们很难计算整个列表的nDCG和ERR等指标，但却很容易知道某个文档应该排的更靠前还是靠后。</u>Listwise算法往往效果最好，但是如何为每个请求对所有文档进行标注是一个巨大的挑战。

这篇文章中，作者应用了DDD的原则，分别是：**领域聚焦，边界清晰和持续集成**。基于上述原则，构建了三个在线排序领域模型，分别是**召回治理，特征服务治理以及在线排序分层模型**。

9.[RankNet: 排序学习算法的“在天之灵”](https://zhuanlan.zhihu.com/p/435989798)

这篇文章除了推导RankNet的损失函数之外，同时给出了个一个基于Python的代码实现，比较清晰。

10.《Methods, Applications, and Directions of Learning-to-Rank in NLP Research》,2024年的Review

LTR这个方向，除了经典的监督损失函数之外，还讨论了对比学习以及生成式模型（都2024年了，可以考虑生成式模型了）