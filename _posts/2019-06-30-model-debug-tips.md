---
layout: post
title: "[NLP]模型实现中的Debug问题"
excerpt: "Troubleshooting Deep Neural Networks-A Field Guide to Fixing Your Model》的tutorial笔记"
date: 2019-06-30 18:43:00
mathjax: true
---

最近读到《Troubleshooting Deep Neural Networks-A Field Guide to Fixing Your Model》，和很久之前读过的AllenNLP写的关于NLP模型实现的tutorial一样接地气。

这是一篇笔记，建议直接品尝原稿，味道更加鲜美。

**时间分配**上，在得到一个可用的模型之前，我们80%-90%的时间都在debugging和tuning，只有10%-20%左右的时间在推导数学和实现（自己在基于Pytorch的模型实现中，80%的时间会花在forward中的复杂tensor操作）。

**为啥深度模型的troubleshooting是困难的？**主要来自三个方面：

（1）实现bug。

（2）超参选择。

（3）数据问题。具体包括：没有足够的数据，类别不平衡，标签噪音，不满足i.i.d条件等。

从自己身边的一些同学来看，多数情况下更加关注（2）而非（1），而（3）是一个通常看起来似乎很明显的事情，但是一旦问题出在（3），实际上很难意识到。特别是在一个pipeline系统中，某些数据错了，但是pipeline仍旧可以流通，直到影响到最终的模型性能。

**那么如何解决呢？**

在troubleshooting之前，作者假设我们已经具备了：

（1）测试集。

（2）评测指标。

（3）目标性能：可以来自human-level， 已经出版的论文和先前的baseline。

实际上，在解决真实场景问题中，**如何得到一个好的测试集？**都可能成为一个问题，很多时候我们没有足够的数据，特别是在domain限定场景下。同样地，不是所有的分类任务都用相同的F1指标。非公开数据集的目标性能的获取，也可能是一个大的问题。这些问题在自己最近的神经关系抽取任务中都遇到了。

假设上述条件满足，作者建议的一个流程是：

（1）选择一个简单的模型。如下图：

![img1](http://wx3.sinaimg.cn/mw690/aba7d18bgy1g4ja4hs30tj21he0lead8.jpg)

（2）使用通常被大家接受的默认参数。比如，优化器的选择，初始化方式的选择等。

（3）正则化输入。

（4）简化问题。具体包括：开始时使用小的训练集等。（在神经关系抽取任务中，首先尝试解决的问题时单句两个实体的情况，逐步扩展到单句多实体，多句两个实体，多句多实体场景下。），比如在一个图片分类任务中，流程如下：

![img2](http://wx2.sinaimg.cn/mw690/aba7d18bgy1g4ja81enxoj20xw0ou42k.jpg)

好了，已经足够简单了，可以开始实现一个bug-free的model了。具体怎么做呢？

（1）先让你的model跑起来。

（2）overfitting一个batch。（这个要求在多个相关tutorial和书中都有提到过，不能overfitting的model都不是好model。）

（3）和已知的结果比较。

一切就绪，在让model跑起来的过程中，出现bug了！来看看作者总结的bug排行榜。

![img3](http://wx4.sinaimg.cn/mw690/aba7d18bgy1g4jadehj5uj21ik0q2wji.jpg)

除此之外，相必数据类型不一致(torch.Long和torch.float)，OOM等也是常见的问题吧。关于OOM的成因，作者总结如下(作者是基于tf给的建议，pytorch粉可以自行对照反思)：

![img4](http://wx4.sinaimg.cn/mw690/aba7d18bgy1g4janxivzzj21gy0oatdv.jpg)

我想说，这些bug的确是我基本上都遇到过。为了减少bug的产生，作者给出的建议如下：

（1）轻量级的实现。不要一开始就搞一个复杂的pipeline，写dataloader，写metric，写logging等，跑起来最关键。

（2）使用第三方组件。如使用第三方的crf层，tf.losses.cross\_entropy的实现等。（我自己通常基于pytorch实现模型，在metric部分一般使用sklearn提供的metric实现）

假设模型已经跑起来，那就可以尝试去overfit一个batch了。额，又会出现一些问题。如下，

![img5](http://wx3.sinaimg.cn/mw690/aba7d18bgy1g4jasbo8cjj21hw0o0dlj.jpg)

假设已经可以overfit一个batch，最后总要check下模型的效果，和已知结果进行对比。那么，从哪里得到一个已知结果就是一个重要的问题了。

![img6](http://wx2.sinaimg.cn/mw690/aba7d18bgy1g4javbm6e7j21c00ry436.jpg)


那么，自然多数人会比较关心的tuning。通过bias-variance的tradeoff过程，我们会遇到一些列问题，那么解决的优先级如下：

（1）解决欠拟合。

![img7](http://wx3.sinaimg.cn/mw690/aba7d18bgy1g4jb3ffanyj21gk0pctd3.jpg)

（2）解决过拟合。

![img8](http://wx3.sinaimg.cn/mw690/aba7d18bgy1g4jb3ilysjj21gu0r6aeo.jpg)

（3）解决distribution shift。

![img9](http://wx4.sinaimg.cn/mw690/aba7d18bgy1g4jb3lrd5cj21cc0mc0wd.jpg)

（4）解决数据不平衡。

总结：从个人的经历来看，作者总结还是非常接地气的，当然有一些自己目前并不能完全认同的做法，在后期的实践中会更多地思考。























