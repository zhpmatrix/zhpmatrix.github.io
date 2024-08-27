---
layout: post
comments: true
title:  "[论文笔记]《A Surprisingly Simple yet Effective Multi-Query Rewriting Method for Conversational Passage Retrieval》"
excerpt: "SIGIR2024的文章，Query改写用于检索系统"
date:   2024-08-26 10:35:00
mathjax: true
---


#### 一. 基本信息
会议信息：SIGIR2024

关键词：对话式文本检索，Query改写

#### 二. 动机和贡献

对话式文本检索中存在的一个挑战是，由于在会话历史中，存在指代，遗漏和话题转换等问题，容易导致检索出不相关的文本。通常的一个解法是根据会话历史，通过Query改写，获取一个非情景化（de-contextualized）的Query用于下游检索。但是这种解法在部分场景下可能捕捉到不正确的意图，从而导致无法检索出正确的答案，根本原因在于Query改写是一个离散生成过程，可能无法准确的捕捉到潜在概率分布和词权重。

在一些工作中已经表明，对于相同的Query，通过整合多个改写后的Query能够进一步提升检索的效果，而beam search可以在没有任何附加成本的条件下，通过在每个生成步骤中考虑最佳的K个句子，而不是用贪心的模式选择最高概率的句子，天然生成多个改写后的Query且同时建模了词权重，方法简单有效且没有过多的计算成本。

该工作的主要贡献如下：

（1）比起当前主流的神经QR方法，能够以没有增加额外计算成本的前提下，产生多个Query

（2）能够以一种非常有效的方式将产生的Query用于sparse和dense检索中
（3）提出的方法在QReCC数据集中拿到了SOTA的结果

#### 三. 主要方法

##### (1) Query改写

通过微调一个生成式语言模型在每个轮次根据beam search的得分生成TopN个改写Query，每个改写的Query有一个改写得分如下：

![1](https://github.com/zhpmatrix/zhpmatrix.github.io/blob/master/images/cmqr_1.png?raw=true)

其中，t1,...,tl是预测的token，q(i,j)的**绝对值符号**是第i个轮次，第j个改写Query的长度，H是会话历史。考虑到RS是句子序列中词概率的乘积，改写得分会增加长度正则避免改写器产生非常短的改写结果。

##### (2) Sparse检索

sparse检索依赖bow文本表示，相关性的计算方式通常如下：

![2](https://github.com/zhpmatrix/zhpmatrix.github.io/blob/master/images/cmqr_2.png?raw=true)

其中w(t,q)表示与query相关的词权重，w(t,d)表示与document相关的词权重。改写的Query用于sparse检索时，主要关注w(t,q)。经典的做法是w(t,q)=c(t,q)，其中c表示频数统计。在该工作中，可以从n个改写的query中构建一个加权bow表示的query。具体分为两个步骤：

（1）每个改写query中的词权重，可以用beam search的得分来表示

（2）对于词集合中的每个词，词的权重可以通过对n个改写query中对应的词的权重进行求和取平均
本质上，上述方法通过n个query改写的结果，实现了query扩展和词权重的重估计。

##### (3) Dense检索

dense检索依赖向量表示，相关性的计算方法通常如下：

![3](https://github.com/zhpmatrix/zhpmatrix.github.io/blob/master/images/cmqr_3.png?raw=true)

其中h(q)表示query的向量表示，h(d)表示document的向量表示。针对第i轮的n个query，向量表示方式如下：


![4](https://github.com/zhpmatrix/zhpmatrix.github.io/blob/master/images/cmqr_4.png?raw=true)

最终的query的表示是n个query的加权，比之单个query，一定程度上增加了鲁棒性。

#### 四. 实验结果

采用QReCC数据集，共14k个对话，包含80k个问答对，数据集分割之后，得到测试实例8209个。采用的评估指标为MAP，MRR和Recall@10。采用的微调模型为t5-base，beam width为10，sparse检索的实现基于pyserini， dense embedding模型采用GTR(t5-based)。对比的baseline分别如下：

（1）manual rewrite。数据集中提供，人工改写的query

（2）T5QR(Manual)。一个比较强的基于t5的query改写模型

（3）Con-QRR。一个基于t5的利用强化学习优化检索性能之后的模型

（4）ConvGQR。利用两个t5模型，第一个进行query改写；第二个针对改写之后的query产生answer

（5）LLM(adhoc)。基于ChatGPT做query改写

（6）T5QR(LLM)。整体策略同（4），不同点在于基于10k的样本做了蒸馏。

具体实验结果如下，星号（*）表示最佳结果，下划线表示第二好的结果。

<img src="https://github.com/zhpmatrix/zhpmatrix.github.io/blob/master/images/cmqr_5.png?raw=true" width="400" align="center"/>

对比分析得到：

（1）该方法在sparse和dense两类检索中，各个数据集上都比对比的方法要好（除人工），这意味着该方法对于检索有效果上的提升。

（2）该方法取得了在QReCC数据集上的SOTA。

（3）虽然人工改写在TREC-CAsT数据集上取得了最好的结果，但是在QReCC数据集上，自动化的方法还是优于人工改写。

#### 五. 结论和启发

（1）提出了一种不增加额外代价的query改写方法，可以以一种比较简单的方式集成在sparse和dense的检索pipeline中带来效果的提升

+ 如何得到一个query改写模型？

蒸馏LLM的结果/利用线上搜索日志等

+ ES混搜架构中，如何利用这种改写方法？

dense检索相对直接，对于sparse检索来说，w(t,q)和w(t,d)是ES的内置操作。或者退化为一种计算关键词权重的逻辑用于召回
    
（2）两个需进一步探索的想法

（2.1）探索多query改写在精排阶段的用法

+ 对于n个改写query，每个query和document计算相关性，按照RS加权得到最终的相关性得分

（2.2）改写query个数的自动化选择

+ 目标和反馈的确定

改写后：

目标: 计算RS的平均分>=平均分阈值

反馈：K依次递增，判断是否满足条件。如果满足则退出，否则增加K的值，直到满足条件或者等于最大的K
改写中，根据logit来实现自动化等




