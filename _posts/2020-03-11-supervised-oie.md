---
layout: post
title: "开放信息抽取-监督视角"
tags: [NLP]
excerpt: "开放并不意味着不能监督，监督视角下的开放信息抽取也是很有意思。"
date: 2020-03-11 10:25:00
mathjax: true
---

围绕开放域信息抽取，在去年做过一个[简单的梳理](https://zhpmatrix.github.io/2019/07/28/open-relation-extraction/)，幸运的是今年有机会重新看一些工作。这篇博客主要围绕监督式的开放信息抽取，该方向上的工作不是很多。

1.《Supervised Open Information Extraction》，NAACL2018

数据获取方式：利用SRL的标注语料来构造。类似的，可以用阅读理解的数据来构造。

新的BIO标注方式，支持抽取多个Arg。如下：

![img1](https://wx1.sinaimg.cn/mw690/aba7d18bly1gcq3t5apyrj213y0mfwk9.jpg)

三元组置信度得分计算。Token级别的prob相乘或者Word级别的prob计算，此处策略较灵活。

补充：

（1）《Span Model for Open Information Extraction on Accurate Corpus》有一些新的内容。

（2）《Supervising Unsupervised Open Information Extraction Models》

（3）《Improving Open Information Extraction
via Iterative Rank-Aware Learning》，围绕置信度的高端玩儿法。

2.《Overview of the Triple Scoring Task at the WSDM Cup 2017》

如何设计评估三元组的指标？给三元组打分（众包的方式），一种直观的标准是：“看到这个三元组有多么的surprised？”

补充：

（1）《Revisiting the Task of Scoring Open IE Relations》，SPO三元组打分也是一个重要课题。

3.[《Facts That Matter》](https://github.com/mponza/SalIE), EMNLP2018

 首次做事实显著性。技术手段为：PageRank+Clustering
 
 4.《Logician: A Unified End-to-End Neural Approach for
Open-Domain Information Extraction》，WSDM2018

和《Neural Open Information Extraction》一样，都是基于seq2seq的。不过，在要抽取的内容上和Magi非常类似，如下：

![img4](https://wx3.sinaimg.cn/mw690/aba7d18bly1gcq4qlhf1oj20wz09ejum.jpg)

5.《Learning Open Information Extraction of Implicit Relations from
Reading Comprehension Datasets》

提出一种从阅读理解的语料构造数据的方式，如下：

![img5](https://wx2.sinaimg.cn/mw690/aba7d18bly1gcq4v9300xj20ex0mpdir.jpg)

6.《Co-Clustering Triples from Open Information Extraction》

通过非负矩阵分解的方式针对SPO三元组做Clustering，联合聚类**predicate短语**和**subject-object对**。

7.《Supervising Unsupervised Open Information Extraction Models》

光看图，是不是就很感兴趣？

![img7](https://wx3.sinaimg.cn/mw690/aba7d18bly1gcq5h3waamj20ql0jwn0c.jpg)

总结，虽然博客中讨论了一些工作，但是实际上监督OIE的工作会带来很多问题，比如歧义的问题，比如需要信息融合，需要质量判断等。此外，在应用层上也需要一些新的思考。
