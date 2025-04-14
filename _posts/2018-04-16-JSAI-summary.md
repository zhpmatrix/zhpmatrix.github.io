---
layout: post
title: "2018-JSAI模式识别专委会学术年会总结"
tags: [技术杂文]
excerpt: "关于JSAI学术报告的总结，反思"
date: 2018-04-16 18:17:00
mathjax: true
---

二零一八年四月十三日，报告第一天。二零一八年四月十四日，报告第二天。早上的报告没有去听，还被老板逮个正着，囧；我们实验室是会务组，从北京返回学校，刚好赶上一大波Talk，也赶上了干活儿。读研期间，学院关于DM/ML/DL/CV/AI方面的Talk一向很少。这一波，估计把未来一年的Talk都给省了，逗乐。

《Kernel based Non-negative Matrix Factorization Method with General Kernel Functions》,是深圳大学的陈文胜老师带来的，讲了他的一个工作UKNMF，是Kernel NMF的一个推广，个人觉得类似generalize的工作，还是可以去尝试一下的。整个Talk很数学。

《面向大规模多模态机器学习的异构并行处理方法，平台与应用》，该报告由湖大的李肯立，同时也是国家超算长沙中心带来。Talk中提出，CNN的并行性，可以从**位级计算并行，神经元节点内计算并行，神经元节点间计算并行，层内并行和层间并行五个方面**来处理。同时，在处理方法中提到一种可能的解决途径是通信优化，具体来讲可以利用模型压缩，张量压缩的方法来提升通信效率；采用节点内和节点间的流水线处理技术和数据复用技术（避免重复数据传输）。

《Research Progress of Dynamic Fuzzy Machine Learning》,这个Talk是苏州大学李凡长教授的，他在1994年提出了"**动态模糊逻辑**"，围绕这个概念，一直做到了今天，做出了很多工作（发了很多Paper）。报告中给出了机器学习和大数据分析的各自五个原理，分别是一致性，对称性，泛化性，可度量，小样本；分解，扩展，表现，度量，拓扑；原理上的定义和阐述，对我而言，目前显得非常困难，但是直觉上是认同的。从参考文献上来看，这个概念已经应用在了机器学习的多个任务上，包括有监督，无监督等，在展望未来部分，李教授提出未来继续做的工作将**围绕dynamic fuzzy deep learning，dynamic fuzzy category learning，dynamic fuzzy topology learning三个方面**具体展开。搞模糊的有很多学者，但是从1994年坚持做到今天，并且和机器学习，过程控制等多个方面建立联系，属于非常基础性的工作，这从一定上启发研究者**要做基础性的工作**，影响力更大，产生的价值更多。

东南的耿新老师的报告是关于标记分布和标记增强的，这两个概念也是他们自己提的。个人感觉这个Topic没啥意思，不过发Paper还是可以Follow的，这里就不谈了。耿老师是学术界新星，自己看到问题，并分析解决问题，然后给大家分享自己的工作，真的是一件非常酷的事情！

《多智能体强化学习中的博弈和近似均衡》，是南京大学的高阳老师带来的Talk，我们实验室的常客了。在和高老师交流的时候，高老师骄傲的说，阿里那边做强化的都是我们的人。高老师总结大数据的关键技术是表示技术，学习技术和推理技术。这里翻翻教材，基于逻辑的演绎推理方法适用于小规模问题；而结合统计的归纳推理方法适用于大数据场景；直到面对复杂决策的动态推理技术。强化学习的本质在于Trial and Error（奖惩和试错），抽象模型包含reward，action，state。Talk中提到一个经典的博弈均衡解概念：纳什均衡，同时提出个体理性和集体理性相矛盾的本质。特意问了一下强化学习的落地情况，高老师说他不清楚啊。阿里巴巴2018年春节期间推了一本电子本《强化学习在阿里巴巴的技术创新和业务创新》，其中总结了阿里巴巴和其他高校，研究单位等合作的几个关于强化学习的报告应用于自己的业务中，落地场景具体怎样，不太清楚，报告中反馈不错，高老师也不知道。

《Built-in Feature Selection with Application in Machine Learning》,由福建师范大学的陈黎飞教授带来。回顾了维度Reduction的两类方法：Feature extraction(creating a subset of new features by combinations of the existing features)和Feature selection(choosing a subset of all the features).其中Feature selection包括Non-linear reduction（e.g., Kernel PCA）和linear reduction（e.g.,PCA）。整个报告更像是一个tutorial，其中也谈到了他们组近期的一些工作。

北邮杜军平老师的《基于时空特性的在线社交网络搜索研究》，讲了各种技术在微博社交中的应用。PPT做的很棒，个人感觉像在讲基金本子，学到的很少。

团队大腿吴小俊老师做了《Deep Learning Meets Shape Analysis》,Shape一直是一个比较难的问题，报告中纪老师问吴老师，你是怎么说服你的博士生做Shape的？在报告的最后，做了自己对于DL发展的几点感受：AutoEncoder is very unique；Layer wise learning is a breakthrough;semantic extraction is a milestone;CNN is a practical model;ResNN is a shortcut;GAN is a new horizon;**Combination and/or Fusion is the main method borrowing ideas from NN, PR, ML or even other disciplines**.个人对最后一点感受颇为认同。

沈红斌老师是我们大团队出去的老师，也是吴老板最为引以为傲的学生。做生物信息学蛋白质相关，从江苏科大被挖到上海交大，杰青。报告期间表示，希望我老板能够做出更好的多目标优化算法用于生物信息学科。本科第一，优秀硕士论文，优秀博士论文，很努力，很优秀。报告组织合理，思维严密。

整个报告听下来最有收获的是厦门大学纪荣嵘教授的报告，提问环节一连提了三个问题，会后也交流了一些问题。报告回顾了DNN面临的一些挑战，例如small training set;biased training distribution;online/incremental learning;un/weak supervised learning;inside DNN Black box;complexity of DNN(large parameters;high flop(floating point operation))，DNN的常用压缩方法：parameter sharing;parameter pruning;matrix decomposition;DNN的常用加速方法：binary network;structured pruning;tensor decomposition;他们组和腾讯优图，滴滴有很多模型压缩和加速方面的工作，具体可以阅读纪教授在人工智能前沿讲习班的文章[深度神经网络压缩及应用](http://mp.weixin.qq.com/s?__biz=MzIzNjc0MTMwMA==&mid=2247483920&idx=1&sn=9963a13afe1214f0b2bf4f520fa27d32&chksm=e8d275cbdfa5fcdd5f49fb186b0cabae7f5733249bc0436a069ad87635cc0445a6169b25dc17&mpshare=1&scene=23&srcid=04138IcRmwd6crwinNQKvU8l#rd)。

总结：两天的报告，第二天早上没有去听。提了大概五六个问题，晚上被老板拉去陪大佬们喝酒，还被几个大佬和同团队的老师夸了一波，嘻嘻。得到的几点认识：第一，搞研究要盯着一个点儿做深做细，从报告老师，从黄博，从我老板等都可以看到，只要做的足够深，足够细，一定可以做出有价值的工作，起码发Paper。第二，要注重原创精神。耿新老师和李凡长老师这些年都是做自己的东西，虽然自己的工作还是要和领域经典工作一块协作，但是做自己的东西很是令人敬佩。第三，部分研究要落地。纪老师的关于模型加速和压缩的工作不但引起了我个人的兴趣，同时也吸引了很多参会老师的兴趣，人气很旺。第四，和第一点相承接，要相信自己做的工作，不一定要赶热潮。比如NMF,比如kernel方法，比如Reduction等，还有很多人在做相关的工作。





















