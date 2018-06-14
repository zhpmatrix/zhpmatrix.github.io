---
layout: post
title: "[DL]关于样本的Hard和Easy的讨论"
excerpt: "围绕CVPR2005，CVPR2016的两篇文章，hard negative mining, hard example mining, OHEM等，从prob和loss两个角度讨论，同时提了一些想法。"
date: 2018-06-06 13:34:00
mathjax: true
---

CVPR2005的文章《Histograms of Oriented Gradients for Human Detection》中，提到的Hard Negative Mining，过程是这样的，那个时候是HOG+SVM的光辉岁月。

第一步：构建Positive(pos)和Negative(neg)样本组成的数据集，训练一个分类器(cls)；

第二步：用cls预测neg，得到预测prob>0.5的所有neg对应的feature和prob；

第三步：把第二步得到的feature喂给cls，重新train；

第四步：把第二步和第三步迭代几次；

考虑一下第二步，prob>0.5，意味着label为true，也就是将一个neg预测为pos，没有human的patch预测为有human。没有overfitting的前提下，用cls重新预测neg，得到的预测值为pos，意味着该样本为hard。通俗点讲，**“做过的题目还做错，可能这道题是真的难，难题多做几遍就不会错了”**，所以，针对hard的样本，重新将对应feature喂给cls，再train一遍，实际上确实有效果提升。

针对二分类问题，通常以prob=0.5为阈值，划分预测标签。实际上，prob的取值范围是\[0,1\]，假设一个样本的prob非常的靠近0或者1，意味着这个样本属于某一类的置信度非常高，prob靠近0.5，也就是cls对于该样本属于哪一类并不是很自信。从这个角度来讲，针对所有样本，根据预测prob的取值范围区分hard和easy样本，或许也是可行的？

上述想法的一个延伸是这样的，针对多分类问题，每个样本会得到一个预测prob向量，若向量prob的max值小于一个阈值，例如0.5，意味着针对每个分类的置信度都很低，虽然softmax后可以得到一个分类结果，但是没有反映出根本的问题。这样的样本，我们定义了一个概念，“可疑样本”。针对“可疑样本“的处理可以放在预测概率空间完成，实际上使用KNN就可以取得很不错的效果，正在考虑要不要整理成文章发表。

和上述第二步的区别在于，第二步专注于neg的挖掘，所以叫做hard negative mining，这里可以叫做hard example mining。另外一点不同，使用了第二步的prob信息，其实prob的内含很丰富，这里的挖掘只是一部分而已。

因此，考虑到处理对象的不同，针对第二步，可以用cls预测pos，得到预测prob<=0.5的所有pos对应的feature和prob，或许可以叫做hard pos mining?

**这里提出一个问题，为啥只对neg做mining？**个人认为，mining的对象可以不同。

**为什么上述方法可以work？**在第一步得到cls之后，由该cls确定的分界面不一定可以将pos和neg刚好分开，重新把neg喂给cls，获得false positive，其实就找到了分错的neg，将这部分neg再喂给cls去train，就是为了纠正分界面的偏移。整体上来看，最终得到的cls实际上是由pos+neg+分错的neg训练得到，分错的neg是neg的一个子集，显然是一个数据增强（上采样），不过这里增强的对象更加的明确。

CVPR2016一篇文章《Training Region-based Object Detectors with Online Hard Example Mining》中提出了一个概念Online Hard Example Mining，讲过上文中hard example mining的一些想法后，这里要关注的就是online了。

回到多分类问题，与prob强相关的是loss了，因此很自然的一个想法是**能不能通过loss判断样本的hard或者easy？**在这篇文章中，用loss找出hard example，bp的时候只回传这些hard example的weight更新。对于分界面的确定，不是所有样本的贡献都是相同的，有的甚至可能成为noise，通过loss来选择，是很合理的想法。

在结构设计上，在Fast R-CNN基础上，将原来的RoI Network变为两个RoI Network，两个Network共享参数，其中一个的输入是image，负责forward操作，用于计算loss，筛hard样本。另一个的输入是hard样本对应的feature(**RoI Pooling Layer**)，负责forward和backward。

**如果在Faster R-CNN基础上使用OHEM呢？**很简单，将非hard样本的loss置为0。但是作者在文章中说，这种方式的优点是直接，缺点是不高效，因为虽然loss为0，但是RoI Network还是要为所有的RoI分配内存，执行反向传播。使用两个RoI网络，只回传hard样本的weight更新。

Online是End-to-End的意思，从实际使用角度来讲，不考虑性能的前提下，个人更加倾向于直接的实现方式，可能一定程度上增加了显存压力，限制超参选择。

总结一下上文的hard和easy选择的两个方式，第一是prob；第二是loss；

针对hard和easy问题，围绕loss的设计，之前写过一篇关于Focal Loss的[博客](https://zhpmatrix.github.io/2017/08/13/focal-loss/)，实际上近一年下来，听到更多的是关于这个Loss不work的消息，不过从理论上讲，设计应该是合理的，将**prob和loss进行了融合**。

loss实际上最终影响的是bp回传时的weight更新，所以，第三个思路是weight。这里涉及的数学问题是loss和loss的导数之间的关系，如果线性相关，可以直接把loss的东西拿到loss的导数上，大多数情况下，应该不是线性的。实际上，这只是这篇博客提出的另一个想法而已，目前还没有看到相关文章，并不意味着没人做。

讨论了这么多，**最重要的问题没有说，什么样本是hard和easy的？**

通过prob或者loss判断不具备足够的说服力，可能需要从数据上来讲这件事儿。比如，不平衡导致某一类样本很hard；某个样本尺度很小，导致检测时很hard；遮挡严重或者光照条件差导致很hard等，这本来就是一个模糊概念。看到一些文章做相关研究，用不同人标记一张图片的平均时间作为是否hard的度量指标，也能讲的通。

**另外一个问题是研究的对象是什么？**

一个image中的一个obj可以是hard的；一个image可以是hard的；一个类也可以是hard的；一个task是hard的等。针对不同的研究对象，可能策略不相同。比如不平衡导致的类是hard的，cls倾向于多类样本，这个时候上述谈到的prob和loss可以适用，但是更多的是用数据增强的方式来做，比如上下采样，合成样本等，当然有一些代价敏感的方式，其实Focal Loss也可以放在这个范围内，可以看到，这种思路已经形成了一个做不平衡学习的社区，可以读之前写过的一篇[博客](https://zhpmatrix.github.io/2017/02/20/learning-from-imbalanced-data/)，关于不平衡学习的综述。

师弟最近在做hard和easy区分的相关工作，期待更多有趣的结论可以分享。


总结(民科味道很浓)：从数据中学习，学什么？难易是数据分布的更高级属性，相对低级的属性包括纹理，形状等，但是捕获属性的阶段不同，前者可以在模型的head处获得；后者可以在backbone处获得。最终通过bp将反馈信号回传。类似的属性，anchor box的aspect ratio和scale，proposal的pos和neg的ratio，IoU等，但是这类属性现在看到是手动设置，启发式的方式在做，好一点的针对anchor box，用聚类的方式处理得到。学习，是否意味着什么都可以学，怎么学？当然，在实现上是End-2-End了。




















