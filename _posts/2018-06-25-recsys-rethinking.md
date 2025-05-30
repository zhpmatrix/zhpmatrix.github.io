---
layout: post
title: "《推荐系统实践》读书笔记"
tags: [读书笔记]
excerpt: "一直对推荐系统保持好奇心，但是没有系统的读过推荐系统方面的资料。最近可能需要一些推荐系统的知识，所以花了一个下午和一个晚上的时间读了项亮的《推荐系统实践》这本书，这篇博客主要是读书笔记，有一些自己的认识和总结。"
date: 2018-06-25 12:17:00
mathjax: true
---

### 总结

花了一下午和一个晚上读了项亮的《推荐系统实践》这本书，边读边做笔记，因此这篇博客其实是一个读书笔记。看到扉页上写道二零一二年六月第一版，距离现在已经差不多六年了。书中几乎没有谈任何深度学习的一些东西，实际上深度学习也已经在推荐系统中发挥作用了。回顾近年，似乎机器学习算法在搜索，广告，推荐领域的变现能力比其他领域好很多。

书中大多举了Amazon和Twitter的一些经典Case，但是其实国内今日头条的推荐系统自己从用户体验上来说感觉也很好。这本书带我我的感觉和读深度学习之前的一些计算机视觉的工作类似，很简单但是在给定数据集上很有效的数学技巧，令人印象深刻。最重要的是全书一直在强调推荐结果的可解释性。总体上的一个认识是推荐系统需要好的特征工程，需要好的工程化。


### 理论轮廓 

《推荐系统实践》序二中，陈义谈到"可能因为是数据资源的限制，大多数学术论文都把推荐问题看做评分预测问题，而实际应用中最常见的是TopN推荐。虽然TopN推荐问题可以归纳成评分问题，但并不是每种评分预测算法都能直接来解决TopN推荐问题。"

推荐系统可以按照数据分为协同过滤，内容过滤，社会化过滤；按照算法分为基于邻域的算法，基于图的算法和基于矩阵分解或者概率模型的算法。在业界得到最广泛应用的算法是基于邻域的方法，基于邻域的方法主要包含两种算法，基于用户的协同过滤算法和基于物品的协同过滤算法。

### 上线步骤

一个新的推荐算法最终上线，通常需要完成三个实验。

第一，通过离线实验证明它在很多离线指标上优于现有的算法；

第二，通过用户调查确定它的用户满意度不低于现有的算法；

第三，通过在线的AB测试确定它在我们关心的指标上优于现有的算法；（补充：使用[bandit算法](https://zhuanlan.zhihu.com/p/21388070)，会获得更快的测试结果。比如给某个用户推荐多个商品，每个商品可以维护一个beta分布。在推荐的时候，每个分布产生一个随机数，排序后选择TopN随机数对应的商品推荐给用户，如果用户点击了推荐商品，对应商品的beta分布的下界加一，否则上界加一。）


### 评测标准

结合实际情况，大多数科研成果集中在离线实验。项亮在书中谈到，用一个数学公式表达，离线实验的优化目标是：

最大化预测准确度

使得，覆盖率 > A
     多样性 > B
     新颖性 > C


### UserCF&ItemCF

简单场景下的UserCF中，

    计算用户UserA对物品ItemB的感兴趣程度 = UserA和UserC之间的相似程度 x UserC对ItemB的感兴趣程度

针对简单版本UserCF的一个重要改进是，如何判断两个用户之间的相似程度？一个重要的启发是两个用户对冷门物品采取过同样的行为更能说明他们兴趣的相似程度。也就是说要从余弦距离中消除二者对热门物品的感兴趣程度。

简单场景下的ItemCF算法并不利用物品的内容属性计算物品之间的相似度，而是通过分析用户的行为记录计算物品之间的相似度。物品A和和物品B具有很大的相似性是因为喜欢物品A的用户大都也喜欢物品B。因此，这也导致了ItemCF的一个优势是可以提供推荐解释，利用用户历史上喜欢的物品为现在的推荐结果进行解释。

同样的一个改进工作类似于UserCF，该工作认为活跃用户对物品相似度的贡献应该小于不活跃的用户。

围绕该工作，一个重要的数学技巧是对物品相似度进行归一化。优点不仅仅在于增加推荐的准确度，还可以提高推荐的覆盖率和多样性。

关于二者的比较，项书中给出了很好的总结。UserCF的推荐结果着重于反映和用户兴趣相似的小群体的热点，而ItemCF的推荐结果着重于维系用户的历史兴趣。换句话说，UserCF的推荐更加的社会化，反映了用户所在的小型兴趣群体中物品的热门程度，而ItemCF的推荐更加的个性化，反映了用户自己的兴趣传承。

此外，从工程角度来看，维护User相似度矩阵和Item相似度矩阵的代价不同。

以上，例如爱艺奇动漫，豆瓣，网易云音乐之类的适合ItemCF，微博，社交平台等适合UserCF。

这里，思考一个问题，物品A和和物品B具有很大的相似性是因为喜欢物品A的用户大都也喜欢物品B的想法没有错，但是也不是绝对的，能不能回到对物品A和物品B本身相似性的理解上？这样，我们得到的启发是，

由于物品A和物品B相似，所以喜欢物品A的用户大都喜欢物品B。和原始观点因果倒置！实际上，更应该关注相关而不是因果。

除了上述经典的两种方法，还有基于隐语义模型和基于图的方法。

隐语义模型的核心思想是通过隐含特征联系用户和商品，下文中的ALS可以认为是隐语义模型的一种方法。和基于统计的方法相比，隐语义模型离线计算的空间复杂度更低，时间复杂度相似，不能支持在线实时推荐，同时不具备良好的推荐解释性。

基于图的方法也是一个很自然的思路。用户和物品之间的关系是多对多的，这种关系恰巧对应着二分图。完成了这种转化之后，就可以从图论的一些角度讨论相似性的问题。

直觉上看，隐语义模型和图方法理论上应该都很漂亮，但是具体的应用情况如何，还不太清楚。


### ALS

任务描述如下，给定一个表格，表格的行表示用户，表格的列表示商品，表格中的数据表示用户对商品的打分，商品可以是电影，文学作品，美食等。

|item0|item1|item2|item3|item4|item5|
|:-|:-|:-|:-|:-|:-|
|user0||3||5||6|
|user1|8|||2|||
|user2||3|9|||6|
|user3|1|3||4||6|
|user4|||2|||6|

观察上述数据，存在数据为空。真实场景下，这个表格会非常大，因此在一定程度上可以假设表格对应矩阵是稀疏低秩的。所以，假设该矩阵为A(mxn)，该矩阵可以分解为A(mxn)=U(mxk)V(kxn)。

其中，U可以认为是对用户偏好特征的嵌入表示，V是商品特征的嵌入表示，则用户i对商品j的偏好可以表示为u(i)^Tv(j)。这里问题的关键是计算U和V，如何计算？

因为A=UV，显然可以使用A-UV的损失作为优化目标。这里既可以认为是最小二乘法思想的使用，也可以认为是使用Frobenius范数来量化重构U和V产生的误差。

从数学角度讲，上述问题是矩阵分解，相关工作非常丰富。但是从工程上讲，A过大，直接的矩阵分解对存储和计算都是巨大的问题，因此采用迭代求解的方式，寻找数值解而不是解析解。

如何求解？考虑到U和V的耦合关系，可以使用[坐标下降](https://www.cnblogs.com/flyfatty/p/6684305.html)求解，给一个名字叫做交替最小二乘算法。

在Spark的MLlib中有对应的[ALS实现](https://www.cnblogs.com/mstk/p/7208674.html)，

    import org.apache.spark.mllib.recommendation.ALS

站在协同过滤的角度来说，ALS算法属于User-Item CF，同时考虑了User和Item的信息。缺点在于，U和V是假设不变的。一旦U和V发生变化，需要重新计算，这也是真实场景下的问题。从这个角度讲，这也是一个离线算法。

分解出U和V之后，可以利用U和V计算用户和商品的相似度。这是一个非常重要且有趣的应用，原始空间相似的用户或者商品在映射到新空间之后，仍然距离最近。因此，这里再次印证了可以从Embedding角度看待这个问题。

### "冷启动"问题

冷启动问题主要分为三类：用户冷启动，物品冷启动和系统冷启动。

具体的解决方案有：

1.给新用户推荐热门排行榜，等用户数据收集到一定时候，切换为个性化推荐。

2.利用用户注册时的人口统计学信息，粗粒度推荐。

3.利用用户的社交网络账号登录信息。

4.要求用户在登录时对一些物品信息进行反馈。

5.新加入的物品，按照物品内容相似性，进行推荐。

6.针对系统冷启动，引入专家知识，迅速建立物品的相关度表。

### 利用用户标签数据

标签系统中的推荐问题主要有以下两个：

1.如何利用用户打标签的行为为其推荐物品？（基于标签的推荐）

2.如何在用户给物品打标签时为其推荐适合该物品的标签？（标签推荐）

同样可以用图的语言重新描述上述问题，构建用户-物品-标签图。

### 利用上下文信息

典型的上下文信息包括时间和地点。针对于时间，问题的关键在于如何在不损失精度的情况下提高推荐结果的时间多样性？

首先，保证推荐系统能够在用户有新的行为后及时调整推荐结果。

其次，保证推荐系统在用户没有新的行为时也能够经常变化一下结果。

### 利用社交网络数据

六度原理是这样的，

    社会中任意两个人都可以通过不超过六个人的路径相互认识。也就是社交网络图的直径为6.

社交网络研究的数学工具是随机图理论。研究工作中两个最重要的问题：第一个是如何度量人的重要性，也就是社交网络顶点的中心度。第二个问题是如何度量社交网络中人和人之间的关系，也就是链接预测。


### 推荐引擎设计

对于一个基于特征的推荐系统架构，推荐引擎根据用户信息(用户属性，用户历史行为)生成用户特征向量，根据候选物品集合，构建特征-物品相关推荐，形成初始推荐结果。这个阶段称为召回。然后对初始推荐结果进行过滤，排名，形成推荐解释，生成最终的推荐结果。这个阶段称为排序。

从存储角度，数据来源可以是数据库，缓存，分布式存储文件等，而且多数场景下，推荐引擎的设计是可插拔式的。

### 经典回顾-评分预测模型

潜语义模型和矩阵分解模型说的是一回事，就是如何通过降维的方法将评分矩阵补全？

传统的SVD分解在存储和计算上不可行。空值填充之后会使得稀疏矩阵变为稠密矩阵。

改进版的Funk-SVD用更简单的思路解决了这样的问题，其实就是上文提到的ALS。如果你对名词感到困惑，不要太纠结，注意形式化表达和求解过程。

在评分预测模型中，同样需要加入时间信息，一种是将时间信息加入到基于邻域的模型中，另一种是将时间信息应用到矩阵分解模型中。

在推荐相关的比赛中，常用的模型融合方式包括模型级联融合（和Stacking，Adaboost等思路类似）和模型加权融合。



相关论文：

1.《Large Scale Parallel Collaborative Filtering For The Netflix Prize》

2.《Collaborative Filtering For Implicit Feedback Datasets》

3.《Matrix Factorization Techniques For Recommender Systems》





















