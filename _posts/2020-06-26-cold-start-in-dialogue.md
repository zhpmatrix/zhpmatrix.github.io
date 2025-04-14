---
layout: post
title: "冷启动，知多少？"
tags: [NLP]
excerpt: "讨论一下对话系统中的冷启动问题"
date: 2020-06-26 10:25:00
mathjax: true
---

我想要做一个问答机器人，但是我只有问答库，咋搞？在一般的政府网站等，经常有一个栏目：问答栏目。该栏目就是一问一答。从产品交互上，对比如下：

|交互方式|优点|缺点|
|------|------|------|
|下拉列表，展示所有|信息冲击力强（电影院总是在印象城的最高层）|用户需要多次下拉，才可能找到需要答案，路径长|
|搜索框|较少搜索空间，是上述方式的泛化|需要增加搜索环节，模糊匹配答案，召回优化|
|问答机器人|直达答案本身|呈现给用户的信息量少|

按照标准的数据驱动建模方式，需要提前有对话数据才能建模。但是还没有一个对话机器人，怎么获取对话数据呢？（别问我：先有鸡还是先有蛋）

嗯。一般说来，先有一个问答机器人。当用户开始使用的时候，就有了对话数据，最重要的是获取用户想要问的问题，这样就可以形成一个迭代闭环。问答机器人上线，总是要能工作的，也就是对用户的输入有反馈，要能在一定程度上理解用户问题。这就是冷启动的场景之一。

#### 基于规则

对于问答机器人，可以直接基于编辑距离，如下：

```
from nltk.metrics import distance
distance.edit_distance('中国的首都', '中国的首都在哪')
```

计算用户输入和问答库中问题的相似程度。这种方式简单，可控，具有一定的可解释性。

对于任务型对话机器人，Slot Filling过程中，需要找到对应的槽和槽值。比如有下述的一些样本：

```
北京的天气
明天的天气
杭州气温
查询明天北京天气情况
请问一下明天北京天气如何
请问后天上海天气怎么样
```

想要抽取出日期和城市两个槽对应的槽值？看到一条正则：

```
.{0,2}[请问[一下]][${日期}][${城市}][的](天气|气温)[如何|怎么样].{0,2}
```
这条正则不包含实体和通配符，可表示144个句子。如果对话系统能够run起来，就可以收集到用户的真实问题，继而可以采用序列标注的方案等进一步提升效果。规则方案一般而言是高精确，低召回。

在其他场景中，比如可以做这样的变化，既而进入一个规则引擎。也就是过通用NER模型后，拿到类型信息，融合原始句子中的字符串，共同作为新句子的表示。

```
[LOC]的天气
[DATE]的天气
[LOC]气温
查询[DATE][LOC]天气情况
请问一下[DATE][LOC]天气如何
请问[DATE][LOC]天气怎么样
```

补充：

1.[聊天机器人中对话模板的高效匹配方法](https://blog.csdn.net/malefactor/article/details/52166235)，总结了三种规则范式，同时给出了一个加速模板检索的方案（基于倒排索引的方案）。

2.[知乎：目前，人工智能机器人能够在多大程度上代替企业客服？](https://www.zhihu.com/question/42988490/answer/153685380?utm_source=wechat_session&utm_medium=social&s_s_i=T8t%2BkZBClNuN%2FxlGmH%2FFbC1oUw6vIlOGjjPwhUdG7QA%3D&s_r=1&from=singlemessage)，郑一轩同学关于长短期记忆那块内容。

3.[小爱的单轮/多轮判不停策略](https://mp.weixin.qq.com/s?__biz=MzU2ODY2MTUwNQ==&mid=2247484059&idx=1&sn=f10fd8232df41452e17a749ac0e13ecb&chksm=fc8bc1f5cbfc48e36426ed593e6ee834f5793898d968e2a02a0f86b16af5f60f74c9085bc021&mpshare=1&scene=23&srcid&sharer_sharetime=1593437525269&sharer_shareid=0e8353dcb5f53b85da8e0afe73a0021b%23rd)

4.[基于词性的序列匹配](https://blog.csdn.net/weixin_34292287/article/details/91882974)


#### 多轮对话中的用户模拟器

在多轮对话系统中，拿到多轮对话的真实数据是一件成本巨高的事情。因此，可以借助用户模拟器在冷启动阶段产生训练数据，基于该训练数据得到相关模型之后，就可以得到一个基本的具有和人类进行对话能力的机器人，继而拿到人类的真实数据。混合机器和人类数据之后，重新训练优化相关模型。至于在线优化，是一个完全基于真实对话数据的优化过程。

该方向的工作，具体可以参考[最新综述：对话系统之用户模拟器](https://blog.csdn.net/c9Yv2cf9I06K2A9E/article/details/98549007)。

#### Few Shot Learning

上述讨论的问题是没有样本，这里讨论的问题是有一些样本，但是这些样本不足以训练一些对话系统中需要的模型，因此FSL就是一种解决问题的可能的方案。可以参考之前的文章[Few/Zero Shot Learning简单梳理](https://zhpmatrix.github.io/2020/02/14/shot-learning/)。

当然，FSL并非是解决少样本的唯一方法。数据少，那就搞更多的数据。[⽂本增强、半监督学习， 谁才是 NLP 少样本困境问题更优的解决⽅案？](https://cloud.tencent.com/developer/article/1648459)

除此之外，[平安科技的数据增强技术用于冷启动问题。](https://zhuanlan.zhihu.com/p/112877845)

参考:

1.[Lambda，柯里化与聊天机器人](https://zhuanlan.zhihu.com/p/100084125)

2.阿⾥云⼩蜜对话机器⼈背后的核⼼算法

3.《Generalizing from a Few Examples：A Survey on Few-Shot Learning》，最近比较新的综述文章

4.[柔性多模正则匹配引擎](https://mp.weixin.qq.com/s?__biz=MzU1NTMyOTI4Mw==&mid=2247507605&idx=2&sn=d4cfd8834f03a77936300536f4667769&chksm=fbd76cf9cca0e5effd671ebcf1bbde3bca4e141ef9ed42cd3723d094b65e6d5f227e1f1e8dd5&mpshare=1&scene=23&srcid=1129HUwTr4VcmjhR0aMPfwJ9&sharer_sharetime=1606586665741&sharer_shareid=0e8353dcb5f53b85da8e0afe73a0021b%23rd)