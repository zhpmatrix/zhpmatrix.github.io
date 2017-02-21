---
layout: post
title: "[ML]模型选择"
excerpt: "偶然间看到余凯在某次工业界报告中谈到误差，就想写点关于模型选择，偏差方差均衡，交叉验证之类的东西。"
date: 2016-12-05 11:11:00
mathjax: true
---
<script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=default"></script>

余凯在《"AI Inside"无处不在的未来》报告中谈到：

                            G = A + E + O

其中

**G**：Generalization Error即泛化误差。

**A**： Approximation Error即近似误差。误差来源是模型假设不完美，解决方法：更好的模型。

**E**： Estimation Error即估计误差。误差来源是数据不完美，解决方法：更多的数据。

**O**： Optimization Error即优化误差。误差来源是计算资源不完美，解决方法：更好的算法。

考虑误差与模型之间的关系(_图片来源《ESL》_)：

![Bias&Variance](http://ww3.sinaimg.cn/mw690/aba7d18bgw1faguvucn98j20hk0db41m.jpg)

随着模型复杂度的增加，训练误差(red line)逐渐减小，测试误差(blue line)逐渐减小到一个值之后又逐渐增加（_Breiman的Random Forest没有增加过程_）。换种方式来说，训练过程是偏差逐渐减小的过程，测试过程方差变化先减小后增大的过程。

NIPS 2016上，Andrew Ng水笔白板作报告，又一次谈了他的bias和variance均衡，此处自行脑补bias和variance两条曲线随着模型复杂度变化的X型，通常来说，最佳的模型复杂度在两条曲线的交叉点处取得。模型复杂度太高，导致overfitting，产生variance，训练误差远小于交叉验证误差，也就是上图中右侧的高方差和低偏差的表示（训练误差和交叉验证误差的值相差较多）。反之，较低的模型复杂度，导致underfitting，产生bias，也就是上图右侧的高偏差和低方差的表示(但是训练误差和交叉验证误差的值是接近的)。此外，对于cost function中的正则项系数，系数太小，导致overfitting，反之太大，导致underfitting。至于**训练样本和两类误差的关系**，Ng是这样表述的，underfitting导致的high bias问题，增加训练样本数目不管用！为啥呢？设想你选择了一个不合适的模型。overfitting导致的high variance问题，增加训练样本数目，使得训练误差和交叉验证误差之间的gap变小，从而有助于性能提高。所以，不是所有的问题都可以用**更多的数据**来解决。

此处不合时宜的谈谈二者均衡对我们的指导操作。

* 更多的数据，解决高方差
* 更小的特征集，解决高方差
* 更多的特征(例如：多用多项式特征)，解决高偏差
* 降低正则系数，解决高偏差
* 增加正则系数，解决高方差

因此，更好的模型要满足有一个合适的模型复杂度。如何选择？

关于选择策略通常有两个，分别是**经验风险最小化**和**结构风险最小化**。前者的具体实施是特定应用情景下的误差函数，基于前者提出的模型如极大似然估计，通常来说，数据越多，效果越好。但是数据较少的情况下，容易出现过拟合，因为模型复杂度过高。为了防止过拟合，提出了结构风险最小化策略，具体实施是正则化。正则化的作用就是选择经验风险和结构风险都尽量小的模型。于是常常看到：

        目标函数 = 误差函数 + 正则化项

上述是从目标函数的角度出发进行模型选择，能否从数据角度出发呢？

当然！经典的方法是交叉验证。通常来说，利用这种方法选择出的泛化能力强的模型，经验风险和模型复杂度同时较小。一般来说，折数为5或者10。回顾交叉验证的过程之后，考虑下交叉验证的目的：

*1.* 从有限的训练数据中获取尽可能多的有效信息。

从工业界的竞赛来看，通常拿到数据之后，将数据分成两个部分，训练集和验证集。简单的做法是利用训练集训练数据，调整参数。验证集用来进行测试（预测），得到一个模型评分。在有限数据情况下，模型并没有从验证集中学习有效信息，因此，利用"交叉"的想法，利用上验证集的数据就显得很重要。

*2.* 从多个方向训练模型，有效避免陷入局部最小值。

一种可能的情况是训练数据满足某种分布，串行训练也即按照分布方向进行的训练。显然交叉之后，会得到不同的分布进而按照多方向训练模型。在[编程复盘](https://zhpmatrix.github.io/2016/12/04/coding-tricks/)中提到的Shuffle操作有同样的意味。其实交叉也是一种Sampling，涉及到采样分布（统计量是样本的函数）的问题。

*3.* 一定程度上避免过拟合。

交叉训练过程中，利用分开的训练集训练模型，利用验证集测试模型，选择预测评分较高的模型。

常见的三种验证方式：HoldOut验证(无交叉，工业竞赛用)，K-fold交叉验证（此乃正法），留一法(K-fold的特殊形式)。

代码时刻终于来了(sklearn中的交叉验证)！

<script src="https://gist.github.com/zhpmatrix/0858ea5a4ba3182597938ead60d49174.js"></script>

几点说明：

1.通常采用的是K-fold交叉验证方式，必要的时候可以HoldOut。

2.HoldOut中的scoring是‘accuracy’,可以读源代码。

3.cross_val_score中的[scoring](http://scikit-learn.org/stable/modules/model_evaluation.html#scoring-parameter)可选参数众多，**scoring是用来定义模型评估准则的**，比如scoring='accuracy'是target预测值和真实值的差度量。具体如下：

[**'accuracy'**, 'adjusted_rand_score', 'average_precision', **'f1'**, 'f1_macro', 'f1_micro', 'f1_samples', 'f1_weighted', **'log_loss'**, **'mean_absolute_error'**, **'mean_squared_error'**, 'median_absolute_error', 'precision', 'precision_macro', 'precision_micro', 'precision_samples', 'precision_weighted', 'r2', **'recall'**, 'recall_macro', 'recall_micro', 'recall_samples', 'recall_weighted', **'roc_auc'**]

在利用交叉验证进行参数选择的时候，结合Ng所谈到的问题，我们只要关心交叉验证误差最小时对应的模型就好，当然，GridSearchCV也是模型参数选择一种合适的方式。

总结：文章从误差谈到模型选择到风险，最终回到正则化和交叉验证的讨论。当然，最爱的还是Coding，文末给出了sklearn中的交叉验证两种方式，可以直接用在工业级数据竞赛。





