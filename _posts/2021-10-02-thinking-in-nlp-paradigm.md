---
layout: post
title: "[NLP]NLP中的范式转移"
excerpt: "宅在家里读的一些文章的笔记和想法"
date: 2021-10-02 11:40:00
mathjax: true
---

NLP的主流范式约有七种，包括分类，匹配，序列标注，阅读理解等，而在解决具体问题时，可以从一种范式转移到另外一种范式，甚至多种范式的综合使用，这称之为NLP的范式转移。具体如下：

---

![](https://s3.bmp.ovh/imgs/2021/10/54cae8f24fd05f34.png)

---


上图来自文章Xuanjing Huang组的《Paradigm Shift in Natural Language Processing》，其中的（f），全称为sequence-to-action-sequence，形式的表达为：

**A = CLS(ENC(X),C)**, 其中A是action的序列，C是configuration的序列。在每个时间步，模型基于当前text和当前的configuration，预测action。

这种方式主要应用于结构化预测任务，比如Parser相关。感兴趣可以读陈丹琦老板Manning或者西湖大学Yue Zhang的工作。

既然有了这些范式，那么范式之间是如何转移的呢？具体如下(图片来自[这里](https://txsun1997.github.io/nlp-paradigm-shift/))：

---

![](https://s3.bmp.ovh/imgs/2021/10/7f0942a3f685efb4.png)

---


以文本分类为例，传统的文本分类采用Class范式，该范式分为one-hot和multi-hot两种，对于multi-hot的问题，Class范式是一种次优范式。而通过将Class转化为Seq2Seq范式，有效利用label之间的交互信息。此外，label本身的语义信息在Class范式中也并未被充分的利用，而通过将Class范式转化为Matching范式,可以充分利用label中的先验信息,尤其是在数据资源较少的前提下。在预训练任务流行的现在，将Class范式转化为（M）LM的方式，可以充分利用预训练语言模型本身的能力。

除此之外，多种范式的组合也是范式迁移的范畴。

在将其他范式迁移到(M)LM的时候，其中一类非常重要的工作是Prompt-Learning。具体文章《Pre-train， Prompt, and Predict: A Systematic Survey of Prompting Methods in Natural Language Processing》，文章一作也是Xuanjing Huang老师组的，对应的[知乎文章](https://zhuanlan.zhihu.com/p/395115779)，评论区也有很多互动的观点很有意思。

这篇文章中，作者的思考问题的方式值得学习。其中一个总结是：在Fine-tuning的年代，我们希望语言模型能够尽可能的向下游任务靠近，而Prompting的年代，则是下游任务向语言模型靠近。我们经历了从使用预训练语言模型到使用了更强的预训练语言模型，到更好的使用了预训练语言模型的过程。整体上看，二者越来越近！

以Huang老师组的这两篇文章，具体可以展开非常多该方向上的研究，在此不再陈述。围绕上述工作，引发的一些思考如下。

（1）模态之间的范式转移是否存在？

一个典型的例子是2021年1月份的文章《Named Entity Recognition in the Style of Object Detection》，这篇文章将目标检测的思路用于NER任务，取得了和NLP传统方法相比comparable的结果。其中，目标检测中的方式是two-stage方法，NER是传统的标准方式。整体上，是CV的范式转向NLP的范式。

2021年9月的Hinton组的文章《PIX2SEQ : A LANGUAGE MODELING FRAMEWORK FOR OBJECT DETECTION》，用一个语言模型做目标检测。其中，语言模型是NLP中的标准范式。整体上，是NLP的范式转移到CV的范式。

这些探索能否将我们引向一个结论：一个统一的范式用于多种模态的问题求解。

（2）Prompt为什么会成为转移至(M)LM的关键操作？

在Fine-tuning的年代，我们倾向于将预训练语言模型作为一个更强的Encoder，但是随着探索的加深，我们认识到这个Encoder非常强，为了更好地挖掘Encoder的潜力，需要将焦点从下游任务转向Encoder自身。其中最简单的一条路径是适应Encoder的训练模式。比如对BERT而言，我们构造Mask的方式，而这就是Prompt的一种方式。范式转移过程中，考虑到Prompt和下游任务的适配，又会引发一系列的工作。

与之相关的一个角度是，研究中心从输出侧转移到输入侧，而对BERT的花式玩法，其实也正是存在于这两端。

其实，核心的思想都和朴素，都很直接。正如网络结构的设计，无论怎样，组件的选择有时候会受到维度对齐的影响，任何能够被设计的结构，都有自己的偏置。


（3）面向具体问题的范式选择逻辑是什么？

在上述两篇文章中，都没有找到比较有说服力的结论。不过，针对预训练语言模型，我们的逻辑是：用+用更强的+更好地用。但是，更多时候的问题是，PLM是不在选择空间中的。虽然文章中给出了各种范式的优缺点，但是只能成为一个出发点，并不能成为一个结论。

这也许很难得到一个结论。

不管怎样，这些范式，以及范式转移的逻辑，定义了一个有趣且庞大的探索空间，NLP的各种可能性均发生于此。
