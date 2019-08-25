---
layout: post
title: "[OpenNMT]OpenNMT核心类设计"
excerpt: "梳理了OpenNMT源码在关键类上的设计，具体包括框架类，数据类，模型类和服务类。"
date: 2019-08-25 15:48:00
mathjax: true
---

整体上看，OpenNMT-py在框架上的设计抽象是比较清楚的，本篇博客主要梳理一下相关的类。目的有两个：第一是进一步熟悉OpenNMT整体上的设计；第二是为后续OpenNMT的扩展做一些准备，方便自己在该框架体系下实现一些想法。

最近和组里同学聊关于框架使用的问题。有的人倾向于不用框架，但是难免从框架中复用一些常用的模块代码，目的是为了最大程度上的灵活性。但是，个人认为源码面前没有秘密，使用框架并不意味着灵活性的丧失，因为灵活性需要从源码中寻找，体现在类设计上，好的框架抽象上。

在之前关于OpenNMT-py源码的博客包括如下：

1.[tensor2tensor源码阅读](https://zhpmatrix.github.io/2019/04/23/tensor2tensor/)

2.[OpenNMT中Attention相关参数](https://zhpmatrix.github.io/2019/02/01/opennmt-attention-params/)

3.[预处理模块源码剖析](https://zhpmatrix.github.io/2018/12/17/opennmt-source-code-reading-0/)

4.[训练模块源码剖析](https://zhpmatrix.github.io/2018/12/17/opennmt-source-code-reading-1/)

#### 第一：framework层的四个核心类分别是model，trainer，loss和optimizer相关。

onmt.models.NMTModel(encoder, decoder)

>继承自torch.nn.modules，是seq2seq的统一接口，包括encoder和decoder。在forward操作时，输入src，tgt，lengths，返回decoder的output，同时返回attention的结果，类型为[tgt\_len，batch，src\_len]。

onmt.Trainer: 

>用于整个训练过程控制的类。onmt.utils.Statistics用于计算与Trainer相关的统计量。


onmt.utils.loss.LossComputeBase:

>继承自torch.nn.modules，用于损失计算的策略类。

onmt.utils.Optimizer:

>用于优化的控制类。多数时候是对optim的薄薄的一层封装。可以通过继承该类实现grad accu。

#### 第二：DataLoader相关的类。

>onmt.inputters.DataReaderBase是数据读取的基类，onmt.inputters.TextDataReader/ImageDataReader/AudioDataReader分别实现文本，图片和声音的读取。

onmt.inputters.Dataset

>继承自torchtext.data.dataset.Dataset，实现从raw数据到tensor数据，最后batch化的工作。在google-bert，pytorch-transformer等框架的实现都可以看到类似的封装，是一个标准过程。

#### 第三：基础模块类

onmt.modules.Embeddings: 同样支持对语言学特征的输入embedding。这对手动添加额外的feature提供了灵活的实现。

onmt.encoders.EncoderBase/MeanEncoder/RNNEncoder/：encoder类

onmt.decoders.DecoderBase/StdRNNDecoder/InputFeedRNNDecoder： decoder类

onmt.modules.AverageAttention/GlobalAttention/: attention相关

onmt.modules.PositionalEncoding等：具体与Transformer实现相关的类。除此之外，还有与Conv2Conv和SRU实现相关的类。

onmt.encoders.AudioEncoder/ImageEncoder: 其他模态的编码。

onmt.modules.CopyGenerator/structured\_attention.MatrixTree: 特殊attention的相关实现。其中前者正是pointer generator networks的一个实现。


#### 第四：翻译类

onmt.translate.Translator：用saved模型来翻译一个batch的句子。

onmt.translate.DecodeStrategy：生成策略的基类。

onmt.translate.BeamSearch: beam search相关的类。

onmt.translate.RandomSampling：生成时的随机采样相关。

onmt.translate.penalties.PenaltyBuilder: 返回beam search的长度(length)和覆盖(coverage)惩罚。

onmt.translate.GNMTGlobalScorer： 用于nmt任务的re-ranking。

#### 第五：server相关的类

用于模型inference的相关逻辑，包括input端的前处理和后处理等。这块逻辑通常由各个团队的内部serving平台完成。可能是考虑到框架的完整性，实现了一个简易版的功能。


总结：简单梳理了框架类，数据类，模型类和服务类的设计。