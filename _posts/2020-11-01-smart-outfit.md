---
layout: post
title: "[NLP]智能服饰搭配的方案讨论"
excerpt: "简单梳理专家模型，CV，NLP和Graph的各种解决方案和思路，以基于CV的几个工作为主。"
date: 2020-11-01 11:40:00
mathjax: true
---

近期做的一个工作是关于智能穿搭的，任务背景是在线上虚拟试衣间中，给定上衣，需要推荐下衣作为搭配。从整体上看，是一个推荐问题，技术思路是标准的召回和排序两阶段任务。在具体实现上，可以仅从NLP的角度求解，也可以从CV的角度求解，还可以从Graph的角度求解，本质上是利用的信息模态不同，当然可以做多模态信息融合。从学术角度上看，这个工作在CV的同学圈子中似乎做的更多一些，这里简单梳理一下相关经典工作。

一个基于专家模型的方案设计如下：

![img](https://ftp.bmp.ovh/imgs/2020/11/c7fd199751b66391.png)

流程上看主要是结构化引擎和业务规则引擎两个重点工作。这里关注其他的解决思路。

《Context-Aware Visual Compatibility Prediction》

这篇文章是基于GCN的建模方式，具体思路如下。将服饰搭配转化为一个基于Graph的Link Prediction或者Edge Classification问题，采用Triplet Loss作为损失函数。

![img_1](https://ftp.bmp.ovh/imgs/2020/11/bf69f02651d9c3ab.png)

其中，需要关注的是待预测商品（作为节点）的表征问题，一般采用基于BFS算法找到满足给定周围节点数的节点表征做融合，具体如下：
![img_2](https://ftp.bmp.ovh/imgs/2020/11/dc5094677b2f4992.png)

《Fashion Outfit Generation for E-commerce》

这篇文章采用二分类的方式来做。在特征表示阶段的做法如下，利用了多模态的信息，具体包括图片本身的信息，商品标题信息和商品类目（在电商体系下，这三类数据都比较容易获取）。

![img_3](https://ftp.bmp.ovh/imgs/2020/11/5a7ceb02e80e84e7.png)

二分类阶段的工作如下（比较朴素的做法）：

![img_4](https://ftp.bmp.ovh/imgs/2020/11/56ab90ac88c30699.png)

《Learning Type-Aware Embeddings for Fashion Compatibility》

这篇工作也是比较经典的，基于度量学习的方式，整体上的解决方案也相对朴素，模型架构如下：
![img_5](https://ftp.bmp.ovh/imgs/2020/11/b11886e1bd64d5e6.png)

对比三篇工作，第一篇主要亮点在基于Graph来做，这样理论上能够获取更加Structural的Context信息；第二篇的工作中规中矩，体现在Compatibality Prediction任务中，多模态信息融合的必要性；第三篇主要特色在于Metric Learning范式的使用，同时融合了多模态信息作为Regularization（学术灌水的标准套路）。

作为Compatibality Prediction任务的特色，三篇文章都在讨论的问题是：Similarity和Compatibality。在第三篇文章中，描述了二者的区别：

	Similarity：when two tops are interchangeable

	Compatibality：items of possibly different type that can go together in an outfit

一个好的模型，通常希望能够学到上述两个概念。在博主之前的问答匹配任务中，提到的两个概念是：相似性和相关性。和该任务相比，在概念学习上，有异曲同工之妙。

除此之外，还有很多其他有趣的基于Graph的任务，如下：

![img_6](https://ftp.bmp.ovh/imgs/2020/11/4e1c030dbff37e57.png)

[服饰搭配推荐研究综述](https://chenyue.top/2019/09/10/%E6%9C%8D%E9%A5%B0%E6%90%AD%E9%85%8D%E6%8E%A8%E8%8D%90%E7%A0%94%E7%A9%B6%E7%BB%BC%E8%BF%B0/)中，总结了该领域的问题和难点，数据集，评测方法和主流算法。从另外一个角度来看，也就是FashionAI的角度，相关工作为[FashionAI全球挑战赛决赛现场答辩](https://tianchi.aliyun.com/course/video?liveId=5437#postsId=5437)，具体内容为服饰关键点定位（服饰属性标签识别）。

除了基于CV和Graph的解决思路，还有基于NLP的方案，比如在[2015年天池大赛-淘宝穿衣搭配大赛：第一名方案](https://wenku.baidu.com/view/a4244b2130126edb6f1aff00bed5b9f3f90f726e.html)中，有一些相关讨论。由于比赛数据是脱敏的，因此无法直接使用。该比赛的基本解决思路有两种：第一种是给定商品，直接找可以搭配的商品；第二种是利用达人的搭配结果，通过计算商品相似性，得到可以搭配的商品。类比于问答系统，第一种给定Q，借助问答模型（生成模型等）直接得到A；第二种，利用QA知识库，通过QQ匹配，得到A作为返回结果。每类方案返回候选商品和搭配度，其中搭配度在不同的方案中，有不同的计算方式，最后通过线性加权的方式得到。


Graph结构是一种通用的数据组织方式，适用于图片和文本，在上文中讨论了基于GCN的商品穿搭任务，Graph用于NLP的相关工作，可以参考[GNN4NLP](https://github.com/svjan5/GNNs-for-NLP)和[benchmarking-gnns](https://github.com/graphdeeplearning/benchmarking-gnns)。考虑到Graph的组成元素，基本任务包括：Node Classification,Graph Regression, Graph Classification, Edge Classification/Link Prediction。

在本文的最后，通过一张图总结智能穿搭的技术线，如下：

|建模方法|优点|缺点|备注|
|------|------|------|------|
|基于规则的方法|可控，快速|专家介入|优先级=1|
|基于CV的方法|商品图片含有丰富的信息||优先级=2|
|融合CV和NLP的多模态方法|在图片信息的基础上，融合NLP的信息||优先级=3|
|数据挖掘的思路：CV/NLP融合结构化信息|更加丰富的信息维度|不同维度的贡献度衡量|优先级=4|
