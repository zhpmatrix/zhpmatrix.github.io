---
layout: post
comments: true
title:  "[搜索系统]《Enhancing Asymmetric Web Search through Question-Answer Generation and Ranking》"
excerpt: "通过问答对生成的方式强化非对称网页搜索"
date:   2024-09-24 16:35:00
mathjax: true
category: "论文笔记"
---

#### 基本信息

主题：通过问答对生成的方式强化非对称网页搜索

作者：Tencent PCG

会议：KDD2024

#### Motivation

网页搜索中，通常建模为一个Query和网页内容的非对称文本匹配问题，而非对称文本匹配由于语义空间的不一致，解决的难度高。因此，可以通过问答对生成的方式将一个非对称文本匹配问题转化为对称文本匹配从而降低问题解决的难度，提升网页搜索的效果。


#### 主要贡献

+ 提出了QAGeneration模块，可以利用大模型的能力离线生成高质量的QA对
+ 提出了QARanking模块，可以无缝集成全文匹配得分和QQ匹配得分，同时不增加在线时延
+ 对比SOTA，提出的QAGR方法，取得了8.7%的离线相关性提升和8.5%的在线参与收益提升


#### 主要过程

QAGR方法由两个模块组成，分别是离线条件下的QAGeneration模块和在线条件下的QARanking模块。离线模块用于给每个doc生成高质量的QA对，在线模块利用这些QA对用于下游检索任务。具体如下图所示：

<img src="https://github.com/zhpmatrix/zhpmatrix.github.io/blob/master/images/qagr_0.png?raw=true" width="400" align="center"/>

##### QAGeneration

离线QA对的构建主要分为三个步骤，分别如下：

（1）核心段落抽取

该阶段的目标主要是两个，分别是消除冗余信息以提升生成问题的质量，同时减少下游模型的输入。通过标注5000个样本，训练一个T5模型用于核心段落抽取。实际中使用这个模型做了百亿文档的核心段落抽取。

（2）Human in the Loop

针对抽取的核心段落，利用LLM通过提示词调优的方式抽取QA对，但是存在生成的格式和质量不满足要求的问题。通过instruct-tuning，显著提升了模型在垂域内的生成效果。


（3）问答验证

虽然通过第二步显著提升了生成的质量，但是仍然有可能生成无效的问题，比如给定生成的问题，在网页内容中找不到答案，以及生成的问题和答案并没有对齐。为了解决这个问题，文章训练了一个QA有效性判别的模型同时辅助人工规则用于过滤生成的问答对。

其中模型基于T5，输入包含问题，答案以及文档，人工的标注结果中通过的QA对作为正样本，不通过的做为负样本。

整体流程如下图所示：

<img src="https://github.com/zhpmatrix/zhpmatrix.github.io/blob/master/images/qagr_1.png?raw=true" width="400" align="center"/>

##### QARanking

Ranking分为两个步骤，分别是预排序和排序。

（1）预排序。计算Query和Question的terms covered，排序之后返回topN个Question。该阶段利用比较轻量的方法减少了不相关的问题用于流入下游检索阶段。

（2）排序。

用于排序的模型设计主要围绕对称孪生BERT展开，主体架构是Q-T-S&Q-Q双塔（共享参数），并融合意图特征，最后通过MLP把三路特征作融合。其中Q-T-S指Query-Title-Summary作为BERT的输入，Q-Q是指Query-Question作为BERT的输入，意图分为“基于关键词”和“基于自然语言”。如果是“基于关键词”，则希望得分更多来自Q-T-S，如果是“基于自然语言”，则希望得分更多来自QQ。整体流程如下：

<img src="https://github.com/zhpmatrix/zhpmatrix.github.io/blob/master/images/qagr_4.png?raw=true" width="400" align="center"/>

模型的复杂度从O(LH(S+S')^2)降低至O(LH(S)^2)，其中L是BERT的层数，H是隐藏层的维度，S是Query+Titlte+Summary的长度，S'是Query+Question的长度。实际中S‘<<S且由于是双塔结构，在计算的时候可以并行。

<img src="https://github.com/zhpmatrix/zhpmatrix.github.io/blob/master/images/qagr_3.png?raw=true" width="400" align="center"/>

为了训练这个模型，人工标注了query-document的相关性评级，从0到4共有5个级别。为了保证可解释性和稳定性，采用了pairwise和pointwise两种损失函数，其中前者是margin loss，后者是regression loss，回归损失的目的是希望模型能够学到绝对的ranking信息，使得模型具备一定的物理含义。对于只使用margin loss的模型，输出到得分只有在比较的时候才是有用的。

<img src="https://github.com/zhpmatrix/zhpmatrix.github.io/blob/master/images/qagr_2.png?raw=true" width="400" align="center"/>


#### 实验结果

针对该工作，作者分别做了离线评估和在线A/B，具体结果如下所示：由于实验条件较多，这里暂不列举，具体可以参照文章。

<img src="https://github.com/zhpmatrix/zhpmatrix.github.io/blob/master/images/qagr_5.png?raw=true" width="400" align="center"/>

<img src="https://github.com/zhpmatrix/zhpmatrix.github.io/blob/master/images/qagr_6.png?raw=true" width="400" align="center"/>

从离线评估来看，基于学术界和工业界的多个数据集，在多个评估量化指标上，对比其他多个方法，该工作均取得了最好的结果。在线实验也进一步证明了该方法的有效性。

#### 思考

+ 和大模型微调中，基于self-instruct的方式将非结构化的文本转化为可以微调的数据具有一致性
+ 核心段落抽取也可以利用LLM来尝试完成
+ QA对本质上是对非结构化文档的一个索引。从搜索内容角度看，搜索对象可以直接是QA库，也可以是非结构化文档，同时可以是基于QA对作为索引的非结构化文档。此外，未必采用本文的方法，也可以结合自己的场景，采用类似实验中的基线方法。类似方法包含[anthropicai最近的contexual retrieval](https://www.anthropic.com/news/contextual-retrieval)
+ QARanking不是很优雅。是不是可以直接路由？统一建模的效果？
