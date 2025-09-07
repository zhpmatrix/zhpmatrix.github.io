---
layout: post
title: "再议推荐系统"
tags: [技术杂文]
excerpt: "杭州城，十里桂花香的季节，一篇迟迟未能写完的文章。"
date: 2021-10-25 11:40:00
mathjax: true
---

最近在阅读Ricci的[《Recommender Systems Handbook》](https://book.douban.com/subject/26437066/)，顺道阅读了公众号《炼丹笔记》的所有文章，公众号《机器学习与推荐系统》的所有文章，翻了RecSys等相关会议的一大坨纸，其中，不乏该方向上业界比较资深的大佬的观点和认识。这篇博客是笔者自己的一个笔记和心得。心得总述如下：

+ 推荐系统是一个算法，工程，业务强耦合的方向。其中，算法上的定义是良好且清晰的（定义简单，目标复杂），工程上需要多方数据联动，效率和稳定性保障，对业务的理解深度是影响推荐效果提升的重要变量（强业务属性）

+ 作为搜索，推荐，广告三驾马车之一，是商业变现的重要手段之一。NLP作为原子能力，通过支持三驾马车，间接赋能业务场景（NLP作为核心能力直面业务的场景极其稀有，在笔者之前的博客中有谈到类似问题）

+ Bias&Debias是推荐方向上一个非常核心且特色的课题，兼具理论价值和实际意义。

+ 推荐的工业属性决定在模型创新上进度慢于NLP，NLP的角色是隐藏在推荐背后的信号。

在接下来的内容中，详细探讨在阅读中的各种发现和想法。

	做一个推荐系统，我们的方向在哪里？

以项亮的观点，包含以下五个方面：

+ 准确。推荐的内容，希望尽可能都被用户采纳。（exploit）
+ 覆盖。在候选内容池中，被推荐的内容的比例。（保守和激进的系统属性）
+ 新颖。推荐给用户一些用户之前没有见过的内容。（explore）
+ 惊喜。推荐给用户一些能够给用户带来惊喜的内容。（business）
+ 可解释。推荐理由。（reasoning）

整体上，借助召回-粗排-精排-重排四个阶段的工作，实现从全部内容推荐出TopN个内容的目的。其中，召回阶段的主流做法是双塔模型，该阶段要求快速，高召回。典型地以Youtube的工作为例。整体上，业界围绕召回阶段的工作并不是很多，整体上主要围绕排序做。这里的问题：

+ 为什么推荐系统要分为召回+排序两阶段？（类似的问题，张俊林也有提到；在笔者自己的一个问答系统经历中，我们并没有采用这种划分方案）

+ 为什么相比排序，召回的相关工作较少？

一个相关的延伸问题是：搜索，推荐和广告本质上都在解决信息过载的问题，各自解决的手段，目标不相同，各自诞生在产品生命周期不同阶段，以至于系统实现不尽相同。但是，三者能否统一呢？（借邢无刀的问题）
，我们知道搜索是站在用户角度识别用户想要什么（搜索求准），推荐是站在平台角度看想要引导什么（推荐求新），广告是以局外人看广告主、平台、用户分别想要什么（广告求财）。

沿着一个技术脉络展开，主流的技术方向包括：

+ 协同过滤
+ 矩阵分解
+ 深度学习
+ 树（TDM）

决定是否上线的方式包括：A/B测试和Bandit算法，前者是业界的主流方式。

下文开始，将对主流的技术方向做一个宏观的总结和思考。首先，再次定义一个标准的推荐问题：

给定M个物品，N个用户的数据，只有部分用户和部分数据之间是有评分数据的，其它部分评分是空白，此时我们要用已有的部分稀疏数据来预测那些空白的物品和数据之间的评分关系，找到最高评分的物品推荐给用户。

具体怎么实现呢？

+ 回到本质。推荐的本质是猜你喜欢。既然是猜，就存在猜的维度。按照维度的复杂度，可以基于规则，按照比较硬的维度做推荐。

+ 协同过滤
	+ user-based：计算user的相似度。核心假设：相似的user喜欢相似的item
	+ item-based：计算item的相似度。核心假设：对于相同的user，喜欢相似的item 
	+ 区别：前者关注点在人，人的计算空间大，有利于实现”千人前面“；后者的关注点在物，物的计算空间小，有利于实现相对稳定的离线计算

+ 基于模型
 
 + 关联规则+分类+聚类
 + 矩阵分解：SVD为代表
 + FM:
      +  二阶特征的各自Embedding的内积作为二阶特征的weight，以一种soft的方式缓解大规模场景下的二阶组合特征的稀疏性问题（hard的方式分配weight/等价于多项式核SVM），更好的泛化能力的来源是Embedding。
      +  本质思想和矩阵分解类似（训练完成后，获取user和item各自的矩阵，可以作为各自的Embedding）。
      +  FM=MF+Side Info，都是针对二阶特征组合的，FM的二阶特征候选更大，MF只有user和item两类。
      +  一种演化路径：LR->FM->DeepFM
      +  FM实用性的关键步骤：O(KxNxN)->O(KxN),K=Embedding Dim, N=Feature Num
      +  召回：多路+策略+模型
      +  排序：特征
      +  假设能够将召回模型和排序模型都统一到特征的视角，一个有意思的想法
	+ Deep&Wide：Wide部分是LR模型，Deep部分是一个Deep模型
	+ DeepFM（D&W的升级版）
		+  Wide->FM
		+  Deep和Wide共享共享原始特征（FM的必要条件）
	+ DIN：Attention首次用于CTR问题
	+ TDM：基于Tree，item是叶子节点，解决召回阶段的TopK问题。树的非叶子节点有独特的特征含义。


除了上述讨论的话题，还有其他比较重要的问题：

+ EdgeRec
+ 序列/跨域/多模态推荐
+ 冷启动
+ Exploit&Explore
+ 隐私计算：联邦学习+安全多方计算+可信计算，见[同盾的工作](https://mp.weixin.qq.com/s?__biz=MzA3MTU2ODMzNA==&mid=2247499159&idx=1&sn=b75ce5f7fbdd8c74a011c89d9b2ca31f&chksm=9f292336a85eaa207bfca8a90c062332475df4b87e1cebb4047c172c1d4b95dd21efface9be3&mpshare=1&scene=23&srcid=1024zw56ptrAEP4wD9O4Im4q&sharer_sharetime=1635076861126&sharer_shareid=0e8353dcb5f53b85da8e0afe73a0021b%23rd)
+ Bias&Debias
	+ 针对开篇中的（3），各种Bias中最重要的是样本选择偏置，具体地将是负样本选择问题。比如常见的策略包括直接使用曝光数据作为负例，全局随机负例，Batch内负例，曝光+随机，Popularity-Based， Hard-Based的方法。在CTR问题中，正样本通过日志即可获得，负样本就需要通过构造的方式，因此构成了一个经典的只有正样本的场景（学术上PU-Learning）。 
	+ 《Bias and Debias in Recommender System: A Survey and Future Directions》	


在阅读过程中，夹杂着各种大问题，比如：

+ 数据挖掘模型+深度模型的融合， Deep&Wide为代表的工作，二者互为特征补充
+ 推荐+NLP的融合
+ 推荐中召回+排序的融合， 俊林的观点
+ 搜索+推荐+广告的融合，《Information Seeking: Convergence of Search, Recommendations and Advertising》


相关文章:

具体模型技术：

+ [FFM及DeepFFM模型在推荐系统的探索](https://zhuanlan.zhihu.com/p/67795161)
+ [推荐系统技术演进趋势：从召回到排序再到重排](https://zhuanlan.zhihu.com/p/100019681)
+ [推荐系统召回四模型之二：沉重的FFM模型](https://zhuanlan.zhihu.com/p/59528983)，这篇文章比较符合笔者当下的品味，开篇提出了两个有意思的问题：
	+ 是否我们能够使用一个统一的模型，将多路召回改造成单模型单路召回策略？如果不能，那是为什么？如果能，怎么做才可以？这样做有什么好处和坏处？
	+ 是否存在一个模型，这个模型可以将召回阶段和排序阶段统一起来，就是把两阶段推荐环节改成单模型单环节推荐流程？就是说靠一个模型一个阶段把传统的两阶段推荐系统做的事情一步到位做完？如果不能，为什么不能？如果能，怎么做才可以？什么样的模型才能担当起这种重任呢？而在现实世界里是否存在这个模型？这个思路真的可行吗?
+ [推荐系统召回四模型之：全能的FM模型](https://zhuanlan.zhihu.com/p/58160982)
+ [Recsys 2016 tutorial: Lessons learned from building real-life recommender systems](https://www.slideshare.net/xamat/recsys-2016-tutorial-lessons-learned-from-building-reallife-recommender-systems)
+ [推荐系统中的特征集列表](https://mp.weixin.qq.com/s?__biz=Mzg4MzU1NjQ2Mw==&mid=2247510505&idx=1&sn=a5b21ec251388c107ca9d03a92c7f1c8&chksm=cf4740e9f830c9fffc13f8c4a1c1e67262dd3aad0618b49ce009e25cedf315b50d0f816fe0e2&mpshare=1&scene=23&srcid=1025A8cmTfdKSsmVtAsKsJMo&sharer_sharetime=1635169333535&sharer_shareid=0e8353dcb5f53b85da8e0afe73a0021b%23rd)
+ [2021年推荐系统论文](https://mp.weixin.qq.com/s?__biz=MzA4NTUxNTE4Ng==&mid=2247507256&idx=1&sn=4eac18f14dc69e04975f7ae16e82a052&chksm=9fd453e5a8a3daf32ccf10a2ca62390c35540aa769939d52566a92e15427ccdd4a9808651740&mpshare=1&scene=23&srcid=1025C69Np1I9XxLeAvJGa12L&sharer_sharetime=1635121397281&sharer_shareid=0e8353dcb5f53b85da8e0afe73a0021b%23rd)
