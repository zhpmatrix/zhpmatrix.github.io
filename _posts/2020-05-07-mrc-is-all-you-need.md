---
layout: post
title: "[NLP]MRC is All you Need?"
excerpt: "讨论一些用MRC的方式建模文本分类，关系抽取，命名实体识别和指代消解等多个任务的想法"
date: 2020-05-07 10:25:00
mathjax: true
---

**总结：**

MRC是一个非常general的框架，多个NLP领域的经典任务都可以用MRC的方式来做。不谈MRC的思路为啥work，本质上，还是将一个复杂任务变为多个简单任务。或者说，将旧有分类器的压力分担到新的input端和新的分类器端。

但是这里有几个问题值得思考：

（1）如何构建Query，保证引入更多先验的信息？

（2）如何高效地解决inference时的N倍时间复杂度问题？（价值一个亿的问题）

（比如直接工程上并行；一次inference算多个结果；分两次算，先粗筛再细选）

（3）样本构建时的正负样本如何平衡处理？

（4）T5据说效果不错，我有想法，你有卡和时间吗？来个基于MRC的多任务预训练吧。


### 文本分类

[《Description Based Text Classification with Reinforcement Learning》](https://arxiv.org/pdf/2002.03067.pdf)

给定一个文本，进行多分类。如何改造成用MRC的方式做呢？对于每个类别，构造针对该类别的描述作为query，原始待分类文本作为context，联合query和context作为input，做二分类。

query如何构造？这篇文章提供了三种方式：

+ 基本模板：找到类别对应的维基百科的解释。（也就是该类别的定义描述）
+ 抽取式：从原始文本中抽取一些语句。（符合分类的经验性规律，只有关键语句有贡献）
+ 生成式：原始文本的摘要。（文本压缩或者简化的一种方式）

比如可以用于aspect-based情感分类任务。当然，input端不一定只可以使用一个Query，可以同时合并多个Query和一个Context作为input端，具体方式取决于你想怎么玩儿？（基于BERT的input端和output端的花式玩儿法已经腻了，溜了。）


沿着这个思路，重新思考brightmart的[将多标签分类转换成句子对任务](https://github.com/brightmart/multi-label_classification)，是不是有新的理解？（记得第一次看到的时候，觉得好有意思的想法）

### 命名实体识别

《A Uniﬁed MRC Framework for Named Entity Recognition》

传统的序列标注模型适合处理flat ner问题，但是对于nested ner问题处理较差（一个token对应多个标签，也可以通过multi-label解决），采用MRC的方式适合处理nested ner的问题。

思路同上，对每种标注类别，构建Query，和Context共同作为模型的input，预测该Query对应的实体位置。比如，对于LOC类别，可以构建的Query如：“请标注出文本中的地点，位置等词。”，同样Query的构建方式比较灵活，比如直接按照标注指南中的描述等。

[这篇文章](https://zhuanlan.zhihu.com/p/103779616)在具体中文任务上验证了该方法的有效性。除此之外，与该任务相关的另外一篇文章是《Dice Loss for Data-imbalanced NLP Tasks》，值得一提，但是超纲了。我自己在中文OntoNotes上亲测，显著提升。

其他两篇包括（这篇文章一脉相承，思想和上述类似）：

《Scaling up Open Tagging from Tens to Thousands: Comprehension Empowered Attribute Value Extraction from Product Title》

《OpenTag: Open Attribute Value Extraction from Product Profiles》

### 关系抽取

《Entity-Relation Extraction as Multi-turn Question Answering》，ACL2019

多数情况下，关系抽取最终的服务目标是填表。类似如下：

给定上下文：“zhpmatrix就职于地表最强科技有限公司，职位是NLP算法工程师。老张就职于京东，任职算法实习生。”

希望得到的结构化数据是：

|姓名|职位|公司|
|------|------|------|
|zhpmatrix|NLP算法工程师|地表最强科技有限公司|
|老张|算法实习生|京东|

通常的做法：第一步找到实体，人名，职位和公司；第二步：关系分类。

基于MRC的做法可以是这样滴，整体上更偏多轮对话的感觉。

Query0：文章中的人名都有啥？结果：zhpmatrix，老张

Query1：zhpmatrix为哪个公司工作？ 结果：地表最强科技有限公司

Query2：老张为哪个公司工作？结果：京东

......

对于职位，依次类推。那么，对于Query1和Query2，就可以用一个模型的形式表示：e\_i为哪个公司工作？

另外的一个工作更早一些，《Zero-Shot Relation Extraction via Reading Comprehension》，在建模方式上更加的直白。输入端由zhpmatrix+zhpmatrix为哪个公司工作？+Context，输出端：地表最强科技有限公司。输出端就可以使用找start/end的方式，比如按照二者乘积的最大值作为筛选条件，至于None的情况，在之前的博客中有讨论过，一定要考虑的细节。

除此之外，比较相关的两个工作（对怎样解决多次inference有启发）：

[LIC2019-第一名](http://tcci.ccf.org.cn/summit/2019/dlinfo/1104-ljq.pdf)

基本思路：第一步做多分类，找出文本中包含的所有关系；第二步合并关系三元组的Schema和文本作为输入，输出S和O。

[LIC2019-第七名](https://kexue.fm/archives/6671)

基本思路：P(S,P,O) = P(S)P(O|S)P(P|S,O)（怎么具体实现是一个有意思的课题。）

[“之江杯”-电商评论观点挖掘第二名](https://zhuanlan.zhihu.com/p/115851256)

### 指代消解

《Coreference Resolution as Query-based Span Prediction》，ACL2020

之前的指代消解的工作多是，第一步找到候选实体和指代词；第二步关系判断，是不是表示同一个含义？将MRC的思想用于指代消解的方式很简单。

基于候选mention构建实体作为Query，标注Context中指代的那个mention。

### 为啥非要用MRC的方式？传统的方式不香吗？

（1）构建的Query其实引入了一种先验，包含我们想要抽取的或者分类的信息。按照相关工作作者的观点，其实一种hard attention。当然在有些任务上，我们可以用其他方式来表达相同的含义，比如某种embedding，但是这种方式终究只能满足区分意图的目的，不能满足引入先验的目的。

（2）domain adaptation/zero-shot learning

对于命名实体识别任务，假设已经训练好了PER的模型，现在想抽取MAN后者WOMAN的实体，直接基于二者构建Query做抽取，不需要训练，试试看？

（3）灵活

想要啥，都写在Query中了。对于NER的传统模型，每次inference，有啥就抽啥？不想要啥，还得加个后处理。这种可插拔的特性的确很诱人。

（4）一套统一的框架做多个NLP任务

能用一套框架解的问题,个人不想用第二套来解。这样的另外一个好处是便于做多任务。

总体上，这种思路可以用于多个子任务还是会带来很多启发，注意细节，模型的设计还是比较灵活的，可以有很多有意思的做法。另外，多种想法是可以互相借鉴的，能够融会贯通，就能灵光一现。比如，谁说标注的时候一定要按照经典MRC的方式找start/end呢？BIO也OK啊，任务上就是序列标注。关键是要能够理解不同组件和策略的配合使用，空谈误国，干就完事儿了（最近莫名丧的不得了）。




