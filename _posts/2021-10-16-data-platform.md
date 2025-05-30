---
layout: post
title: "数据中台注"
tags: [技术杂文]
excerpt: "上海的雨，一直下个不停。这篇博客是针对数据中台的读书笔记。"
date: 2021-10-16 11:40:00
mathjax: true
---

按照一贯的文风，首先需要思考的是数据中台是个什么东西？数据中台不仅仅是技术，也不仅仅是产品，而是 一套完整的让数据用起来的机制。也就是说，数据中台=产品+技术+人。数据中台兼具业务价值和技术价值。站在技术角度观察，给出场景和计算能力的列表如下：

|编号|计算能力|场景|
|------|------|------|
|0|离线计算能力|报表需求|
|1|实时流式计算能力|准实时的指标统计和实时推荐|
|2|即席计算能力|圈人|
|3|在线计算能力|用户画像|

业务价值的实现需要依托一个价值框架：业务->（业务数据化）->数据->(数据资产化)->资产->(资产服务化)->服务->服务业务化->业务。整体上形成一个价值的闭环。

好了，我要搞一个数据中台，咋搞？

+ 数据汇聚
+ 数仓构建
+ 标签体系：面向具体对象构建的全维度数据标签，是面向业务视角的数据组织方式，标签体系要具备服务能力
+ 应用数据

具体的，以某地产公司为例的数据中台数据体系架构，如下：
![](https://s3.bmp.ovh/imgs/2021/10/bccab5fb1222d5a0.png)

+ ODS：业务系统数据的汇集
+ DW: DWD+DWS，业务系统是按照业务流程方便操作的方式来组织数据的，而DW是从业务易理解的视角来组织数据的
+ TDM: 通过ID-Mapping把各个业务板块，各个业务过程中的同一对象的数据打通
+ ADS：按照业务的需要从统一数仓层，标签数据层抽取数据，并面向业务的特殊需要加工业务特定数据，以满足业务及性能需求，向特定应用组装应用数据

对整个数据体系架构而言，ODS和ADS没有统一的构建规范，但是DW和TDM有统一的构建规范，同时TDM也是体现大数据能力的层。

在整个数据体系中，存在各种各样的数据。其中围绕元数据的各种应用比较有特色，具体应用如下：

+ 元数据浏览和搜索
+ 数据血缘：表A由表B，表C和表D级联得到，如果表A的数据不准确，可以追溯到表B，表C和表D
+ 影响性分析：判断当表A改变之后，是否会影响到与之相关的表B，表C和表D
+ 数据冷热度分析

除了元数据之外，主数据的构建和管理也是整个数据体系中的关键，并不是本篇文章讨论的重点。

基于数据体系的服务体系，主要包含四种服务方式，如下：

+ 查询服务：取数
+ 分析服务：算法分析
+ 推荐服务：主动的数据找人的过程
+ 圈人服务：基于标签

围绕数据中台，最上层的数据应用包括数据大屏，智能应用和数据报表。

扯了这么多，与NLP有什么关系呢？一个NLP的同学如何理解数据中台的概念。

+ 数据中台的研究对象是数据，文本是数据的一部分。由于数据的异质性，数据中台的活儿多是脏活儿累活，但是距离业务近，能够产生直接的业务价值，且有相对较长的研发周期，数据中台的活儿又是一个好活儿。
+ 数据中台可以包含算法中台，或者算法中台建立在数据中台之上。
+ 标准化能力构建对于数据中台的建立很重要，是数据打通的核心能力，但是不同的标准化，解决的难度不同。
+ NLP通过对非结构化数据的理解，能够扩展数据中台的数据颗粒度，更细的粒度在一定场景中能够产生更多的价值


相关文章和书籍：

+ 《数据中台：让数据用起来》，数澜科技中台团队的作品，个人还是比较喜欢这本书的写作风格。有对问题的严格化的定义，也有手记之类的有趣的场景对话。

+ 《大数据之路：阿里巴巴大数据实践》

+ [《数据资产管理白皮书4.0》](http://www.caict.ac.cn/kxyj/qwfb/bps/201906/P020190604471240563279.pdf)

+ [《数据质量漫谈》](https://mp.weixin.qq.com/s?__biz=MzIzOTU0NTQ0MA==&mid=2247506718&idx=1&sn=dd437ac302c2cad743dbfe611b7df917&chksm=e92ae611de5d6f07600d21d447a341d76462f25a095228f2a9d5d052eea4f17b42923d487dca&mpshare=1&scene=23&srcid=1227St8iO16IxvK0HMrn4ISB&sharer_sharetime=1640565716101&sharer_shareid=0e8353dcb5f53b85da8e0afe73a0021b%23rd)

+ [基础概念：维表与事实表](https://blog.csdn.net/qq_28666081/article/details/104686822)