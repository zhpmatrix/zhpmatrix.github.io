---
layout: post
title: "Rethink系列-CNN/RNN"
tags: [NLP]
excerpt: "对CNN在NLP中应用的方法，缺点，优点及其目前发展形势做的小思考。"
date: 2019-01-27 18:00:00
mathjax: true
---

一.[Rethink系列-CNN/RNN/GRU/LSTM/BiLSTM](https://zhpmatrix.github.io/2019/01/27/NLP-rethinking-base-blocks/)

二.[Rethink系列-Attention](https://zhpmatrix.github.io/2019/01/27/NLP-rethinking-attention/)

三.[Rethink系列-seq2seq](https://zhpmatrix.github.io/2019/01/28/NLP-rethingking-seq2seq/)

四.[Rethink系列-copy和coverage机制](https://zhpmatrix.github.io/2019/01/29/NLP-rethinking-copy-and-coverage/)

五.[Rethink系列-词法/句法/语义](https://zhpmatrix.github.io/2019/01/31/NLP-rethinking-basic-techniques/)

六.[Rethink系列-Transformer](https://zhpmatrix.github.io/2019/03/13/NLP-rethinking-Transformer/)

沿着DL的路线，目前为止，解决NLP问题的主要方式包括CNN，RNN和Attention三种。这里的R是循环的意思而非递归，虽然递归神经网络(RNN)在NLP领域也有重要用途，但是从近期相关文献来看，关注度并不高，因此本文并不准备讨论相关问题。传统观点认为RNN天然适合处理序列结构，因此，在相当长的一段NLP历史时期，研究的焦点都在RNN，因此也有部分不严格的观点认为"做NLP的同学就是搞RNN的"。虽然也存在"做CV的同学就是搞CNN的"的逻辑，但是RNN和CNN的应用并非只能限制在特定领域，RNN可以用在CV领域，同理CNN也可以用在NLP领域。除二者之外，Attention近年来已经成为了一个明星，以Transformer为代表模型，以致于有些人会去讨论"Transformer能否替代RNN在NLP领域中的地位？"这样的问题。

### 1.CNN

围绕CNN为啥有效的讨论，已经有太多的观点。其中，局部不变性和可组合性尤为重要。在CNN中，通过卷积和Pooling(_平移，旋转，伸缩三种不变性_)实现局部不变性，通过网络的层次结构实现可组合性。

所谓局部不变性，除了Pooling带来的三种不变性之外，利用卷积对图片进行特征提取，也会引入局部不变性。比如，对图片中的物体进行分类，CNN并不关心图片中物体的具体位置。

所谓可组合性，是指利用网络的层次结构，通过组合网络低层的低水平特征，实现网络高层的高水平的表示。比如，CNN可以按照从网络低层到网络高层的顺序，逐渐从像素，依次获取边缘，形状，物体等表示。

那么，如何将CNN用于NLP中呢？这可能是最重要的问题了。从费曼的第一性原理出发，可以这样思考。

第一，限定场景下的直观类比。图片分类中，可以用一个二维结构(卷积核)去卷积另外一个更大的二维结构(图像表示)，句子分类中是否也有这样的场景呢？显然，当使用Embedding向量去表示一个句子的时候，就获得了大的二维结构(句子表示)，这样就可以直接使用CNN来做句子分类了。且不管效果怎样，此时已经可以写代码来验证想法了，而且成本并不高。由此可以看出，Embedding不仅是NLP中的核心，同时也可以通过Embedding作为CNN在NLP和CV之间的桥梁。Embedding有许多美丽的故事可讲，但是目前并不准备来讲述。个人观点认为，在DL刚开始统治CV和NLP等领域时，也正是技术的蛮荒年代，类似这样的想法就很有可能带来一些顶会文章。


第二，理论可行性。所谓理论指导实践，理论上是否可行？这里的理论主要讨论上文中已经讨论到的局部不变性和可组合性。图片分类中的卷积是对相邻像素进行操作，相邻像素具有语义相关性是图片分类的重要特性。因此，CNN中的卷积应当对句子中的相邻词(词向量)或者相邻字符(字符向量)进行操作，这样，卷积核的大小就有一些条件需要满足。比如宽度等于词/字符向量的长度。这样唯一可以改变的就是卷积核的高度了，不同的高度对应不同的n-gram特征。这里的讨论是上文中谈到的直接用于CNN做句子分类的优化改进了。

局部不变性和可组合性暂时并不能同CNN在CV中的应用严格对应，但是或许可以找到一些特例来直观的感受。比如，情感分类中，通过Pooling操作过滤掉一些词或者字符并不影响最终情感属性的判断。可组合性的理解似乎更加困难，需要对CNN每层学到的特征有所了解后，才能合理解释。

这里存在的一个问题是，什么是一个句子的低水平特征和高水平表示？通常认为Embedding后的结果作为句子的表示，放在CNN的框架下，这个是一个句子的原始表示，那么由此能否按照CV中图片分类的理解得到低水平特征和高水平特征呢？如果不能，是否有更良好的Embedding方式，或者句子表示的方式能够很好的用可组合性的理论来解释学习到的特征？

第三，技术可行性。假设卷积特征和n-gram特征的对应关系成立，则卷积特征具有明显的优势。便于GPU加速实现，具有一定的理论合理性，CV中基于CNN得到的一些理论结果有较大的可能迁移到NLP领域中CNN的应用。

虽然理论上稍有牵强，但是技术上的吸引力使得CNN在NLP中也能够被接纳。实际上，围绕CNN在NLP领域中的应用很广泛，在多个任务中都取得了不错的效果，CNN在NLP领域中的小迷弟并不少呢。个人更加希望围绕CNN的在NLP领域中的应用有更多的研究成果出现，但是目前来看，CNN的发展似乎并不及LSTM系列和Attention系列，不过CNN应该是很有吸引力的模型。

这部分用较少的文字主要讨论了CNN在NLP中应用的方法，缺点，优点及其目前发展形势。CNN在具体任务中的应用，模型改进，优化调整等并不是Rethinking系列需要关注的地方。能够大致想到的是，将CNN用于NLP，第一可以尝试将CV中的研究成果直接迁移过来，然后结合具体任务做调整，所谓具体问题具体分析。第二是结合NLP本身的特点做因地制宜的改进，所谓CNN的NLP化。第三，CNN在NLP领域的运用超过CV领域的发展，成为"做NLP的同学就是搞CNN的"。


### 2.RNN/GRU/LSTM/BiLSTM

_由于这部分很多人讨论过，等我考虑到有趣的东西时再来完善吧。_

本节参考文献：

1.[Understanding Convolutional Neural Networks for NLP](http://www.wildml.com/2015/11/understanding-convolutional-neural-networks-for-nlp/)

2.[Understanding LSTM Networks](http://colah.github.io/posts/2015-08-Understanding-LSTMs/)



















