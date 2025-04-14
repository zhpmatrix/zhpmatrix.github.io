---
layout: post
title: "聊一聊，预处理和数据增强技术"
tags: [NLP]
excerpt: "这篇博客梳理了NLP中英文的预处理方法和一些通用但是实现成本不高的数据增强思路。"
date: 2019-03-08 18:43:00
mathjax: true
---

<script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=default"></script>

在[基于margin-loss的句子相似度](https://github.com/zhpmatrix/margin-loss-for-sentence-similarity)这个项目中，为了验证想法，找不到开放数据集，因此自己从新浪爱问爬取了数据。自己爬的数据和学界开放的数据对比，数据显得非常脏。这里有三个含义：第一：数据不规范，比如用词，写作等；第二：中文文本中蕴含了特殊符号等；第三：数据偏见在真实场景下是确实存在的。这里是从数据质量的角度来看，结合具体的场景，可能会有各种影响数据质量的因素。因此，我们需要数据预处理，目的是提升数据质量；

此外，数据规模也是重要的。我们需要数据增强技术来提升数据规模。这是数据增强技术的表面结果，从深层次的角度来看，数据增强技术可以有效防止模型的过拟合，提升模型的鲁棒性。所谓"见多识广"。

因此，为了提升数据质量和数据规模，我们需要预处理技术和数据增强技术。

### 一.预处理技术

#### 1.中文

#### (1)分词

中文分词通常是基于词的中文NLP场景下的第一步，虽然目前的中文分词社区仍然对于一些中文语句的分词结果不理想，但是整体上是可用的。自己常用的分词工具是哈工大的LTP。

#### (2)停用词过滤

停用词是高频，但是无意义的词。在中英文环境中都存在停用词，但是停用词是否要去掉是一个有争议的问题。从理论上分析，去掉停用词，有助于减少VOC的大小，加快收敛，节省存储和计算时间；减少停用词对句子语义表示的影响，有助于提升模型效果。但是实际上，预估停用词对任务的影响是困难的。因此实际场景下，可以做两个版本分别对比。

#### (3)特殊符号清洗

标点符号和词都是符号，但是还要一类特殊符号，诸如笑脸，数字，运算符号等，在一些场景下，需要注意这类特殊符号的过滤。如果这类符号是低频的，那么通过停用词过滤，可以去掉一部分符号，但是如果不能过滤掉，需要显式地去过滤该类符号。在上文提到的项目中，就会遇到这种表情符号特别丰富的场景。

#### (4)任务依赖的预处理

在分类任务中，可以通过NER技术将待分类文本中出现的地点，组织和人名替换为\<place\>，\<org\>和\<person\>，减少OOV的可能，优点同上。比如，可以应用在[AI Challenger 2018的细粒度情感分类比赛](https://github.com/xueyouluo/fsauor2018)中。


#### 2.英文

#### (1)分词

英文句子以空格作为分割符，分割单词。但是直接通过空格分隔符会导致下述情况下的分词结果的不正确性。比如：

**You're the apple of my eye!**

分词后，**eye!**和**eye**就表示不同的单词了。直观上来看，似有不合理之处。因此，显然，要去掉符号。

#### (2)标点符号过滤

在(1)中，去掉标点符号之后，得到，

**You re the apple of my eye**

这样的话，又会遇到**it's**和**its**的冲突。

因此，好的英文分词要考虑上述两种情况，NLTK对于

**it's my dog!**

的分词结果是：

**\[\[it\] \['s\] \[my\] \[dog\] \[!\]\]**

这正是我们需要的。

#### (3)大小写统一

在英文场景下需要考虑，有些特殊场景下不适合进行大小写的统一。比如，BERT的预训练模型就提供了两个版本的，分别是统一后和不做统一的。

#### (4)标准化(stemming&lemmatization)

这个是英文场景所特有的，举例如下：

第一种情况：比如对名词eye，有eye和eyes两种形态；

第二种情况：比如对动词take，有token, taken, take三种形态。

通过stemming(词干分析)解决第一种；通过lemmatization(词元分析)解决第二种；

如果说分词可以认为是中文所特有的（不严格成立，英文也可以分词，但是英文分词的必要性显然不如中文分词），那么标准化就是英文所特有的。

#### (5)subword

为了进一步减少VOC的大小，在机器翻译任务中比较流行的subword技术。比如两个单词，分别是person和possion,则subword可以表示为\[\[pers\],\[on\],\[possi\]\]，具体由[语料和BPE算法](https://github.com/rsennrich/subword-nmt)决定。

### 二.数据增强

#### 1.简单数据增强

#### (1)同义词替换

同义词的获取可以基于词向量获取其他技术构建的词的量化表示，通过距离计算相似度得到。

#### (2)同义词随机插入

将句子中选定的词的同义词随机插入句子任何位置，插入之后，句子变长。

#### (3)随机交换词汇位置

交换后，句子长度不变。

#### (4)随机删除

#### 2.任务依赖的增强技术

#### (1)back-translation

反向翻译用于机器翻译，用于[中文文本纠错任务](https://liweinlp.com/?p=5000)。

#### 3.复杂技术

#### (1)使用预测语言模型做同义词替换

#### (2)作为平滑技术的数据加噪

#### (3)基于生成模型(VAE&GAN&Flow)进行数据生成

总结：虽然梳理了一些预处理和数据增强的技术，但是实际任务中的技术选取还是要以下游任务的提升为基准点。2018年有一篇文章做CV领域的自动数据增强技术的，基于强化学习。NLP领域或许也可以做一做呀。从工具使用上，在预处理阶段，综合体验NLTK和哈工大的LTP结合使用最棒。可能与自己不载入一个模型就会感觉不舒服有关吧。本来写这篇博客的目的是想写一个预处理和数据增强的模块的，但是现在感觉意义不是很大。

主要参考：

1.《EDA: Easy Data Augmentation Techniques for Boosting Performance on Text Classification Tasks》

2.[中文对比英文自然语言处理NLP的区别综述](https://zhuanlan.zhihu.com/p/59838270)

3.[《Low Resource Text Classification with ULMFit and Backtranslation》](https://arxiv.org/abs/1903.09244)

在情感分类任务上，比较了两种数据增强技术，分别是Random Token Perturbations和Backtranslation，证明了Backtranslation的有效性。

4.[《Learning to Ask Unanswerable Questions for Machine Reading Comprehension》](https://arxiv.org/pdf/1906.06045.pdf)

SQuAD2.0生成不相关的问题。该问题与文章相关，但是在文章中找不到答案。因为SQuAD2.0添加了一类新的问题，该问题的是“no answer”的。

5.[《Data Noising as Smoothing in Neural Network Language Models》](https://arxiv.org/abs/1703.02573)

6.[相对全面的总结](https://zhuanlan.zhihu.com/p/75207641)

7.[思考为什么要做预处理，预处理做到什么程度的文章，非常棒。](https://zhuanlan.zhihu.com/p/76957566?utm_source=qq&utm_medium=social&utm_oi=52727124066304)

8.[去除停用词对情感分类的影响](https://towardsdatascience.com/why-you-should-avoid-removing-stopwords-aa7a353d2a52)

如非必要，不要做过多的数据预处理。因为无论是对于任务本身，还是对于后续的生产部署，都是坑。

9.[NLP中的数据增强总结，包括多个NLP的具体任务](https://github.com/quincyliang/nlp-data-augmentation)

10.《Data Augmentation using Pre-trained Transformer Models》

文章比较了基于自编码(BERT)，预训练语言模型(GPT-2)，和预训练seq2seq(BART/T5)的三种模型用于数据增强的效果。具体的，比如对于一个情感分类任务，三种方式都可以做，哪种好一些？文章的结论是：考虑到标签保持的能力和多样性，seq2seq整体上较好。 在具体数据增强的方法上，文章也有一些阐述。整体上文章解决的问题实用性较强，既可以作为一篇Review，也可以作为一篇技术报告来看。此外，文中的一些方法虽然是放在数据增强的角度来考察的，但是理论上应该也可以推广到其他Task上，例如情感迁移等。

11.[SCIR-深度学习领域的数据增强](https://mp.weixin.qq.com/s?__biz=MzI4MDYzNzg4Mw==&mid=2247492349&idx=5&sn=c4c7180ea455310ff1b6539fa7168599&chksm=ebb7da29dcc0533fe6bb348788b66246395110c2c1a606e41edfc7b37a5b66643d6736eed487&scene=0&xtrack=1&key=615298b6af513962a2ccd0616eac026eddcbf12936b0b0ef1ee1609eef767b638d63c184ace6204ea701057c1c49124510e951b47ce95f72e2d6d1355b0475c05a1e0109af3c4bbf8de8a219cb70a8e6&ascene=0&uin=MTg2NTIxNzUxNw%3D%3D&devicetype=iMac+MacBookAir7%2C2+OSX+OSX+10.15.2+build(19C57)&version=11020201&lang=zh_CN&exportkey=AyGPkP9lEsk1LxHnwqlXLfU%3D&pass_ticket=L5m3u%2FRnPtgczNrYDLg8yofoGvrUzX%2B1RWX2pbEdauEOQpSI1cCTiC71mkYWrSX%2B)

12.[A Visual Survey of Data Augmentation in NLP](https://amitness.com/2020/05/data-augmentation-for-nlp/)

总结的非常全面的NLP中的数据增强方法。

13.[Why is data augmentation classified as a type of regularization?](https://stats.stackexchange.com/questions/295383/why-is-data-augmentation-classified-as-a-type-of-regularization)

数据增强作为一种正则化的观点。

14.[A Visual Survey of Data Augmentation in NLP](https://amitness.com/2020/05/data-augmentation-for-nlp/)