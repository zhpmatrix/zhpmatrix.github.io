---
layout: post
title: "[工作总结]我在医疗NLP方向的工作总结"
excerpt: "大概两年半的时间过去了，我以及团队到底贡献了什么价值？"
date: 2023-08-11 11:40:00
---

#### 产品&技术

围绕产品&技术这个话题，一张算法架构图基本可以表达我们在过去很长一段时间做的工作，具体如下图：

算法架构图|
:-------------------------:|:-------------------------:
![PIC_01](https://github.com/zhpmatrix/zhpmatrix.github.io/raw/master/images/算法能力架构图4.0.drawio.png){:height="400px" width="700px"}  |



整体上分为行业相关和行业无关，这是公司主体朝着集团化发展必然的选择。在具体划分上，我们认为内容和数据通常是行业相关的，能力是行业无关的。这套能力体系首先要能够服务于医疗行业，因此在基础数据层，强调了医疗属性。数据设施层通过中间件完成数据的离线和在线计算。基础算法层和应用算法层是行业无关的，通过基础算法层的原子能力组合形成应用算法层。为了支撑能力构建，需要搭建一套算法工程体系，这里包括标注平台，Pipeline平台，算法服务平台等，以及配套的爬虫框架，能力评估中心和配置中心等。

基于这套底层能力和工程基建，可以构建行业算法层。面向医疗行业的核心能力包括三个方面，分别是医疗数据挖掘，结构化和医疗知识图谱。结构化的能力能够支持医疗数据挖掘，同时用于知识图谱的构建。知识图谱通过内容提供，用于结构化的知识增强。其中的最核心的内容是结构化，具体能力包括段落解析，医疗实体识别，医疗关系抽取，术语标准化能力等。对于通用结构化能力的认识演化如下：

通用结构化的认识演化|
:-------------------------:|:-------------------------:
![PIC_02](https://github.com/zhpmatrix/zhpmatrix.github.io/raw/master/images/通用结构化的理解.drawio.png){:height="400px" width="700px"}  |



基于上述认识，我们落地了具体的方案，分为段落结构化和段落内结构化。

段落结构化能力的主要目的是将一个HTML的病历文书按照特定段落划分。以入院记录为例，需要结构化为主诉，既往史，现病史，家族式，疾病史等。技术需求看似简单，需要支持的实际院内的业务则非常广泛，如科研检索产品，患者360产品，数据上报业务，互联互通业务等。具体方案如下：

![段落结构化](https://github.com/zhpmatrix/zhpmatrix.github.io/raw/master/images/段落结构化.png)

实际上，基于上述方案开发了一套病历结构化产品，能够使得研发和交付分离，显著提升了研发效能，释放了算法的资源投入。


段落内的结构化，具有如下特点：

+ 支持54种实体，12种关系，9种通用属性，78种特殊属性的识别和抽取
 基于深度学习的信息抽取模型设计，采用端到端的方式，在减少对医学知识
 通过模型蒸馏，模型压缩等工程化服务部署方式，在显著降低在线服务资源

方案的具体架构如下图所示：

![结构化的具体实现](https://github.com/zhpmatrix/zhpmatrix.github.io/raw/master/images/结构化的具体实现.png)

当然，我们也需要从能力视角切换到内容视角（业务角度），从关心怎么抽到关心抽什么。

![通用结构化的多维视角](https://github.com/zhpmatrix/zhpmatrix.github.io/raw/master/images/通用结构化的多维视角.drawio.png)

结构化的能力构建除了实体，属性和关系的抽取，还有术语标准化的能力。主要功能如下：

+ 通过术语标准化能力建设，显著提升人工主数据校对的效率
 实现临床医疗文本数据到医疗知识图谱的映射，建立知识的关联，赋能上层医疗具体应用

|类别|标准词规模|来源|
|------|------|------|
|手术|12855|ICD9|
|药品|200000|国家药监局|
|诊断|34975|ICD10|
|检查|3499|知识图谱|
|检验|163|知识图谱|

围绕术语标准化的离线和在线能力构建如下：

![标准化能力-离线](https://github.com/zhpmatrix/zhpmatrix.github.io/raw/master/images/标准化能力-离线.png)

![标准化能力-在线](https://github.com/zhpmatrix/zhpmatrix.github.io/raw/master/images/标准化能力-在线.png)

通过整合上述能力，在算法演示平台的呈现效果如下所示：

![算法演示平台](https://github.com/zhpmatrix/zhpmatrix.github.io/raw/master/images/算法演示平台.png)

基于上述这套算法体系，可以构建业务应用层。具体如下:

专病库。这里的主要工作是构建一套专病库研发框架。通过低代码的方式，将算法能力赋能医学团队，实现专病库的取数逻辑，计算逻辑可以通过配置化的途径实现快速开发。每100个非结构化字段，明确入组条件和获取规则后，预计完成时间从8周降低至4周，研发效率提升1倍。基于该框架完成了消化道出血和结直肠癌专病库的研发，验证了有效性。
患者360和科研检索。作为院内标准产品的一部分，主要依托结构化能力来支撑。

智能分诊。包括意图识别，科室分类，智能追问等功能，提升交互体验，落地多家医院。

病历质控。通过融合基础算法信息抽取能力和医疗知识图谱，实现针对病历的内涵质控，提升病历书写质量。

临床决策。通过和头部三甲医院合作的方式，构建针对胸痛，脓毒症和发热待查的预测模型。


#### 医疗大模型

医疗大模型的整体推进阶段，分为司内和司外。司内主推模型和应用两条线，司外和知名三甲医院结合具体场景共创。整体架构如下:

![cmllm-架构](https://github.com/zhpmatrix/zhpmatrix.github.io/raw/master/images/cmllm-架构.png)



#### 组织&团队

#### 我的想法