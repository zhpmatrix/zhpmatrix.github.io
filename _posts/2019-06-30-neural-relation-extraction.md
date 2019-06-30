---
layout: post
title: "[知识图谱]神经关系抽取"
excerpt: "总结18年，特别是19年到现在的一些关于实体识别和关系抽取的工作。其中多数是自己在近期的工作中主要参考实现并且证明有效的工作，算是对近期工作内容的一个总结。"
date: 2019-06-30 18:43:00
mathjax: true
---

前言：主要总结最近关于关系抽取的一些工作和思考。


### 从一个具体例子了解信息抽取

信息抽取是一个大的研究方向，从ACL2019的文章录用可以看到。近年来，围绕知识图谱的研究也是一个热点，包括我们组里在知识图谱都有相关人力投入，围绕知识图谱的相关工作也是非常的有意思。而信息抽取相关技术则是知识图谱构建的基础。

一般认为信息抽取有三个基本任务：

（1）实体识别

（2）关系抽取(分类)

（3）事件抽取

或者更加一般地认为前两个任务。为了直观地理解上述概念，下面通过一个纽约时报的新闻实例，演示上述过程(_例子引用参考文献1_)：

```

(1) 实体标注： 

[Julian Hill]<人名> , a research chemist whose accidental discovery of a tough , taffylike compound revolutionized everyday life after it proved its worth in warfare and courtship , died on [Sunday]<日期> in [Hockessin , Del]<城镇名> . He was 91. 

[Hill]<人名> died at the ［Cokesbury Village］<城镇名> retirement community , where he had lived in recent years with his wife of [62 years]<时段> , [Polly]<人名> . 
......... 
[Julian Werner Hill]<人名> was born in [St. Louis]<城镇名> , graduated from [Washington University]<学校名> there in [1924]<年代> and earned a doctorate in organic chemistry from the [Massachusetts Institute of Technology]<学校名> in [1928]<年代> . 
......... 

(2) 关系抽取： 

职位: research chemist ← Julian Hill 
年龄: 91 ← Hill 
出生地: St. Louis ← Julian Werner Hill 
工作单位: Du Pont Co. ← Julian Werner 
毕业学校: Washington University ← Julian 
毕业学校: Massachusetts Institute of Technology ← Julian 
配偶: Polly ← Julian Hill 
特长: an accomplished squash player and figure-skater ← Julian 

(3) 事件抽取： 

<死亡事件> 何人：Julian Werner Hill 何时：Sunday 何地：Hockessin , Del 
<发明事件> 何人：Julian Hill 何物：nylon　何时：1930s 
<毕业事件> 学校：Washington University 何时: 1924 何地：St. Louis 
......... 
```

那么，通过上述三个过程，可以得到最终想要的一个结果，如下：

```
【Julian Hill 概览】
 
姓名：Julian Werner Hill 
年龄：91 
性别：MALE 
职务：research chemist 
工作单位：DuPont Co. 
教育背景：Washington University; Massachusetts Institute of Technology 
配偶：Polly 
儿女：Louisa Spottswood; Joseph ; Jefferson 
特长：an accomplished squash player and figure-skater 
相关事件： <死亡事件> ；<发明事件>；<毕业事件> ；
......... 
```

从整体上看，输入是一段文本，输出是结构化的信息。那么，目前的技术水平是怎样的呢？(引用同上，从最近读的一些文章来看，这些指标基本合理)

```
三大任务中，专名标识是基础，也是最成熟和已经得到广泛应用的技术。

(1)如果领域已经确定，标识的准确度可以达到90％左右，已经接近人工标注的水平。

(2)实体关系的抽取近年来有长足的发展，抽取的准确度可达80％。

(3)复杂事件由于其动态性，抽取难度最大，抽取准确率大体在50％－60％徘徊，尚不足以投入应用。
但是单纯的事件，比如高管变动，恐怖事件，以及抽取一般事件中的谁做了什么及其事件的时间地点等，
抽取的质量也可以达到70%到80%。

(4)事件抽取系统的真正难点在领域的移植性（domain portability），一个开发了多年的系统一旦应用领域变换，重新定义了目标模板，非动大手术不能适应。
```

### 解决的思路

关系抽取是一个研究了很长时间的问题，自己做的内容偏向于DL的方法，这里暂且不讨论事件抽取，围绕实体识别和关系抽取两个事情。为了解决这两件事情，有两个大的思路方向：

第一：一个模型解决两件事情；

这个思路上的尝试，主要基于这篇文章，《Joint entity recognition and relation extraction as a multi-head selection problem》，这篇文章也是百度2019年在信息抽取赛道上第一名主要采用的一个方案。

第二：两个模型分别解决实体识别和关系抽取；

这里，可以把实体识别理解为一个sequence labeling任务，关系抽取理解为一个multi-classification或者multi-label问题（更加倾向于前者）。

那么，这里思路就相对清晰了，bert的参与应该少不了。实际上，在2019年的一些文章中正是基于bert来做的。

实体识别直接基于bert来做，可以后接一个crf层，这里不是关注的重点。而关系抽取这块主要参考实现的文章是acl2019年的《Matching the Blanks_Distributional Similarity for Relation Learning》，同时会融合一些其他文章的想法，具体包括两篇文章：

1.AKBC2019，《Improving Relation Extraction by Pre-trained Language Representations》

2.《Simple BERT Models for Relation Extraction and Semantic Role Labeling》，arXiv，2019


严格意义上的神经关系抽取，按照读的一些文章的形式上的定义，是给定句子或者段落，以及两个或者多个实体，给出实体间的关系。其实这句话中，已经给出了两种setting：context和实体个数。一般研究较多的setting是一个句子+两个实体，给出关系。其中，针对context，需要特别提出的是，刘知远团队等在今年的acl2019上给出了一个文档级的关系抽取任务数据集，具体文章《DocRED: A Large-Scale Document-Level Relation Extraction Dataset》，**一句话总结：传统的数据集解决句子级的关系抽取，可以解决60%左右的问题，剩下的40%的关系需要从多个句子中挖掘。**

### 具体的模型

针对神经关系抽取，在《Simple BERT Models for Relation Extraction and Semantic Role Labeling》中，具体做法如下：

![img1](http://wx4.sinaimg.cn/mw690/aba7d18bly1g4ilg9r9ecj20vc0p2dk4.jpg)

比较值得一提的有两个地方：

第一是mask操作，作者在文中写道：“To prevent overﬁtting, we replace the entity mentions in the sentence with masks, comprised of argument type (subject or object) and entity type (such as location and person), e.g., S-LOC, denoting that the subject entity is a location.”

第二是position embedding操作。文章采用的position emebdding方式在多篇文章中也被用到，具体就不列举了。

分析上述思路，整体上是一个multi-classification任务，但是与常见的句子分类任务相比，比较特别的地方在于需要显式建模entity的表示，也就是output representation需要有conext+entity的信息。其中entity的表示需要好的position emebdding。这点基本上是最近实现的一些工作中得到的最关键的感受了。

沿着上述思路，就可以聊《Matching the Blanks_Distributional Similarity for Relation Learning》这篇文章了。看下图：

![img2](http://wx2.sinaimg.cn/mw690/aba7d18bgy1g47p0g5ln3j210n0drtas.jpg)

自己实现了基于pytorch的代码，稍后有机会开源，给出在semeval2010 task8和tacred上的具体评测结果，同时会有一些新的策略。

额，相关思路还有，不过工作相对较早，《Improving Relation Extraction by Pre-trained Language Representations》使用的是gpt。

![img3](http://wx2.sinaimg.cn/mw690/aba7d18bly1g4ilvkkau7j21aq0u045u.jpg)

这个需要提到的是，文章写道：“since our model processes the input left-to-right, we add the relation arguments to the beginning, to bias the attention mechanism towards their token representation while processing the sentence’s token sequence.”

那么，看了上述三篇文章需要预先给定entity，实际上我们更希望直接从句子中抽取关系而非预先给定entity，同时也是个人更加喜欢的一个思路。这里的一个代表是《Joint entity recognition and relation extraction as a multi-head selection problem》，看下图：

![img4](http://wx4.sinaimg.cn/mw690/aba7d18bly1g4j5odbhc8j212i0u0tj6.jpg)

从结构上看，比较暴力的方法应该要遇到outupt端的计算复杂度过高的问题。的确，在较大的数据集上跑官方代码的时候，非常慢。具体的，semeval 2010 task8上跑的时间可以接受，tacred上跑就慢的难以接受了，需要进一步优化。原始代码是基于tf实现的，这里给出一个朋友基于pytorch的[实现](https://github.com/WindChimeRan/pytorch_multi_head_selection_re)。

从建模体验上，类似的在实体识别中，acl2017的工作《Joint Extraction of Entities and Relations Based on a Novel Tagging Schem》，也是相同的。虽然暴力，但是通过简单的建模方式去解决问题，而且效果不差，的确是个人目前比较喜欢的方式（比起拍脑袋组合的奇怪的策略）。

类似地，在这个工作中，《Extracting Multiple-Relations in One-Pass with Pre-Trained Transformers》，架构如下：

![img5](http://wx2.sinaimg.cn/mw690/aba7d18bly1g4j6g5lw1fj20uy0n0td4.jpg)

具体可以看下论文，在苏剑林的[工作1](https://spaces.ac.cn/archives/6736)和[工作2](https://spaces.ac.cn/archives/6671)同时尝试了一个模型解决关系抽取的问题，也可以看到类似思想的使用，同样应该是一个很自然的想法。

### 反思

这篇博客总结了18年，特别是19年最近的一些关于实体识别和关系抽取的文章。从大方向上，可以考虑较强的backbone（bert），好的position embedding（变种非常多）。考虑任务之间的关系，一步或者两步解决。从context的长度，考虑单个句子或者多个句子。从entity和relation的个数考虑，要考虑多个entity和relation的建模。部分描述只给出了个人认为的关键部分，细节不清楚的可以具体读文章，此外，相关工作的实现难度上应该不算大。

参考文献：

1.[自然语言处理与信息抽取](https://mp.weixin.qq.com/s?__biz=MzIyODExNDgxOA==&mid=402669092&idx=1&sn=b91c2c413b74e27ecbbbd72109e064c4&chksm=75a276c942d5ffdf4f1f22fe4843ac4066d56df3388cdb4ccfdc32dd59e516d97b2fab06d7e8&mpshare=1&scene=23&srcid=0612H0vYaFGB77kJZOQ3PZ0K%23rd)












