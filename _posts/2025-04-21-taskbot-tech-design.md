---
layout: post
title: "财税咨询系统的架构思考"
tags: [对话系统]
excerpt: "Lepton AI的一个启发是通过对单点能力的良性组合实现系统价值的最大化。"
mathjax: true
date: 2025-04-21 12:00:00
---

#### 咨询系统的设想

在得物技术最近的一篇[文章](https://mp.weixin.qq.com/s/2Og361FIQ7WcknBIYFskQw)中谈到对于AI的预期描述，如下：

**告诉AI我们想要的目标或者任务，AI能够理解深度理解并分析我们的意图、自动的进行任务的拆解、自动的寻找可以使用的工具、自动的进行结果数据的汇总过滤、自动的呈现符合任务的展示形式。同时在任务处理过程中，可以自己完成异常的检测和修改。**

拆解之后要满足的特征如下：

+ 能够接受指令，具有较好的指令遵循能力，听得懂人话（浅层理解）
+ 能够理解指令的含义。如内含的梗，意图，背景知识等（深层理解）
+ 自动做计划+找工具+结果汇总（人类完成任务的方式未必可迁移至机器）
+ 纠错能力（是否需要自己完成持保留意见，但是系统要具备容错能力）

站在人类的角度，基本是符合预期的一个AI系统。在上一波NLP创业热潮中，虽然做了很多以对话为中心的ChatBot系统，但是进到LLM时代重新审视各类对话系统，以交付为中心的multi-agent承载了更多的期待，比如Manus等产品。


#### 从NLU到NLG的演化进程

首先看上一波客服系统的设计方案，如下：

<img src="https://github.com/zhpmatrix/zhpmatrix.github.io/blob/master/images/%E6%99%BA%E5%BA%93%E9%A1%B9%E7%9B%AE-%E4%BC%A0%E7%BB%9F%E5%AF%B9%E8%AF%9D%E7%B3%BB%E7%BB%9F%E8%AE%BE%E8%AE%A1.drawio.png?raw=true" width="400" align="center"/>


实际的系统设计可能单独一个多分类也能够解决问题，或者仅仅是采用向量匹配。不管怎样，电商智能客服的模式验证使得FAQ的技术路线深入人心，但是迁移到其他领域时可能会遇到新的问题。本质上，相比电商业务，医疗和财税方向的业务复杂度足够高。在做财税咨询系统的时候，正值RAG技术深入人心，同时DeepSeek V3爆火。

但是传统的对话架构和RAG架构的区别和联系是什么？一个基本的想法如下：

<img src="https://github.com/zhpmatrix/zhpmatrix.github.io/blob/master/images/LLM+%E9%97%AE%E7%AD%94%E7%B3%BB%E7%BB%9F.drawio.png?raw=true" width="400" align="center"/>

但是正如软件世界的“没有银弹”，存在诸多的问题是朴素RAG无法有效解决的，比如预测类需求，多跳查询类，统计类，逻辑推理类等。

不同的目标会采用不同的技术架构设计，可以分为答案可用率要求高的目标和答案可用率要求不高的目标。前者的定位是高质量咨询服务，核心在于提质，具体要求包括可用+好用+轮次少。本着确定性高和可解释性强的设计原则会形成若干基本做法，包括如下：

##### 答案生成时，避免使用模型内部的知识

在近期的一篇论文中提到，模型知道的知识，和模型能够表达出来的知识有40%的差距。对于一个知识驱动的系统，如果过分依赖模型内部的知识，那将是一个灾难。因为不知道模型内部知道什么以及不知道什么？如果对于知识的边界是不清晰的，那么知识的更新和维护就无从谈起。与此同时，甚至无法清晰描述自己维护的知识的边界是什么？比如知识的覆盖率是可接受的吗？

围绕知识构建，是可以单开一篇文章讨论的主题。可以阅读参考中给出的一些近期的文章，包含知识平台构建，医疗知识等。

比如在一个经典的咨询场景中，知识分为显性知识和隐性知识，其中**显性知识是指明确记录在文档或知识库中的知识，而隐性知识则是个人在日常工作中积累的经验和直觉。**

通过建立一个数字化系统，才能实现隐性知识的显性化，继而实现个人知识的组织化沉淀。经典RAG系统将知识显性化为非结构化文档，模型方案将知识隐性化为参数。理想的一个咨询系统是通过数字化的方式既能实现咨询效率的提升，同时能够实现个体知识的组织化积累并能二次利用，也即知识资产。

##### 按照问题空间分解

构建财税咨询系统，既需要站在知识角度，基于演绎法自顶向下的设计，同时需要站在数据角度，基于归纳法自底向上的设计。其中一个是答案视角，另外一个是问题视角。咨询的目标也正是实现问题和答案的匹配。如果无法清晰地划分问题空间，那么对于系统的边界就会存在认识不清的问题，而这对于一个高准确和可解释的系统而言是无法接受的。同时这种分解也有助于系统的持续可演进。

从答案角度理解咨询系统，可以见笔者2020年的文章[对话系统的思考](https://zhpmatrix.github.io/2020/08/02/think-in-dialogue-system/)。


##### 系统设计要求头重脚轻，重理解轻生成

在一个垂直领域，截止写这篇文章时，LLM的应用仍然存在不少问题，包括幻觉和不可控等，因此系统的设计希望在生成环节降低对LLM的依赖。这意味着系统的设计需要把LLM的能力分解并前移，这样才能降低对答案生成侧的压力。具体而言，加强系统对于会话的理解程度，对于答案生成环节则采用尽可能轻量可控的方式完成。

因此，整体的系统设计偏向于一个任务型机器人，但是弱化了对话路径的设计。回到财税咨询系统，本质上是强规则导向。作为知识表达的一种方式，规则可以通过二维表的方式来表示，其中单条规则的表示方式为要素+目标。站在知识表达的视角，系统的设计分为两个阶段，分别是规则召回和答案生成。规则召回解决的问题是从规则库中找到对应的规则，答案生成是基于召回的规则，形成一个答案。这里采用形成作为描述词，是因为输出答案的方式可以是：

+ 直接配置(类似FAQ系统中的QA对)
+ 追问(基于某种启发式规则)
+ 话术模版
+ 大模型生成(类似RAG的逻辑)

为了更好地召回规则，一方面需要更好地知识表达方式，另一方面需要对访客咨询的问题有深刻的理解，也就是需要强大的QU模块，包括问题提取，意图提取，要素提取，目标和目标值提取，问题风格等，本着能提尽提的目标，实现对访客咨询的深度理解。作为一个pipeline的系统架构模式，问题部分获取的信息越多，作为下游的答案生成环节的挑战会越低。


#### RAG

基于后者的定位，可以设计一个基于RAG的方案，相关案例参考笔者之前的工作，如[AI搜税](https://zhpmatrix.github.io/2024/09/07/ai-tax-search/)和[搜医搜](https://zhpmatrix.github.io/2024/10/12/souyisou/)。假设已经有一个相当规模的问答库，在采用RAG架构进行系统构建时，要注意考虑系统各个组件的存在必要性，比如真的需要rerank吗？真的需要混搜吗？


#### workflow v.s. agent

围绕agent，其实目前尚没有形成共识。似乎分别以openai，anthropic和langchain团队为代表，openai认为是自动化的流程编排，anthropic认为自不自动都可以，langchain认为是需要手动的，但是观点又非严格对立。

<img src="https://github.com/zhpmatrix/zhpmatrix.github.io/blob/master/images/workflow-agents.jpg?raw=true" width="400" align="center"/>

如上图所示，workflow的可观测性更强，agent的"agency"能力更强。在系统设计时，也代表着技术方案的选型。比如，笔者至今保留着对于通过模型微调实现更好的财税咨询对话体验的预期，但是同时认为短期内奔着落地上线的目标，手动编排几乎是唯一的选择，这是目前来看可观测，可解释，可追溯，可快速修复，可控的手段。

#### 相关参考

[1688AI助手“源宝”的产品演变之路](https://mp.weixin.qq.com/s/B9b-mmYc7ejH0rN5R09mJg)

[AI+智能客服:大模型可落地的最成熟场景之一](https://mp.weixin.qq.com/s/TN_UVBplxDFONIkfp9v57Q)

[智能对话新纪元:百万日活对话机器人的LLM落地实践](https://www.nxrte.com/jishu/41984.html)

[蚂蚁金服客服服务及权益保障事业部总监/智能客服业务负责人-丁翌专访](https://mp.weixin.qq.com/s/zjo-oUnVQyi3lZYQgexVcw)

[批量回答质量的自动化评测](https://mp.weixin.qq.com/s?__biz=MzkxNzE5MjE2NQ==&mid=2247483973&idx=1&sn=280e98633f006d7d81f07a353b377e99&chksm=c090a1cb84ce772710b6434fe7bb7230eade79a66e15771dd8077e2f174447be9b7153718835&mpshare=1&scene=1&srcid=0313MV2r4kJIdKxnZB8rlqgZ&sharer_shareinfo=58199471c63f74c1e572a41e2664494d&sharer_shareinfo_first=b1085fa6f8a5f9f6edf9a382e8818c4c&version=4.1.31.99548&platform=mac#rd)

[《Converse Task-Oriented Dialogue System Simplifies Chatbot Building, Handles Complex Tasks》](https://www.salesforce.com/blog/converse-task-oriented-dialogue-system/)

[《Task-Oriented Dialogue with In-Context Learning》](https://arxiv.org/pdf/2402.12234),RASA的工作

[蔚来汽车知识平台的构建](https://mp.weixin.qq.com/s/Q6Beo_Q9mR2TTZe1BPQaLg)

[大模型和知识图谱双轮驱动的汽车制造业知识服务](https://mp.weixin.qq.com/s/4ZmGOEMJEYKcB2P_xjfjhA)

[图驱动的知识管理：观察与思考](https://mp.weixin.qq.com/s/hU6SFbHrx6ssVRwEN21LtQ)

[融合知识图谱与大模型的中医临床辅助决策体系](https://mp.weixin.qq.com/s/s2Oi3y89TjBlXVyG_8U52w)

[大模型+知识管理发展趋势及标准化工作介绍](https://mp.weixin.qq.com/s/Inv7jSdSbeEq4KcPvV4jEQ)

**[扫码加笔者好友](https://zhpmatrix.github.io/about/)，茶已备好，等你来聊~**