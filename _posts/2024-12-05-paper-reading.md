---
layout: post
comments: true
title:  "[论文笔记]《Exploring the Impact of Table-to-Text Methods on Augmenting LLM-based Question Answering with Domain Hybrid Data》"
excerpt: "问答系统中，无论采用模型微调的方式，还是RAG的方式，将表格转化为markdown总没有错。"
date:   2024-12-05 10:35:00
mathjax: true
---

#### 基本信息

主题：	表格问答/大模型微调/RAG

作者:	东南大学，曼彻斯特大学，华为

会议：	NAACL2024

#### Motivation

表格-文本生成技术已经在NLP领域被广泛研究，围绕大模型增强的问答系统，融合文本和半结构化的表格数据是一个趋势，但是不同的表格-文本生成技术是如何影响QA系统的，并没有相对系统的对比分析。通过对不同的表格-文本生成技术的实验对比和理论分析，可以形成一些有价值的技术选型建议。

#### 主要贡献

+ 通过实验证明，不同的表格-文本生成技术会显著的影响问答系统的效果。其中，人类评估的RSD（Relative Score Difference）的范围从2.8%到9.0%，GPT-4的评估范围从4.8%到16%

+ 对于领域微调范式，基于LLM和传统预训练语言模型的方法在各种模型设定下，显著优于其他方法。在RAG范式下，虽然基于LLM的方法依然表现优秀，但是基于markdown的方法也表现出超出预期的有效

+ 不同方法产生的领域术语和动词的频率的不同，以及在文本切片的语义表征中的质量不同，是不同方法在两类系统存在效果差异的首要因素


#### 主要过程

##### QA系统的两种实现方法

+ 基于领域模型微调的QA系统

<img src="https://github.com/zhpmatrix/zhpmatrix.github.io/blob/master/images/12051.png?raw=true" width="400" align="center"/>

+ 基于RAG的QA系统

<img src="https://github.com/zhpmatrix/zhpmatrix.github.io/blob/master/images/12052.png?raw=true" width="400" align="center"/>


##### 四种表格-文本生成技术

**Markdown**

直接将表格表示为markdown格式，不需要模型训练，可以利用脚本在无需人工参与的条件下快速完成转换

**Template**

使用一系列提前设计好的适配表格特征的模版做表格的文本化。比采用markdown的方式能够实现更好的多样性，但是需要人工提前设计多种模版。

**TPLM-based**

利用传统的预训练语言模型，比如T5和BART等，通过在跨领域的表格-文本生成数据集做微调。这种方法能够提供更高的灵活性和领域适配性，但是也要求更多的计算资源。

**LLM-based**

GPT-*系列模型的效果多数情况下优于表现最好的微调的模型，和TPLM-based方法相比，这种方法能够通过in-context learning实现自定义的裁剪，但是同时也存在领域数据泄漏的风险。


##### 实验分析

###### 数据集

ICT-DATA：170个信息与通信技术领域的英文技术文档，每个文档都是由文本和表格组成，其中表格数据约占总数据的18%。

ICTQA：从QA平台收集9000个答案较长的关于ICT产品的问答对，其中答案均是由专家根据产品文档书写的。选择500个问题做测试集，对应的答案需要同时从表格和文本中提取，剩下的问答对用于领域模型微调。

###### 评估指标

自动评估指标：利用GPT-4作为评估器，基于生成的答案和参考答案的相似性打分，分值范围为[0-5]，其中0表示生成的答案如"I don't know the answer."，1代表最小的相似度，5代表完全准确的生成答案。

人工评估指标：评分准则同上，利用三个领域专家进行打分。


###### 实验设置

用于领域微调的基座模型为Meta's OPT(1.3B-13B)和Llama-2-base（7B,13B），采用QLora用于持续预训练和指令微调。RAG系统使用的生成模型为Llama2-chat（7B，13B和70B）以及GPT-3.5-turbo。采用文本切片切分语料，每个切片长度不高于3000个char，采用BGE向量模型做表征，利用FAISS存储向量。每个问题检索出最相似的3个切片，基于LangChain实现整体流程。


###### 实验结果


<img src="https://github.com/zhpmatrix/zhpmatrix.github.io/blob/master/images/12053.png?raw=true" width="400" align="center"/>

其中，加粗表示最佳结果，下划线表示次佳结果。基于领域模型微调的方法中，无论是基于人类的评估结果还是GPT-4的评估结果，LLM-based的方法在绝大多数设定下取得最优结果。而在RAG系统中，两种评估方法中，均存在基于Markdown的表示方法取得最优结果的设定。其中RSD(Relative Score Difference)=(Highest Score - Lowest Score)/5。


**领域微调系统中，为什么TPLM-based的方法和LLM-based的方法分别取得次优和最优结果？**

<img src="https://github.com/zhpmatrix/zhpmatrix.github.io/blob/master/images/12054.png?raw=true" width="400" align="center"/>

上表给出了不同方法生成的语料中，领域术语和动词频率分布情况。可以看出LLM-based的方法能够得到的领域术语和动词最多，其次是TPLM-based的方法。


**RAG系统中，为什么Markdown的方法和LLM-based的方法分别取得次优和最优结果？**

<img src="https://github.com/zhpmatrix/zhpmatrix.github.io/blob/master/images/12055.png?raw=true" width="400" align="center"/>

采用t-SNE方法做了切片向量的聚类可视化，对于给定Query会发现LLM-based的方法和Markdown-based的方法得到的切片，在语义空间中距离Query相比其他更加地接近。

#### 思考&应用

（1）在做表格-文本生成的时候，无论是否利用模型微调，基于大模型的方法多数情况下是最佳实践。但是RAG系统中，也可以考虑采用Markdown的方法

（2）基于表格的问答应用中，将表格（600*25）格按照行转换为json格式（字段名称采用中文表示），检索效果也不错



**[扫码加笔者好友](https://zhpmatrix.github.io/about/)，茶已备好，等你来聊~**
