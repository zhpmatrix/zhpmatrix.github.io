---
layout: post
title: "Rethink系列-Transformer"
tags: [NLP]
excerpt: "梳理一下Transformer实现时的一些基础问题。"
date: 2019-03-13 18:43:00
mathjax: true
---

<script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=default"></script>

一.[Rethink系列-CNN/RNN/GRU/LSTM/BiLSTM](https://zhpmatrix.github.io/2019/01/27/NLP-rethinking-base-blocks/)

二.[Rethink系列-Attention](https://zhpmatrix.github.io/2019/01/27/NLP-rethinking-attention/)

三.[Rethink系列-seq2seq](https://zhpmatrix.github.io/2019/01/28/NLP-rethingking-seq2seq/)

四.[Rethink系列-copy和coverage机制](https://zhpmatrix.github.io/2019/01/29/NLP-rethinking-copy-and-coverage/)

五.[Rethink系列-词法/句法/语义](https://zhpmatrix.github.io/2019/01/31/NLP-rethinking-basic-techniques/)

六.[Rethink系列-Transformer](https://zhpmatrix.github.io/2019/03/13/NLP-rethinking-Transformer/)


前言：

在写代码的时候，觉得想法挺多的。但是到写博客的时候又觉得想写的东西其实不多，但是还是将这篇博客发出来，围绕Transformer的工作很多，后续逐渐更新补充一些新的工作吧。

### Self-Attention是怎么提出来的？

RNN系的三个问题：序列模式导致难以并行；长期依赖的问题；对序列位置的建模是线性的；实际上CNN也可以实现类似的功能，并且具有以下几个优点：容易并行化；可以挖掘局部依赖；对序列位置的建模是对数的。CNN具有很多优点，但是对依赖性的建模不是很好。Transformer的提出在性能上优于单纯的CNN的模型，除了CNN模型的优点之外，对依赖性的建模更好。


### Transformer的架构特点是什么？

从Transformer的整体架构上来看，Encoder端包括N层相似的子层，每个子层包括Self-Attention层和前馈网络层。Decoder端也包括N层相似的子层，每个子层包括Self-Attention层和Encoder-Decoder Attention层以及前馈网络层。在Encoder端，每个位置的数据有自己独特的数据流路径。这些路径在Self-Attention层有依赖关系，但是在前馈层是独立的，因此这些路径可以并行地执行。这也是Transformer并行性的来源之一。

### 标签平滑正则化(Label Smoothing Regularization，LSR)

在分类问题中，针对每个训练样本，训练过程中会得到一个该样本是所有类别的预测概率向量。针对该预测概率向量，可以有很多工作来做，比如讨论样本的难易程度等。而LSR认为预测概率向量较大的值，表示模型对于当前样本属于某类的置信度比较高，随着训练过程的进行，该预测值会越来越高，而LSR的目的就是阻止这种趋势的发生。所谓正则化，正是模型对这种行为的惩罚。因为从数值角度来看，这种情况的出现会导致CE损失变得较大，而这并不是我们所希望的。从KL散度的角度也可以给LSR一个合理的解释。具体细节可以读论文[《Rethinking the Inception Architecture for Computer Vision》](https://arxiv.org/pdf/1512.00567.pdf)。

### Positional Encoding

针对一个输入句子，每个位置，每个维度的位置嵌入向量的值是一样的，满足sin和cos函数。之所以选择这两个函数，按照官方论文的意思是可以学习到相对位置的概念。在上文中，开篇就提到对序列位置的建模是一个重要的问题。但是自从Transformer出现之后，工业界很多人都希望有一些更好的对位置编码的方案出现，目前的方案似乎并不是最优的。

### Dropout

在Transformer的实现过程，Dropout无处不在，为了防止模型过拟合，Dropout的使用可以随心所欲。

### 权值矩阵共享

在Transformer中，Encoder和Decoder的Embedding层的权重是共享的，同时在Decoder端的Softmax层前的线性层也和前两个部分共享权重。

### Mask矩阵

Mask矩阵的两个使用场景分别是：处理不定长输入和在LM中防止未来信息的泄露。一般来说，对PAD的符号也需要做Embedding，但是这些PAD的符号本身来说意义不大，那么参与到训练过程中就可能对模型的性能优化有损伤。那么一种解决问题的思路是用标志位表示出哪些位置是PAD的，哪些不是PAD的，通过在梯度反传过程中过滤掉PAD位的信号就OK。还有一个形式上更加漂亮的Mask矩阵就是对角矩阵，该矩阵可以用于语言模型中的Decoder端，防止由于Attention机制的使用导致未来信息的泄露。

### 参数初始化(初始化为0或者初始化为任意随机数)

初始化为0和均匀初始化以及其他各种初始化方式。在PAD后的序列中，PAD位的初始化通过Mask操作后，对损失函数的影响就会被过滤掉。在PyTorch的已经实现的层中，可以看到大部分的初始化都是按照均匀分布初始化，但是PyTorch同时给与了我们选择初始化方式的接口，可以自己定义各种初始化方式。

### 新工作

除了《Attention is all you need》这篇文章，还有Universal Transformer，后续的The evolved transformer,Transformer-XL, Star-Transformer, BERT，GPT-2等工作。相信在后续会有更多的新的工作出现，这篇博客将持续更新。


参考:

1.[How Transformer Work-Model Used by Open AI and DeepMind](https://medium.com/@giacaglia/transformers-141e32e69591)

2.[The Annotated Transformer](http://nlp.seas.harvard.edu/2018/04/03/attention.html)

这篇博客基于PyTorch实现了一个Transformer的版本，除此之外，读这篇博客的代码也可以学习PyTorch实现模型的很多技巧，比如实现一个优化函数，比如如何实现并行化的计算损失函数，比如如何将Transformer模型解耦从而方便实现，比如数据的Batch/Iter化等，关于seq2seq模型的一些核心技术也有实现，比如Greedy Decoding的实现，BPE数据编码，Attention的可视化等。总之，质量非常高，令人受益匪浅的博客。该团队开发了opennmt-py，在该框架中也实现了Transformer。

处理上述技术细节之外，对一个模型了解到什么程度可以做框架级的实现，也算给出了一个答案。也就是这篇博客，也对我们观察模型给出了一个角度。

3.[The Illustrated Transformer](http://jalammar.github.io/illustrated-transformer/)

这篇博客用可视化的方式，通过非常具体的画图方式讲解了Transformer的细节问题。虽然Transformer的原始论文已经写得比较清晰了，但是读了这篇博客，对Transformer的理解又会加深许多。

4.[Mask矩阵在深度学习中有哪些应用场景](https://www.zhihu.com/question/305508138)

5.[Evolution of Natural Language Generation](https://medium.com/sfu-big-data/evolution-of-natural-language-generation-c5d7295d6517)

总结了语言模型的发展历史，前DL时代的语言模型需要从HMM开始讲起，HMM模型只关注当前词的前一个词，没有对上下文建模，自然过度到RNNs，继而现今的Self-Attention模型。



















