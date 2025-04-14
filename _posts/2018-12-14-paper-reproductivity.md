---
layout: post
title: "从一个例子谈DL论文的复现问题"
tags: [NLP]
excerpt: "针对EMNLP2018关于对话生成的一篇文章《An Auto-Encoder Matching Model for Learning Utterance-Level Semantic Dependency in Dialogue Generation》，对实验复现过程的讨论和思考"
date: 2018-12-14 18:43:00
mathjax: true
---

这两天读到的一篇文章EMNLP2018的来自PKU的《An Auto-Encoder Matching Model for Learning Utterance-Level Semantic Dependency in Dialogue Generation》，[文章地址](https://arxiv.org/abs/1808.08795v1)，模型结构如下：

![模型结构](http://wx2.sinaimg.cn/mw690/aba7d18bgy1fy693onzqwj20gv0izmzo.jpg)

该模型用于对话生成，基准数据集是DailyDialog，Encoder端和Decoder端都是Auto-Encoder，中间的Mapping Module使用多层感知机，目的是两个端的中间表示尽可能接近。训练损失包含四项，分别是两个端的损失，中间Mapping的损失，整体的端到端的损失。测试的时候，数据从模型的左上角出发，经中间层，到右下角。

受文章所提结构的优雅简单吸引，决定跑一下实验。这里是[代码地址](https://github.com/lancopku/AMM)，针对该代码遇到的问题如下：

**第一. 超参数设置。**代码中给定了超参数，同论文中设置。Epoch=25，在文章中没有提到。

**第二. 数据集划分。**文章中的表达是将数据分为训练，验证和测试，利用验证集选择超参，然后合并训练集和验证集，基于选定超参在测试集上的结果。代码中显示的训练，测试集划分比例为0.8，没有基于验证集的模型选择相关代码。

为了尽可能还原实验结果，除了按照代码的README下载数据并放置到指定目录下，没有做任何代码上的修改。同时，将实验过程对照文章描述，尽最大可能保证实验过程的规范性，下面记录了实验过程结果和自己的一些想法。

原始论文结果(表1)：

|Models|BLEU-1|BLEU-2|BLEU-3|BLEU-4|
| ------ | ------ | ------ |-----|-------|
|Seq2Seq|12.43 |4.57 |2.69|1.84|
|AEM|13.55|4.89 |3.04|2.16|
|Seq2Seq+Attention|13.63 |4.99 |3.05|2.13|
|AEM+Attention|14.17| 5.69|3.78|2.84|


文章中称以BLEU-4作为主要的评估指标。针对上表，文章的分析结论是：

_The proposed AEM model **signiﬁcantly outperforms** the Seq2Seq model. It demonstrates the effectiveness of utterance-level dependency on improving the quality of generated text. Furthermore, **we ﬁnd that the utterance-level dependency also beneﬁts the learning of word-level dependency.** The improvement from the AEM model to the AEM+Attention model is 0.68 BLEU-4 point. It is much more obvious than the improvement from the Seq2Seq model to the Seq2Seq+Attention, which is 0.29 BLEU-4 point._

核心观点是说，从表格前两行看，BLEU-4的得分，AEM比Seq2Seq高了(2.16-1.84)=0.32。作者用**显著优于**来表达0.32个点的提升的含义。从表格第二行和第四行对比来看，AEM+Attention比AEM提升了0.68个点，而第一行和第三行对比，提升为0.29个点，按照作者对**显著优于**的认识，这个应该是**非常显著优于**的水平。针对于这个对比，作者的结论是，**句子级的依赖约束有助于单词级依赖的学习。**我对该实验条件以及得出的结论表示质疑，质疑理由是非严格对照组实验。按照作者的意思，AEM表示句子级依赖约束，Attention是单词级依赖的表示。但是AEM是包含句子级约束的完整模型，只有Mapping Module可以建模句子级约束，更重要的是Encoder和Decoder端都是Auto-Encoder，这显著区别于传统的Seq2Seq。不过从上表可以看出的是，**增加Attention之后，BLEU-4进一步提升，并且AEM提升显著多于Seq2Seq。**但是句子级依赖约束是否有助于单词级依赖的学习，结论应该不能直接得出。单词级依赖的学习不能有助于句子级依赖约束的加强吗？

暂且抛开上述结论的得出是否正确，作者想要通过实验表明的有两点，分别记为G1和G2：

G1：第二行(AEM)的BLEU-4比第一行(Seq2Seq)要高，并且当高于0.32个点的时候，可认为是**显著**；

G2：第四行(AEM+Attention)的BLEU-4 与第二行(AEM)的差要高于第三行(Seq2Seq+Attention)和第一行(Seq2Seq)的差； 


Epoch=25的结果(表2)：

|Models|BLEU-1|BLEU-2|BLEU-3|BLEU-4|
| ------ | ------ | ------ |-----|-------|
|Seq2Seq|13.69(+1.26)|4.95(+0.38)|3.00(+0.31)|2.19(+0.35)|
|AEM|13.02(-0.53)|4.66(-0.23)|3.78(+0.74)|1.91(-0.25)|
|Seq2Seq+Attention|None|None|None|None|
|AEM+Attention|13.02(-1.15)|4.46(-1.23)|2.65(-1.13)|1.83(-1.01)|

从上表可以得出：

1. **G1不成立**;

2. 从绝对指标值上看，**绝对误差的方差非常大**；

原始代码未动，重新跑一遍得出的结果：

|Models|BLEU-1|BLEU-2|BLEU-3|BLEU-4|
| ------ | ------ | ------ |-----|-------|
|AEM+Attention|12.94(-1.23)|4.55(-1.14)|2.69(-1.09)|1.84(-1.00)|

**显然代码未进行有效的种子设定**，但是**浮动范围姑且能够接受**吧。


从表2看出，结论G1不成立，为了进一步验证文章中所提模型的有效性，继续实验Epoch=40的结果：

|Models|BLEU-1|BLEU-2|BLEU-3|BLEU-4|
| ------ | ------ | ------ |-----|-------|
|Seq2Seq|13.37|4.47|2.87|2.00|
|AEM|13.39|4.87|2.99|2.12|

从上表看出，确实有提升了。并且从结果上看，和文章中的比较接近了。

继续实验...

Epoch=60的结果(表3，括号中给出了相对于原始论文中的差值)：

|Models|BLEU-1|BLEU-2|BLEU-3|BLEU-4|
| ------ | ------ | ------ |-----|-------|
|Seq2Seq|13.40(+0.97)|4.66(+0.09)|2.80(+0.11)|1.97(+0.13)|
|AEM|13.58(+0.03)|5.06(+0.17)|3.27(+0.23)|2.41(+0.25)|
|Seq2Seq+Attention|15.04(+1.41)|6.64(+1.65)|4.83(+1.78)|3.92(+1.79)|
|AEM+Attention|14.04(-0.13)|5.57(+0.08)|3.73(-0.05)|2.85(+0.01)|

从Epoch=60的表结果来看，可以得出：

1. 从相对指标值上看，**G1成立**，并且接近**非常显著优于**的标准；

2. 从绝对指标值上看，**绝对误差的方差非常大**；

3. 从相对指标值上看，**G2显著不成立**；这可能与第三行的绝对指标值绝对误差过大有关； 

此外，对比表2，表3中Seq2Seq过拟合；对比表3， 表2中AEM和AEM+Attention都欠拟合。

Epoch=90的结果如下：

|Models|BLEU-1|BLEU-2|BLEU-3|BLEU-4|
| ------ | ------ | ------ |-----|-------|
|AEM|13.77|5.25|3.46|2.60|
|AEM+Attention|13.88|5.34|3.55|3.69|

对比表3，AEM+Attention从前三个指标来看，过拟合；但是**BLEU-4提升有0.84之多**。再看，AEM的各项指标均有提升。可以得出什么结论呢？

我已经不想继续做实验了，从上述可以得出一些初步的结论：

第一. Attention是有效的。

第二. AMM大概率是有效的，但是这个结论的置信度较低。


回顾上述实验过程，由此有一些想法：

第一. 固定种子，保证实验的可复现性，无论对自己还是对源码开放者都是重要的。从实验室周围人的经历来看，会经常遇到开源代码种子不固定导致实验不能复现的尴尬，对自己的启发是，看到不固定种子的代码，首先要去质疑作者是不是_耍流氓_，既然为了造福社区放了代码，就不要让别人吐口水，或者好好写一写README文件。

第二. 对待结果不是显著提升的文章要格外小心，在实验控制不严格的条件下，可能怎样的故事都可以讲出来。读文章，还是要好好看实验条件和实验结果。

第三. 比较模型或者组件的优劣，实验到底怎么做值得深入思考，固定相同Epoch还是直到模型过拟合，无论是为了文章本身，还是为了防止后续研究者灌水扯淡都有好处。

参考：

[知乎关于商汤某篇CVPR论文的讨论](https://www.zhihu.com/question/276744581)















