---
layout: post
title: "论文阅读-《Language Models are Unsupervised Multitask Learners》"
tags: [NLP]
excerpt: "GPT-2的论文阅读，陈述了主要内容，比较了实验结果，并提出了关于该模型的几点思考。"
date: 2019-02-16 18:43:00
mathjax: true
---

<script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=default"></script>

#### 前言

这里的多任务可能会让人误解，文章中更多地想要表现一种观点。Transformer+多任务，感觉可以去看微软那篇文章，见参考5，前些日子在GLUE上屠了Transformer的那篇，中规中矩。

#### 什么样的数据集？

WebText(millions of webpages，40GB of text)，来自Reddit。

#### 多大的模型？

GPT-2在GPT的基础上做了微小的修改，其中包括：

第一：LayerNorm的移动和添加；

第二：修改后的残差层的权重初始化策略(每层的初始化权重随层数加深而变小)；

第三：扩大词表；

第四：增加context size和batch size；

GPT-2(1.5B parameter Transformer)，即使这样，模型仍然没有过拟合WebText，意味着模型的参数可以更多，迁移任务的性能可以进一步提升。对于模型容量的认识，给一个表格：

| BERT | VGG-16 | VGG-19 |ResNet-101 | GPT-2|
| - | - | - |-|-|
| 3.3亿 | 1.38亿 | 1.44亿 |0.10亿|15.00亿|

#### 任务设定是啥？

给定一个文本中前面的所有单词，预测下一个单词。

#### 有效吗？

不需要显式的监督学习，模型就可以用于非常多的任务(例外下谈，实际上这些例外很重要)且取得SOTA结果！

#### 有效性的来源？

语言模型+数据集(规模巨大，多样性巨高)

#### 缺点是啥？

比之BERT，GPT有的问题，GPT-2都会继承。无监督的通病，收敛慢。问答，阅读理解，翻译和摘要任务成绩一般(语言建模任务成绩优秀)。相关结果如下：

##### 自然问答

![自然问答](http://wx1.sinaimg.cn/mw690/aba7d18bgy1g07sgevxwrj20kf0bqt9f.jpg)


##### 摘要

![摘要](http://wx4.sinaimg.cn/mw690/aba7d18bgy1g07sfsqhw6j20ke0boab5.jpg)


##### 阅读理解

![阅读理解](http://wx3.sinaimg.cn/mw690/aba7d18bgy1g07sfoj7sqj20kj0bwwfk.jpg)

##### 机器翻译

![机器翻译](http://wx3.sinaimg.cn/mw690/aba7d18bgy1g07sfjrjoej20ki0c0ab6.jpg)

##### 常识推理-代词消解

![常识推理-代词消解](http://wx2.sinaimg.cn/mw690/aba7d18bgy1g07sl38ae7j20kf0byjsd.jpg)

##### 语言建模

![语言建模](http://wx1.sinaimg.cn/mw690/aba7d18bgy1g07sff2nsbj20kl0bx3zf.jpg)

从上述结果来看，印证了文章所说，在语言建模任务上成绩优秀(常识推理-代词消解，语言建模)，其余表现一般(CoQA表现尚且可以)。


#### 结论是啥？

传统的经验认为性能提升来自：大规模的数据集+大容量的模型+监督学习。而这篇文章则用实验证明了在NLP领域中，性能提升可以来自：大规模的数据集+大容量的模型+无监督学习(语言模型)。对于NLP而言，无标注的数据量非常大，因此挖掘出无监督学习的能力则成为了一个重要命题。传统解决NLP问题的方式是针对一个任务，构造一个数据集，训练一个模型。而GPT-2的出现，证明一个数据集，一个模型，可以很好地解决多个任务。

#### 几点思考？

第一：复现实验的成本极高，几乎意味着不可能；因此期望作者放出预训练的模型，但是作者目前并没有相关意愿，实际上基于多种语言的预训练模型实用价值更大，在该问题上，BERT做的非常出色，因此可以看到围绕BERT的后续工作也相当的丰富。

作者认为放出预训练模型，会使得模型用于不该使用的地方，比如假新闻的产生等。该理由略显牵强，不做过多讨论，实际上由此引发的一个问题是虚假新闻检测的任务，是一个值得深入挖掘的方向。在CV领域，围绕同质问题的研究已经很丰富了，比如围绕活体检测的一些工作。

不过，作者还是放出了一个[117M大小的模型](https://github.com/openai/gpt-2)，也就是文章中四个模型中最小的。GPT-2大模型和小模型的效果对比参考7。

第二：适用于基于语言模型的文本生成任务。比如写作助手，围绕该任务，可以基于字，词，句子，甚至段落等粒度。个人认为，当模型用于该任务时，主要得益于数据集(WebText)和大模型(15亿)带来的增益。除此之外，包括对话生成，无监督的机器翻译等。

第三：上文可以看到，常识推理任务表现优秀。或许可以在Kaggle最新的一个比赛[Gendered Pronoun Resolution](https://www.kaggle.com/c/gendered-pronoun-resolution)上尝试。

第四：从务实角度出发，个人认为文章的主要贡献在于训练了一个超大容量的语言模型。从务虚角度出发，文章进一步表明，语言模型和无监督学习在NLP领域的潜力，一个模型解决多个NLP任务是可行的，期待后续相关工作的出现和完善。从写作上来看，文章的系统性也是非常值得学习的。比如实验的设计，记忆和泛化的分析方法(_通过暴力方式记忆近似全集，如果可以有效解决问题，未尝不可？_)等。

第五：GPT-2是一个基于语言建模的文本生成器，由于语言建模本身的通用性，因此它可以提升多个任务。但是从目前的实验结果来看，有效提升任务类型并不包括诸如机器翻译，文本摘要等任务。大的数据集和大的模型，由经验结果得到，理应有好的性能提升。这一方面解释了为什么认为媒体对该工作过誉了，另一方面解释了实验结果，它本应如此。

第六：GPT-1是预训练+Fine Tuning的两个阶段任务；GPT-2没有Fine Tuning的过程，直接用训练得到的语言模型用于下游文本生成任务(借助引导符完成)。具体是如何做的，需要进一步思考。关于引导符的使用，可以参考[我在知乎和知友的讨论](https://zhuanlan.zhihu.com/p/56865533)，观点在评论区。

#### 实验结果(117M的小模型)

##### 无条件样本生成的两个例子：

<script src="https://gist.github.com/zhpmatrix/17e2459875833242ce75b3cd98dca3f8.js"></script>

<script src="https://gist.github.com/zhpmatrix/0e76545415b0130b2785fe4dc572c90c.js"></script>

##### 有条件样本生成的两个例子：


<script src="https://gist.github.com/zhpmatrix/940abd7ad28f67c18a805011e0d4a6b5.js"></script>

上述这个例子有点代码生成的感觉了，可以看到正确的函数声明已经实现。个人比较好奇的是这些代码片段是不是直接从原始数据集中extractive/copy的？由于没有原始数据集，因此暂时无法验证。

<script src="https://gist.github.com/zhpmatrix/3940b0db085643b9c5956e34a80a102d.js"></script>






参考文献：

1.[DeepTech报道](https://zhuanlan.zhihu.com/p/56798510?utm_source=qq&utm_medium=social&utm_oi=52727124066304)

2.[Better Language Models and Their Implications](https://blog.openai.com/better-language-models/)

3.[机器之心的报道](https://mp.weixin.qq.com/s?__biz=MzA3MzI4MjgzMw==&mid=2650757118&idx=1&sn=a777dabb78f055fbfb451f2e75d5a7d5&chksm=871a9380b06d1a9639351bc4352a897104dcca16883c02aa5301e61da149845fdc09ac4bbfb3&mpshare=1&scene=23&srcid=%23rd)

4.[新智元的报道](https://mp.weixin.qq.com/s?__biz=MzI3MTA0MTk1MA==&mid=2652038485&idx=1&sn=e5623e1df705fca9cd72679a5210f094&chksm=f12191a4c65618b22662101f3c33aacb7ba308dde8041b41599163305e02bae5afd7094ba4b8&mpshare=1&scene=23&srcid=%23rd)

5.《Multi-Task Deep Neural Networks for Natural Language Understanding》

6.[量子位的报道](https://mp.weixin.qq.com/s/Viyc66ywVBsrnQUdYvK8ow)

7.[GPT-2大模型和小模型的效果对比](https://mp.weixin.qq.com/s?__biz=MzIzNjc1NzUzMw==&mid=2247514504&idx=2&sn=736c42eb98712fa918371b59a3e55db1&chksm=e8d00efadfa787ece0622ef8f6abec918f1d91c64c8e056d9c0d0542cb136c1fddd85298f922&mpshare=1&scene=23&srcid=%23rd)

8.[张俊林的解读](https://zhuanlan.zhihu.com/p/56865533)

9.[虚假新闻检测的调研](https://mp.weixin.qq.com/s?__biz=MzIwMTc4ODE0Mw==&mid=2247495009&idx=1&sn=786d5297ba95117e72cb2e46a22d2935&chksm=96ea32e1a19dbbf7c9653338be329c2a78b21b7660f4696b13812512cac7c647f7c132d14309&mpshare=1&scene=23&srcid=%23rd)















