---
layout: post
title: "[paper]Learning from Imbalanced Data"
excerpt: "解决数据不平衡问题的一篇论文笔记"
date: 2017-02-20 12:00:00
---

真实场景下(比如广告点击问题，乳腺癌诊断问题)，会遇到一个问题：

**原始数据集中正例比反例多，数据集会使得学习到的模型更偏向于预测结果为正例。**

这就是**数据不平衡问题**。一般的学习器都有下面的两个假设：**通过学习器可以使得预测准确率提高**和**数据独立同分布**。如果数据不平衡，学习器使得准确率最高应该是偏向于预测结果为比例更大的类别。比如说正例为1%，反例为99%，很明显的是即使不学习，直接预测所有结果为反例，这样做的准确率也能够达到99%，而如果建立学习器也很有可能没有办法达到99%。这就是数据比例不平衡所造成的问题。

这是一篇论文笔记，主要梳理了论文思路，为以后遇到此类问题能够找到合适方案打下基础。笔者在文中尽量按照作者原始意图表达，但是可能会掺杂部分个人观点和理解。
这是一篇解决数据不平衡问题的综述性文章，2009年发表在IEEE TRANSCATIONS ON KNOWLEDGE AND DATA ENGINEERING,共22页，参考文献148篇。作者为Haibo He,史蒂文斯理工学院助理教授(2009年)

1.简介

关于非平衡学习的研究，作者给出一张图：

![Number of publications on imbalanced learning](http://wx1.sinaimg.cn/mw690/aba7d18bgy1fd2mq525u6j20fd09eq3i.jpg)

数据不平衡是数据的一个本质特征，同时也是现实世界中真实数据的反映。**标准算法的前提假设是：数据平衡和误分类误差代价相同**。比如乳腺癌诊断问题中，乳腺癌患者是少数，此外，把一个正常人预测为乳腺癌患者的代价远远小于把一个乳腺癌患者预测为正常人的代价。

2.非平衡学习本质

关于非平衡学习的本质，作者给出了两个概念：**类间不平衡和类内不平衡**。如下图：
![between-class imbalance and with-in class imbalance](http://wx4.sinaimg.cn/mw690/aba7d18bgy1fd2ndzos2oj20m10cf0wg.jpg)

个人认为：通常情况下，更多的关注在类间不平衡，比如我们常常讨论的正例和负例的数目多少的问题。而类内的不平衡可能会被忽视。

3.非平衡学习的经典方法

作者总结了四类处理非平衡学习的技术：采样方法，代价敏感方法，核方法和主动学习，以及其他具有代表性的工作。

3.1 采样方法

3.1.1 oversampling&undersampling

举个[例子](https://en.wikipedia.org/wiki/Oversampling_and_undersampling_in_data_analysis), 假设我们有一个样本集，共1000人，其中有2/3的男性(比如，这个数据集是从江南大学中心篮球场采集的数据)，而通常的人口分布中1/2是男性。如果我们希望数据分布满足这样的特征，oversampling的方法是将一个女性样本当做两次，这个可以得到一个1333个样本的数据集，其中男女分布满足1/2。当然，对应的方法是undersampling, 随机的从男性数据中选择约333个样本，这样得到的数据仍然满足通常的性别分布。从中我们可以看到的问题是，虽然满足了目标分布，但是同时改变了数据集的大小。

3.1.2 informed undersampling

关于该采样方法，作者提出了三个例子：EashEnsemble&BalanceCascade, KNN classifier, 和 one-sided selection method。与KNN相关的方法有四种，分别是，NearMiss-1,NearMiss-2,NearMiss-3和"most distant" method。其中NearMiss-2的表现最好。从大类(undersampling是从大类中选样本)中选择的样本具有这样的特征，小类中距离该样本最远的三个样本到该样本的平均距离最小。一种简单的操作上的表达是计算大类样本中每个样本和距离该样本最远的三个小类样本平均距离，排序后从大类中选择满足目标分布的样本数目。

3.1.3 synthetic sampling with data generation

作者用SMOTE技术作为例子，同时提出了它的一般版本，如图：

![SMOTE](http://wx2.sinaimg.cn/mw690/aba7d18bgy1fd2pp84iulj20m70cljud.jpg)

SMOTE技术利用特征空间相似性生成新的样本数据，在一些应用场景下取得了较好的效果。但是作者提出，SMOTE仍然有自己的缺点，比如过度泛化和方差较大。

3.1.4 adaptive synthetic sampling

SMOTE的缺点是由于它生成样本的方式导致的。此处，提到了一种新的样本生成的方式，如下：

![SMOTE-NEW](http://wx2.sinaimg.cn/mw690/aba7d18bgy1fd2qau0lirj20lm0bdtbi.jpg)

除了上述方式，还有基于数据清洗的采样方法，基于聚类的采样方法，同时整合采样(sampling)和提升(boosting)的方法也有出现。

3.2 代价敏感方法

采样方法试图平衡数据的分布，代价敏感方法则考虑误分类样本的代价。作者指出，在一些领域，代价敏感方法要优于采样方法。

3.2.1

关于代价敏感学习框架，作者提到了现在代价敏感方法实现的三类方法：第一类方式是将误分类代价应用到数据加权，本质上是代价敏感采样方法，通过误分类的代价来选择最好的训练数据。第二类是将误分类应用到集成学习中。第三类直接将代价敏感函数或者特征吸收进分类范式。

3.2.2 cost-sensitive dataspace weighting with adaptive boosting

3.2.3 cost-sensitive decision trees

就决策树而言，代价敏感方法可以用到三个地方：决策阈值的选择，每个节点分割准则的确定和剪枝策略。当考虑将代价敏感性引入到分割准则的确定中的时候，首要的任务是拟合一个对不同代价不敏感的不纯度函数(熵，Gini系数等)。决策树的剪枝策略是为了提高决策树的泛化性能，但是在遇到数据不平衡的时候，倾向于剪去描述小类概念的节点。

3.2.4 cost-sensitive neural networks

就神经网络而言，代价敏感方法可以用到四个地方：首先可以应用到概率估计，其次是神经网络的输出，第三是学习率，最后可以用于误差最小化改进。除了应用到决策树和神经网络之外，还有研究者将代价敏感方法引入到贝叶斯分类器，支持向量机等。

3.3 核方法和主动学习

3.3.1 kernel-based learning framework

关于核方法的研究主要集中在统计学习和VC维理论，最具有代表性的学习范式是SVM，但是对于SVM，当面对非平衡数据时，分割超平面的位置会有所偏移，从而导致SVM的性能有所下降。

3.3.2 integration of kernel methods with sampling methods

在学术界，已经有些工作是将采样和集成技术引入SVM，其中具有代表性意义的是GSVM-RU算法。

3.3.3 kernel modification methods for imbalanced learning

除了关注采样和集成技术，还有一些工作关注SVM机制本身，这类方法称为核变方法(kernel modification method),典型的例子包括：基于正交前向搜索和标准正交加权最小平方的核分类构造算法，调整SVM类边界的算法及其变种，模糊SVM核方法，k类最优SVM，支持聚类机。

3.3.4 active learning methods for imbalanced learning

3.4 其他方法

4.非平衡学习的评价方法

关于评价方法，作者总结了五个方面的问题：混淆矩阵(confusion matrix), ROC曲线(receiver operating characteristic), PR曲线(precision-recall), 代价曲线, 以及多分类问题背景下的评估方法。

4.1 confusion matrix

4.2 ROC

4.3 PR

4.4 cost curve

4.5 多分类非平衡学习中的评估方法

5.机会和挑战

在文中，作者提出五个方向，分别是对非平衡学习问题的深刻理解，建立统一基准平台，建立标准评估方法，针对非平衡数据的增量学习和针对非平衡数据的半监督学习。

作者首先提出要进一步认识非平衡学习问题的本质。什么样的假设可以使非平衡学习算法更有效？(关于问题假设，举个例子，在时间序列分析中的平稳序列假设和常见的独立同分布假设)，对于非平衡数据集，应该平衡到什么程度比较合适？不平衡数据的分布是怎样影响学习算法的计算复杂度的？给定非平衡数据分布的泛化误差界是什么？有没有一些针对特定领域和算法的理论方法？（个人观点：这个方向的问题比较基础但是同时比较深刻）

针对建立统一基准平台：在知识发现和数据工程研究中，数据资源起着决定性的作用。
虽然现在有UCI Repository和NIST Scientific and Technical Databases，但是这是不够的。作者指出了可能导致非平衡学习中瓶颈的三个方面：缺乏标准的性能评测基准，不同学科之间缺乏数据共享和数据传播，学术界的研究团队各自准备自己的数据集增加额外成本，包括时间和精力等。

针对建立标准的评估方法：作者认为现在的研究工作中，每种技术都有自己的评估手段，这不利于不同技术研究之间的沟通和比较。

针对非平衡数据的增量学习：在Web数据挖掘，传感器网络，多媒体系统等领域需要流式数据学习技术，如果在学习期间出现不平衡性，我们能够自动地调整学习算法吗？在增量学习期间，我们可以考虑重新平衡数据集吗？如何可以，怎样做？我们怎样利用先前的经验和知识来自适应的改进从新数据中学习的能力？我们怎样处理新引入的概念也是不平衡的问题？(例如非平衡概念漂移问题)，对[concept drifting的理解](https://en.wikipedia.org/wiki/Concept_drift)。

针对非平衡数据的半监督学习：半监督学习面对的数据是有标签和无标签的数据，该学习重要的想法是利用有标签数据的信息来完善无标签数据的信息(例如标签特征)，典型方法有cotraining, self-training methods, semisupervised support vector machines, graph-based methods and Expectation-Maximization(EM) algorithm with generative mixture models等。具体问题是：我们怎样判别一个无标签数据是来自隐藏的平衡平布还是非平衡分布？在给定有标签的非平衡数据集的前提下，高效找到无标签数据的标签的方法是什么？利用传统的半监督学习方法找到无标签数据的标签，这个过程引入的偏差是什么？

结论：在这篇论文中，我们讨论了知识发现和数据工程领域一个既有挑战性又非常重要的问题-数据不平衡学习。我们希望这些对不平衡学习问题的本质的讨论，用来表述该问题的较好的方法的陈述，检验该问题解决方案好坏的评估技术的整理能够为现在和将来知识发现和数据工程领域的研究者和实践者们提供一份全面的材料。此外，我们希望我们发现的在这个相对较新领域(2009年)的一些机会和挑战能够指引潜在研究者为该领域的未来发展做出更好的贡献。

参考：

1.[How to handle Imbalanced Classification Problems in machine learning?](https://www.analyticsvidhya.com/blog/2017/03/imbalanced-classification-problem/)
