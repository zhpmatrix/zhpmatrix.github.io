---
layout: post
title: "[DL]Loss函数设计与优化"
excerpt: "针对我们目前正在做的工作，图片难易程度划分。讨论损失函数从mse到kendall，从kendall到kl散度，再到一些新的想法。"
date: 2018-06-29 14:59:00
mathjax: true
---

题目是真的做不动了，写篇博客，梳理一下最近和马栋梁在讨论的一个工作。师弟的[这篇博客](https://vipermdl.github.io/2018/06/26/Rethinking-mixUp/)总结了前期在数据增强阶段做的工作。这篇博客主要从损失函数设计上讨论后续将要进行的工作。

CVPR 2016有篇文章解决的问题是预测PASCAL VOC的图片的难易程度。作者基于PASCAL VOC，给每张图片的困难度打分，建模为一个回归问题，评价指标是kendall系数。

回顾一下，[衡量随机变量相关性](http://www.cnblogs.com/kemaswill/archive/2012/11/01/2749842.html)的方法主要有三种：pearson相关系数，spearman相关系数和kendall系数。

原始paper中使用的loss函数是mse，在我们的工作中，直接去优化kendall系数，有显著提升。当然更显著的提升来自backbone由VGG改为Resnet了。

正在尝试的一个工作是mse和kendall的联合优化和分阶段优化。前期有些数据增强的方案，例如mixup和up sampling等方式，并不work，设计新loss后，需要重新验证这些数据增强方案。

kendall在做什么呢？看下图。

![kendall](http://wx1.sinaimg.cn/mw690/aba7d18bgy1fss3k8z0uej21kw16oqdn.jpg)

假设黑色是真实值，红色是预测值。针对五个pair，A到E，两两pair作比较，如果当一个pair中的真实值小于另一个pair中的真实值时，预测值也对应小，则记为1；否则记为-1；最后，所有标记求和。

本质上，通过两两比较来确定一个分布。

但是针对kendall，预测分布错误的时候，需要付出代价。例如C和D这个pair，趋势预测错误，需要正确的pair进行补偿。

因此，当作为度量方式时，不考虑补偿应该也是OK的！kenall应用于排序时，看下图，

![kendall2](http://wx4.sinaimg.cn/mw690/aba7d18bgy1fss3ysop3bj21kw23u78s.jpg)

上图的kendall系数值要小于下图。直观上看，下图显然是更好的分布，确定的序列完全和真实值分布相同。

直观讨论完kendall，想一下和KL之间的关系？沿着上述的思路，能不能只单单考虑对应位置的预测值和真实值之间的关系呢？相比于直接优化kendall，这个想法更加的tight。

比大小，不一定只能用减法，也可以用除法，当然取个log之后，二者就等价了。

考虑到KL散度的计算，假设q是真实值，p是预测值，KL的计算是sum(plog(p/q))，当p=q时，KL值为0，完美预测；

在图片困难问题中，p和q的差距不能太大；p也可以直接去掉，毕竟不是使用KL损失；考虑到log值的正负性，可以添加绝对值，这样，得到一个损失函数是类凸的！

    损失函数最优值处，可以得到kendall最优；但是反之不成立；

我们优化一个更tight的问题，获得一个relax条件下的度量指标。

另外的一个想法是，直接使用KL损失函数，用softmax做归一化，得到合理的p和q值。

总结：这篇博客从直接优化kendall系数出发，提出两种新的建立损失函数的想法。上述想法，从问题出发，从KL损失函数中得到一些启发。虽然不是最适合KL损失函数的应用场景，但是从数值角度上分析，应该是work的。

参考：

1.[概率中的PDF, PMF, CDF](https://blog.csdn.net/wzgbm/article/details/51680540)

为什么需要分布函数？计算连续性随机变量的概率。

2.[Kullback-Leibler Divergence Explained](https://www.countbayesie.com/blog/2017/5/9/kullback-leibler-divergence-explained)

一篇有趣的博客介绍KL散度。

3.[PyTorch中提供的与交叉熵有关的损失函数](https://cloud.tencent.com/developer/article/1126921)

torch.nn.CrossEntropyLoss, torch.nn.KLDivLoss, torch.nn.BCELoss, torch.nn.BCEWithLogitsLoss, torch.nn.MultiLabelSoftMarginLoss

4.[PyTorch中的所有损失函数总结](http://yangli.name/2017/12/25/20171225pytorch2/)

[官方Doc对KLDivLoss的定义](https://pytorch.org/docs/stable/nn.html?highlight=torch%20nn%20kl#torch.nn.KLDivLoss)

5.[非负矩阵分解中的KL散度](https://www.cnblogs.com/xingshansi/p/6672908.html)

建立了非负矩阵分解和KL散度的关系，Taylor近似，泊松分布。重点提示，文中推导出的KL散度的计算和PyTorch中不同，原因未知。

6.[KL散度在推荐系统中的应用](http://chuansong.me/n/2759305)

讨论某个专辑被哪个年龄段的人喜欢，简单讲，需要考虑年龄的分布。
























