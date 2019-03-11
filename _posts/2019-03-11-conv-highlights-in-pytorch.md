---
layout: post
title: "[PyTorch]CNN系列接口Highlights"
excerpt: "讨论PyTorch中与CNN实现相关的接口，包括Conv层，Pooling层，Normalization层和Dropout层，Padding层。"
date: 2019-03-11 18:43:00
mathjax: true
---

<script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=default"></script>

### Convolution Layers

PyTorch中Conv层，主要包括卷积和反卷积两类，并且实现了两类分别对1d到3d的支持。卷积的作用之一是降维。那么反卷积的作用之一自然是升维了。这里指的一提的是，与之在作用上有点类似的是Vision层，该层主要实现了一些Upsample的方法，如最近邻和双线性插值等方法。Downsample和Upsample在CV领域中的Segmentation任务上，例如Unet系列中是很常见的模块。在讨论参数的时候，以torch.nn.Conv2d为例，具体参数包括：输入和输出通道的数目；卷积核的大小；步长；是否padding；是否有空洞；输入和输出之间是否进行分块连接；是否需要bias；由此接口实现，可以看到空洞卷积已经是标准的一部分了。同时，该接口支持输入通道和输出通道之间的分块连接，这对模型的并行训练非常重要，同时可能支持一些相关Trick的实现。

围绕卷积，在之前的一篇博客中，[CNN中的两个计算问题](https://zhpmatrix.github.io/2018/07/06/Tech-Notes/)，讨论了感受野和输出通道的大小计算的问题。[Rethink系列-CNN/RNN](https://zhpmatrix.github.io/2019/01/27/NLP-rethinking-base-blocks/)，重点讨论了CNN在NLP中应用的理论意义。[啊哈，CNN!](https://zhpmatrix.github.io/2017/06/01/something-about-dl/)，列举了很早时期首次接触CNN时的一些参考资料。[R-CNN](https://zhpmatrix.github.io/2018/05/12/RCNN-Series/)中讨论了一个基于CNN的目标检测模型。

在官方文档中，给出了一个综合考虑上述参数的具体的计算公式(面试/笔试必备，拿出小本本记下来。)。转置卷积参数与上述参数类似。其实转置卷积也是卷积过程。

### Pooling Layers

Pooling层经常讨论的是Max和Avg操作，自然包括1d到3d的支持。但是PyTorch同时实现了一些有意思的支持，包括MaxUnpool，FractionalMaxPool，LPPool，AdaptiveMaxPool四类。MaxPool的结果返回输出结果和对应的位置，找Max的过程是一个离散的操作，记录了位置自然可以做逆向实现了。LPPool是按照LP范式实现的Pooling操作，Max和Avg理论上都可以划分为LPPool中，AdaptiveMaxPool实现的是只关心输出的大小，也就是接口中需要指定的参数，对核的大小，步长等其他参数并不关心，也就是只关心结果而不关心过程的MaxPool。

Fractional Max-Pooling在2014年就提出了，但是似乎并没有得到业界的关注，具体论文可以参看Benjamin Graham
d的[文章](https://arxiv.org/abs/1412.6071)，这里不做过多讨论。

### Normalization Layers

Normalization层目前实现了BatchNorm，InstanceNorm，LayerNorm以及GroupNorm和LocalResponseNorm。关于Normalizaiton，还有一个相对较大的分支，Weight Normalization，一个朋友围绕这块内容做的文章几乎发遍了CV各个顶会。但是直观上看，主流框架在官方实现上并没有关注到这块。

BatchNorm和InstanceNorm的区别可以通过下述两句话来描述：

BN:The mean and standard-deviation are calculated per-dimension over the mini-batches.

IN:The mean and standard-deviation are calculated per-dimension separately for each object in a mini-batch.

LayerNorm在NLP领域应用较广，典型的Transformer的Block中。和BN&IN的区别如下：

LN: The mean and standard-deviation are calculated separately over the last certain number dimensions which have to be of the shape specified.

印象中的LRN是较早时期的工作，但是GN则是2018年比较火的工作，该工作在很大程度上与自己做Weight Normalization的朋友的工作重叠，背后的故事太多，在这里就不展开了。

和Conv层，Pooling层一样，Normalization层同样需要1d到3d的实现。

### Padding Layers

Padding的策略较多，PyTorch中实现了四种策略，适用于不同Nd的Padding操作，包括基于输入边界的reflection，基于输入边界的replication，0填充，常数值填充。

### Dropout Layers

除了实现Nd的Dropout，还实现了AlphaDropout，具体论文可以读[Self-Normalizing Neural Networks](https://arxiv.org/abs/1706.02515)。

上述组件在CNN相关的模型实现中是比较清晰的，比起上述组件或者Layers，激活函数的选择，损失函数的选择和优化器的选择三块内容种类要丰富的多，但这些并不是这篇博客要去梳理的内容。嗯，基本可以愉快地尝试基于PyTorch复现Facebook的[《Convolutional Sequence to Sequence Learning》](https://arxiv.org/abs/1705.03122)了。

在年初，关于Transformer/RNN/CNN的未来发展的讨论持续了好长一段时间，目前来看，Transformer取得了辉煌的成就，但是由于CNN的并行特性和在CV中广泛应用，在NLP中将CNN发扬光大也是众多NLP研究者的希望，同时多数情况下RNN总是我们最稳定的Baseline提供者，同时目前很大一部分工作仍旧是基于RNN的研究成果，非要给出一个结论，排个队，对我而言还是挺难的。



主要参考：

1.[torch.nn](https://pytorch.org/docs/stable/nn.html#)


















