---
layout: post
title: "会话标准化之最后一句话抽取"
tags: [对话系统]
excerpt: "最后一句话是会话标准化的一种具体实现方式"
mathjax: true
date: 2025-06-23 12:00:00
---

#### 前言

最后一句话抽取作为财税对话系统的第一站，给孩子苦的，承载了太多太多...

#### 欢迎来到真实财税咨询对话场景

在真实财税咨询对话场景下，某一个时刻可能会存在多个未被回答的问题，类似如下的对话:

```
访客:哪些农产品可以用于抵扣？ 问题(1)
坐席:XXX 答案（1）
访客:哪些算农产品 问题（2）
访客:农副产品能用于抵扣吗？ 问题（3）
```
其中，问题（1）是已经被坐席回答过的问题，问题（2）和问题（3）是尚未被坐席回答过的问题。这种条件下，希望能够通过最后一句话任务找到要回答的问题。由于对话是以流式存在的，因此本质上需要找到的是最后一个未被解答完的问题，比如这里的问题（3）。这里有两层含义：

（1）只关注最后一个问题，而不关注所有问题
（2）未被解答完的问题是指：针对访客的具体某个问题，对话过程中坐席回答过了，基于回答的内容访客又提出的新问题（如用户又补充了一个新要素）。这是一个非常狭隘的表述，实际情况中包括如下：

+ 问题和问题之间确实是不相关的
+ 问题和问题之间存在递进关系
+ 问题和问题之间存在包含关系
+ 最后一个问题并非真实意图

评估最后一句话抽取的效果的标准是根据最后一句话写出来的答案与根据完整会话写出来的答案是一致的。具体要求包括完备的背景信息，流畅的问题表达，和原始会话内容在语义上的一致等，这是一个在业务上make sense的评估手段，但是不够具体到能够被算法直接应用。如果要求背景信息是完备的，则需要在对话上下文中能够找到与最后一句话相关的信息。但是实际对话中存在各种复杂的问题，如下：

+ 访客中的信息有些是确定的，有些是不确定的，而是自己推理出来的
+ 怎样判断相关？
+ 访客提供的信息是冲突的

在构建测试集的时候，要刻意去掉有歧义的最后一句话和访客根据坐席回复进行追问确认的内容，比如访客确认意图，访客确认答案以及访客对于专业知识不懂的时候的反问等。

#### 可能的解决方案

最后一句话实际在建模的时候是一个文本生成问题或者类似文本摘要任务，可以采用直接评估的方式，也可以采用间接评估的方式，如下：

+ 直接评估：需要人工参与的最后一句话的可用率评估
+ 间接评估：下游任务（要素抽取）的准确率评估。这里主要是因为最后一句话的下游只服务于要素抽取，同时要素抽取还是一个客观题目，可以实现自动化地量化评估

既然对话是流式的，站在某个具体的轮次来看，可以顺流而下，也可以逆流而上，分别对应自顶向下的方案和自底向上的方案。其中自顶向下的方案可以结合memory机制的应用，典型的论文如《Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory》中讲述的两种方法，但是在具体实现的时候可以采用提示词等更轻量的方式等。

##### 站在当前看当前

财税咨询对话系统和医疗问诊系统类似，在系统的各个阶段均存在对领域知识的强依赖，对于最后一句话抽取任务而言同样如此。在上文中提到的“信息”的概念，在最后一句话任务中的具象化表达就是财税领域的要素。因此，通过将要素名称和要素值域等信息注入到实现方案中，有助于提升最后一句话抽取的效果。

增加校验机制。一种典型的实现方式是分为两个阶段，第一个阶段直接总结访客最后一个问题，第二个阶段通过某种策略修正第一个阶段总结的最后一个问题。

场景适配。经过量化结果和面向case的分析，会显著发现对话轮次较少的时候，总结的最后一个问题的质量非常高，这意味着至少可以有两个策略：
（1）目前的方案直接用于对话轮次<=3的场景
（2）目前的方案在对话轮次>N的场景中，只回答<=N时的访客问题（其中N是一个较小的数值）

##### 站在全链路看当前

最后一句话任务的下游是要素抽取任务，一种简单的实现方式是每个任务单独一个提示词来实现，这样的实现方式存在理论上的噪音传递问题。因此，通过直接合并两个提示词为一个提示词，也许能够减少噪音传递的问题。但是如果只是简单的合并提示词，则建模本质没有发生改变。考虑到降低优化的难度，此时分开应该是一种更好的解决问题的方式。

怎样理解“鸡生蛋，蛋生鸡”的问题？最后一句话的目的是要素抽取，但是最后一句话的要求是要素完备。这样的话，是否意味着如果能把最后一句话做好，要素抽取就顺道做了，或者没有做的必要了。其实不然，最后一句话虽然也关心要素，但是可以认为是要素之间的“弱连接”，关心的是“要素召回”，这个过程中允许有误报。但是要素抽取则直面要素本身，更关注的是“强连接”，关心的是“要素精确”。虽然二者都关注要素，只是关注程度上的不同，并非任务上构成了一个循环依赖。

#### 总结

针对访客和坐席的模糊对话，最后一句话任务通过压缩的方式实现了对话标准化。
模糊是指对话中访客自身表达的歧义性以及访客和坐席对话的全双工特性带来的语义模糊。
压缩是指找到有用的信息，同时排除无用的信息（纳排逻辑）。这里的三个子问题如下：
（1）信息是什么？
（2）怎么判断有用还是无用？
（3）如何做到“找到有用”和“排除无用”？
标准化有两个具体含义：
（1）输入内容的标准化。将对话统一转化为问题。为了实现内容的标准化，需要识别问题有哪些？问题是否已经被坐席解答？未被解答完的最后一个问题是什么？过程中需要解决对话中的指代，错别字，否定关系，引用等问题
（2）输入长度的标准化。任何长度的对话都可以通过最后一句话任务压缩成一个较短的问题，使得下游对于会话输入长度无感，显著降低LLM的理解难度

**[扫码加笔者好友](https://zhpmatrix.github.io/about/)，茶已备好，等你来聊~**