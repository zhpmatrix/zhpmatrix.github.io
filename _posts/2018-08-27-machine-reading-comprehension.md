---
layout: post
title: "全国第一届“军事智能·机器阅读”挑战赛"
tags: [NLP]
excerpt: "放在草稿箱好久的一篇调研，本来是为比赛准备的，Pipeline跑通之后因为各种原因没有时间继续调试。梳理了比赛任务，相关比赛和数据集，经典模型等。"
date: 2018-08-27 10:20:00
mathjax: true
---

*作者按：本来想着全职做这个比赛，老大看过比赛之后，语重心长地说“来公司最好做一些业务型的项目。”，于是交给我一个更具挑战性的项目，中文文本错误检测和修正，凉。*

先放出比赛链接，[“莱斯杯”全国第一届“军事智能·机器阅读”挑战赛](http://47.96.153.138/index.html)，写这篇博客的目的主要是通过比赛来了解机器阅读理解的任务，技术和进展。这篇博客不会给阅读理解老司机带来任务价值，逃。

### 赛题分析

机器阅读类比赛需要关注两个方面的数据，分别是文档和问题。二者的关系是问题是从文档中来的，需要机器能够读懂文章，然后回答问题。比赛的文档包括新闻类，快讯类和情报类共三大类五万+篇文档。其中每篇文档对应五个问题以及人工标注的答案，共有二十五万问题答案对。

问题包括六类，具体为事实型问题，列表型问题，数值型问题，定义型问题，观点型问题和篇章型问题。

现对问题进行逐一分析。

- 事实型问题是有一个确定性实体级别的答案。

例如第X舰队指挥官是谁？

- 列表型问题是有多个确定性实体级别的答案。

例如X国舰载机机型？

- 数值型问题有可能需要统计运算的数值型答案。

例如最近一周，XX对XX油气田几次骚扰？

- 定义型问题需要用一句话或者多句话回答某个概念，术语，现象，任务的定义或者解释。

例如“XX一体战”的定义？

- 观点型问题的答案是发表的一句话或者多句话的言论或者观点。

例如XX对军事智能化的指示？

- 篇章型问题的答案需要对问题进行全方位的描述，答案包含问题目标的多个方面。

例如XX对南海的基本政策倾向？

从问题角度出发，和搜狗问答比赛对比，搜狗比赛只包含事实型问答和非事实型问题，而该比赛则涵盖的问题类型较广，这会增加比赛的难度。

因为比赛的数据集还有公布，暂且看一下DuReader的数据，如下。

```
{
  "question_id": 186358,
  "question_type": "YES_NO",
  "question": "上海迪士尼可以带吃的进去吗",
  "documents": [
    {
      'paragraphs': ["text paragraph 1", "text paragraph 2"]
    },
    ...
  ],
  "answers": [
    "完全密封的可以，其它不可以。",                                  // answer1
    "可以的，不限制的。只要不是易燃易爆的危险物品，一般都可以带进去的。",  //answer2
    "罐装婴儿食品、包装完好的果汁、水等饮料及包装完好的食物都可以带进乐园，但游客自己在家制作的食品是不能入园，因为自制食品有一定的安全隐患。"        // answer3
  ],
  "yesno_answers": [
    "Depends",                      // corresponding to answer 1
    "Yes",                          // corresponding to answer 2
    "Depends"                       // corresponding to asnwer 3
  ]
}

```

上述数据就是一个事实型问答，但是给出了问答的关系，包括Depends和Yes.


比赛指标为ROUGE-L和BLUE指标。


### 相关比赛和数据集

#### [2018机器阅读理解技术竞赛](http://mrc2018.cipsc.org.cn/cipsc)

比赛数据集是基于百度搜索引擎获取的数据，整理成DuReader公开数据集。评测指标为ROUGH-L和BLEU4，针对是非及实体类型问题，对ROUGE-L和BLEU4评价指标进行了微调， 适当增加了正确识别是非答案类型及匹配实体的得分奖励， 一定程度上弥补传统ROUGE-L和BLEU4指标对是非和实体类型问题评价不敏感的问题。

比赛给出了基于PaddlePaddle和Tensorflow的基准模型。第一名团队尝试很多的经典RC模型，包括bidaf，match-lstm, r-net, dcn等，最终模型是对bidaf的改进，尝试引入多个答案的信息。

[PaddlePaddle来做机器阅读理解（DuReader数据集)](https://www.kesci.com/apps/home/project/5b2ca2e3f110337467b2752c)

#### [WebQA](https://kexue.fm/archives/4338)

百度的中文问答数据集。

#### ASC2018世界超算-机器阅读理解

比赛数据集是基于微软Bing和Cortana收集的数据集，整理成MS MARCO数据集发布。

比赛给出了基于CNTK的基准模型。

#### SQuAD

由Standford发布的Standford Question Answering Dataset.


#### CoQA

[数据集地址](https://stanfordnlp.github.io/coqa/)，对话型问答挑战。


#### HotpotAQ

[数据集地址](https://hotpotqa.github.io/)，多跳问答，注重推理。


#### SemEval-2018

[比赛地址](https://competitions.codalab.org/competitions/17184#phases)


#### SemEval-2019

[比赛地址](https://competitions.codalab.org/competitions/20013#results)


#### 哈工大发布的阅读理解数据集

#### [第一届“讯飞杯”中文机器阅读理解评测（CMRC2017）](http://www.cips-cl.org/static/CCL2017/iflytek.html)

填空型阅读理解任务。

#### [CIPS-SOGOU问答比赛](http://task.www.sogou.com/cips-sogou_qa/)

分为事实类问答任务和非事实类问答任务。


#### [Fujitsu AI-NLP Challenge](https://openinnovationgateway.com/ai-nlp-challenge/)

冠军方案是：Cross-Attentive Convolutional Neural Network.

#### [TriviaQA](https://github.com/mandarjoshi90/triviaqa)


#### 经典模型

参考2中**梳理QA的经典模型**中用非常清晰明白的语言梳理了QA的发展历程，个人对CNN比较认可，所以选择了QANet作为比赛模型，模型结构如下：

![QANet](http://wx3.sinaimg.cn/mw690/aba7d18bgy1fuo1cft3bfj212z0w0438.jpg)

大部分相关任务结构从整体上类似，两个输入，中间聚合，一个或者多个输出(“魔镜杯”比赛问题相似度模型使用相同架构），所以需要关注的点就是模型细节。

_近期任务较多，跑通Pipeline后，就一直拖着没有去调试模型。允悲！_


#### 参考资料

1.[深度学习解决机器阅读理解任务的研究进展](https://zhuanlan.zhihu.com/p/22671467)

2.[梳理QA的经典模型](https://mp.weixin.qq.com/s?__biz=MzI3NTA0MzM1OQ==&mid=2651615623&idx=1&sn=03bed544ea8f932beffbaea76af6aa4c&chksm=f0f214f7c7859de112edd5d183590e916f098c48e7d05613995525226af989d81e6309b412c0&mpshare=1&scene=23&srcid=0803uL7l7PNzyIIaj8mqXGG8#rd)

3.《QANet: Combining Local Convolution With Global Self-Attention For Reading Comprehension》，Google

4.[question answering with tensorflow](https://www.oreilly.com/ideas/question-answering-with-tensorflow)

5.[NLP领域的阅读理解模型实际上是语义匹配还是词与词之间的匹配？](https://www.zhihu.com/question/389751777/answer/1178900681)

6.[样本构造中的偏置问题](https://zhpmatrix.github.io/2020/04/04/sample-bias/)














