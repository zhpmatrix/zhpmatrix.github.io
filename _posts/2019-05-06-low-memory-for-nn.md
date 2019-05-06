---
layout: post
title: "[NLP]神经网络的Low-Memory技术"
excerpt: "这是一篇技术报告笔记，讨论了训练神经网络时能够减少memory的技术，同时讨论了该技术与模型最终效果的影响。"
date: 2019-05-06 18:43:00
mathjax: true
---

非常新的技术报告，文章如下：

![img-1](http://wx4.sinaimg.cn/mw690/aba7d18bly1g2s03uqyvjj21eo0o0q7d.jpg)

学术界有大量的工作在研究inference时的减少memory的技术，但是较少的工作在研究train时的low-memory技术。这篇技术报告想要讨论的问题是：

**在训练一个神经网络的时候，需要多少的memory？**

讨论了四种策略：

（1）imposing sparsity on the model

（2）using low precision

（3）microbatching

（4）gradient checkpointing

结论：基于WideResNet用于图片分类和DynamicConv Transformer用于机器翻译，组合上述策略，分类任务上内存减少60.7x，准确率减少0.4%；翻译任务上内存减少8.7x，BLEU减少0.15。

**既然要减少train时候的memory，首先要回答memory来自哪里？**

（1）model memory。模型参数。

（2）optimizer memory。优化时的grad和momentum。

（3）activation memory。激活函数值，用于backprop。

在整个train的过程中，除了上述三个大类之外，还有一些附加的memory，例如临时性存储buffer。一般情况下，上述四种策略在减少上述三个方面memory的同时，也可以减少附加的memory。

不同的策略最终会影响到上述三个memory来源，同时对train过程中的浮点计算次数产生影响，具体如下(表格中为空的表示没有显著影响)。

![img0](http://wx4.sinaimg.cn/mw690/aba7d18bly1g2ryo6moiij21oo0cmacb.jpg)

### sparsity

报告中使用**动态稀疏重参数化技术**。

### low precision

报告中使用半精度。传统的浮点计算是32bit的，半精度是16bit，一般认为使用半精度会存在数值收敛相关的问题。

### microbatching

传统的经常用的方法是mini-batching。将一个mini-batching的数据feed给网络，更新参数。microbatching是对一个mini-batching中的数据分成多份，然后顺次feed给网络，当一个mini-batching中的数据feed完之后，累计梯度更新参数。在含有bn层的网络结构中，由于batch大小的选择会影响到bn层的统计特性，因此该方案在减少memory的同时，会对模型最终效果产生影响。

### gradient checkpointing

传统的方式是为了后续backprop的计算，需要保留激活层的所有中间输出。该方法只保留一部分激活函数值，只是在backprop的时候重新计算激活值。由于训练过程是**数值不变**的，因此该方法不对模型的最终效果产生影响。

报告中除了讨论上述四种主要技术之外，在相关工作中讨论了一些工作，如下：

#### sparse neural networks

pruning(and quantizing)神经网络；

sparsity-inducing技术：L0正则化和变分dropout；

但是这类技术关心inference，并不关系train时候的memory cost。为了解决该问题，沿着这个方向，仍旧很多工作。


#### low precision training

训练low-precision网络，只有1bit。

#### small-batch training

在训练过程中varying the minibatch size。

#### gradient checkpointing

2000年提出的该技术，2016年又重新被学术界拿起研究，由于该方法不对模型的最后效果产生影响，因此已经被pytorch等框架实现。结合bn层的特殊性，有工作将该技术和bn层和激活层结合起来。

#### 其他技术

模型蒸馏，low-rank相关技术，空间高效的优化器(adafactor)。

总结：有很多很fancy的工作，但是实际在解决问题的时候还是要做trade off，包括应用相关技术的成本也要考虑在内，在deadline的压力之下，学习成本是不可忽视的代价。来到工业界更是见证了“暴力”的美学特性，大数据，大模型，大计算带来的收益往往会有客观的产出。为了减少“一顿操作猛如虎，一看收益0.5”情况的发生，小心取舍似乎更加重要吧。虽然实际上是这样，但是还是期待更多fancy工作的出现给自己，给社区带来hope。不知道我司同学在翻译模型的压缩上进展如何了？




















