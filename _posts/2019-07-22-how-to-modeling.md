---
layout: post
title: "[比赛]用两种思路解2019之江杯的电商评论观点挖掘问题"
excerpt: "2019之江杯全球人工智能大赛的电商评论观点挖掘任务为例，讨论一下对如何建模的思考。"
date: 2019-07-22 15:48:00
mathjax: true
---

个人比较喜欢的建模方式：

（1）通过设计schema，用一个sequence labeling的模型来搞定，可以看下文的思路二；

（2）《BERT for Joint Intent Classification and Slot Filling》，整体上还是一个sequence labeling的模型，不过添加了一个分类任务，通过joint的方式来做；


截止写这篇博客时，距离比赛的数据公布还有不到两周的时间，这是[比赛地址](https://zhejianglab.aliyun.com/entrance/231731/information)。评论文本和标签如下所示：

![img1](http://wx4.sinaimg.cn/mw690/aba7d18bgy1g58qhhmkgoj20vy0ckq6p.jpg)

![img2](http://wx2.sinaimg.cn/mw690/aba7d18bgy1g58qhdo9qzj20vo0a2n0n.jpg)

乍一看，感觉这是一个情感分析的常规任务，其实不然。再一看，是一个面向切面的情感分析，不完全正确。这是一个什么任务，与建模的方式有关。头脑风暴后，能够想到的比赛有：

1.HPC2017"英特尔"杯-面向金融评论文本的情感分析

任务输入是一段评论文本，输出是N个维度(环境服务，优惠力度等)的情感值。

2.AI Challenger2018-细粒度用户评论情感分析(美团数据)

任务输入是一段评论文本，输出是N个维度(距离远近，环境优美等)的情感值。**和1的主要区别是N个维度是细粒度的。**

3.DataFountain2016-[基于视角的领域情感分析](https://www.datafountain.cn/competitions/237/faq)(汽车领域的新闻、微博及论坛数据)

|Content|View/Opinion|
|------|------|
|比众泰更早一步，江淮版兰博基尼，10万可带走|众泰/neu，江淮/neu，兰博基尼/neu|
|近日官方公布了全[汽车]新威朗的内饰图片，威朗内饰的布局、用料以及制作工艺都有着很高的水准。|威朗/pos|

**也就说，该任务需要先找到实体，然后判断实体的情感值。**


4.2017CCF大数据与计算智能竞赛-基于主题的文本情感分析(电商评论数据)

|	content-评论内容|	theme-主题|	sentiment\_word-情感关键词|sentiment_anls-情感正负面|
|------|------|------|------|
|收到了，太实惠了，买了一大箱，以后继续购买，送货速度快服务也好|NULL;送货速度;服务;|	实惠;快;也好;	|1;1;1;|
|	热水器加热时间太长，安装费太贵，预留太阳能口摆设，根本用不到，没有水位指示器，加满热水的指示灯放在了最侧面，不方便用户看指示灯，必须斜着看才能看到，|	加热时间;安装费;用户;	|太长;太贵;不方便;	|-1;-1;-1;|

相比3，该任务要求识别的内容更多，最后才是情感值。

那么在今年的之江杯中，**和4的主要区别在于，增加了要识别实体的categories**。

那么，如何建模呢？明显可以看到，之江杯的比赛，需要预测的内容更多。那么，这里给出两种启发性的思路。

#### 第一：情感分类。

参考2017年的论文《Target-dependent Sentiment Analysis of Tweets using a Bi-directional Gated Recurrent Unit》中提到了一种结构，如下：

![img3](http://wx3.sinaimg.cn/mw690/aba7d18bgy1g58p7d65q4j20xs0d50v7.jpg)

因为文章比较早了，因此结构上并不复杂。如何使用？以上文中的任务3为例说明如下：

> 我 不太 喜欢 宝马 ， 奔驰 比较 适合 我 。

这句中的实体词包括**宝马**和**奔驰**，当预测**宝马**的情感值时，将宝马两侧的文本的BiGRU的embedding做一个merge，然后进全连接层(分类器，三分类)。当然，也可以merge宝马对应的embedding。这里给出一个有意思的问题，当一个句子中出现多个相同实体，如何处理？（由一到多的场景，需要在多数任务中遇到。）

其实，上述的思路在之前做纠错的任务时，英语流利说团队就用几乎相似的结构在国际某项评测数据上拿到了第一的成绩。另外，在之前的博客[神经关系抽取](https://zhpmatrix.github.io/2019/06/30/neural-relation-extraction/)中，类似的结构被多次提到，同样在ACL2019的工作中也可以看到。

之江杯同样可以尝试这种思路，不过需要处理一些相对Tricky的问题。


#### 第二：序列标注。

由于对ACL2017的工作《Joint Extraction of Entities and Relations Based on a Novel Tagging Schem》印象太深，因此看了之江杯的问题之后，个人会比较感兴趣的方案是基于序列标注的。同时从另外一个角度来讲，是joint learning的一些问题，**实体识别+情感分类**。

沿着这篇工作，问题的关键是**如何设计一个标注方案？**

这里使用的一种方案是这样的，整体上'BIO'标注，作为第一级标注；第二级标注包括：Categories+Polarities。标注的对象是AspectTerms+OpinionTerms。参考代码如下：

```
def get_labels(self):
        """See base class."""
        label_list = []
        bio_list = ['B','I']
        cate_list = ['wuliu','chicun']
        opinion_list = ['pos','neu','neg']
        
        label_list.append('[MASK]')
        label_list.append('O')
        label_list.append('[CLS]')
        label_list.append('[SEP]')
        for i in bio_list:
            for j in cate_list:
                label_list.append(i+'-'+j)
            for k in opinion_list:
                label_list.append(i+'-'+k)
        return label_list
```

基于这种方法，假设Categories的个数为N，则总共的类别数为**2\*N+2\*3+1**!所以，也可以不采用这种方法，有一些其他的标注方法可以尝试，比如去掉'BI'的层级；使用'BIEO'的标注等。

通过上述方式，简化了问题的解决，同时不会存在ACL2017的文章中一个位置对应多个标签的问题(有一些解决方案，可能会在稍后的博客中讨论吧)。

基于这种思路，基于pytorch-transformer实现了一个[参考方案](https://github.com/zhpmatrix/pytorch-transformers/tree/zhijiang)。


