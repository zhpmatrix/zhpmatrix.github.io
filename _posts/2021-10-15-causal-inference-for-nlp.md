---
layout: post
title: "[NLP]因果推断+NLP"
excerpt: "这是一篇学习笔记，讨论因果推断和NLP的互动。"
date: 2021-10-15 11:40:00
mathjax: true
---

《Causal Inference in Natural Language Processing: Estimation, Prediction, Interpretation and Beyond》，相关的[中文解读](https://zhuanlan.zhihu.com/p/419734891)，对应的[参考文献列表](https://github.com/causaltext/causal-text-papers)。在该文章中，讨论了两个方向的关系：
 
 + NLP有助于因果推断
 + 因果推荐有助于NLP：interpretation&explanation/sensitivity&robustness

其中，第一个方向的研究对象是因果推断，NLP是辅助手段。第二个方向和第一个方向恰恰相反。下文中的例1表明第一个方向，例2表明第二个方向，其中涉及的具体因果概念如下（例子原文来自网络，表格和分析来自博主本人）：

**例 1** 一个在线论坛允许其用户在他们的个人资料中用一个图标表示性别。他们注意到，图标为「女性」的用户所发的帖子得到的点赞量要少一些。为了评估这一政策（允许用户在资料中提供性别信息），他们问了一个问题：被认为是女性会降低帖子的受欢迎程度吗？

|Treatment|Outcome|Confounding|Counterfactual Question|
|------|------|------|------|
|被认为是女性|帖子得到的点赞量|话题（图标为女性的用户所发的帖子可能更多的是关于某个话题的，而该话题本身就很难吸引人点赞）|如果我们操控了一个帖子的性别图标，它能得到多少个赞？|

在例1中，借助于NLP相关的技术，能够刻画Confounding，比如话题分析技术等，继而有利于因果分析。在本例中，文本作为Confounding，其他场景下，文本也可以作为Treatment或者Outcome，或者Mediator。

**例 2**
一家医学研究中心想要构建一个分类器，用于从病人医疗记录的文本叙述中检测临床诊断。这些记录汇总在多个医院站点，目标临床状况的频率和叙述的写作风格都有所不同。当分类器应用于训练集之外的站点的记录时，它的准确率会下降。事后分析表明，这个分类器在看起来不相关的特性上投入了很高的权重，比如格式标记。

|Treatment|Outcome|Confounding|Counterfactual Question|
|------|------|------|------|
|医疗记录文本|分类器的预测|医院站点（写作风格）|如果我们改变医院站点，同时保持真实的临床状态不变，分类器的预测是否会改变？（我们希望分类器依靠那些表达临床状况的短语来作出判断，而不是写作风格。）|

在例2中，反映了NLP模型的鲁棒性差的问题。借助于因果推断，分析影响NLP模型鲁棒性的因素，比如这里的写作风格，通过特定的提升鲁棒性的方法，比如对抗训练等，从而有助于NLP。

相关文章和工作：

+ [《A Survey on Causal Inference》](https://arxiv.org/abs/2002.02770)

+ [CausalML](https://github.com/uber/causalml)/PyLift/grf(uplifting models)

在读过一些文章，看过一些工作之后，博主形成的基本结论是：

+ 因果推断在一些更好的场景下有着实际的落地价值，比如A/B实验，营销定价策略等

+ NLP赋能因果推断，其实是一个NLP问题，和赋能哪个方向没有关系

+ 因果推断赋能NLP，是做NLP的同学要格外关注的一个方向，但是从目前赋能的问题看，理论性>实践性，短期内看不到特别的价值