---
layout: post
title: "[OpenNMT]OpenNMT中Attention相关参数"
excerpt: "对opennmt-py中的train模块与attention相关的参数进行了解释和梳理，官方文档确实写的比较落后。部分参数可能需要回到代码中，或者issues区才能理解。"
date: 2019-02-01 18:43:00
mathjax: true
---

在之前的博客中写过两篇关于opennmt-py的源码解析，实际上tensor2tensor的源码写的也是很好，虽然两者开发团队不同，但是功能交集很多。虽然二者的发展起始点不同，但是殊途同归，为大家提供了很好的开源工具。这篇博客重点关注opennmt-py中实现的与attention相关的参数，这些配置项在seq2seq任务中一般来说比较有用。


### global\_attention

该参数指明使用的三种基本的attention类型，包括Bahdanau的mlp和Luong的dotprod和general。

### copy\_attn

Attention相关参数中最重要的参数。该机制是基于NIPS2015的文章《Pointer Network》实现的，它可以帮助模型从source中copy词汇作为target的词汇。当使用该机制时，在预处理阶段，需要给preprocess.py传递参数dynamic\_dict和share\_vocab，目的是使source端和target端使用相同的词典。

此外，当encoder端和decoder端共享word embedding的时候，也需要source端和target端使用相同的词典。但是，opennmt-py的官网文档说了这么一句话：

This option drastically decreases the number of parameters a model has to learn. We did not find this option to helpful,but you can try it out by adding it to the command below.


这里值得一提的是，preprocess.py中注意参数src(tgt)\_seq\_length和src(tgt)\_seq\_length\_trunc的大小设置。其中，前者是指最大序列长度，后者是截断序列长度。同时前者具有默认值50，后者没有默认值。这两个参数的设置要结合自己的数据集，在["默克杯"](https://github.com/zhpmatrix/Retrosynthetic-Reaction-Prediction)的比赛中，明显采用默认值会使得效果打折扣。

### reuse\_copy\_attn

这个参数使用standard attention作为copy attention，也就是文献1中的方法，在[Rethink系列-copy和coverage机制](https://zhpmatrix.github.io/2019/01/29/NLP-rethinking-copy-and-coverage/)中的描述正是standard attention。如果不使用该参数，模型则会单独为copy机制学习一个attention分布，增加了待学习的参数数量。

该参数的使用通常配合copy\_attn，在官网的示例文档中，给出了两个例子都是配合使用。encoder\_type和decoder\_type采用transformer时，没有reuse\_copy\_attn。按照原始论文，transformer自身是一个完整的encoder-decoder模型，opennmt-py中的encoder\_type和decoder\_type设置为transformer可能会造成一定的误解，这里应该分别对应原始transformer的encoder端和decoder端。

### copy\_loss\_by\_seqlength

损失函数是否要除序列长度。其实是一个长度的正则化，一般而言，在推断时有助于产生更长的生成序列。为了达到这一目标，在解码时添加惩罚项也可以实现。在tensor2tensor中，解码的时候通过控制解码参数alpha的值，配合beam\_size的设置，可以灵活的控制生成序列的长度，从而提高生成效果。opennmt-py在推断的时候，提供了多种惩罚机制。包括对coverage的惩罚，对长度的惩罚，对ngram重复的惩罚等。


### coverage\_attn

基于attention机制的coverage机制，在机器翻译领域，有助于解决过翻译和欠翻译问题。

### copy\_attn\_force

这个参数的解释，只有一句话："When available, train to copy"。具体的解释可以从[issue](
https://github.com/OpenNMT/OpenNMT-py/issues/628)中得到，有：

From my reading of the code in CopyGenerator.py, I see that in -copy_attn_force, you have copy probabilities of source tokens and gen probabilities of non-copied tokens. Without -copy_attn_force, you have copy probabilities of source tokens and gen probabilities of non-unk target tokens. As to your second question, Gu, Jiatao, et al. "Incorporating copying mechanism in sequence-to-sequence learning." uses separate copy layer. If that is a better idea has to be empirically verified.

[这里是一个使用案例](https://github.com/Henry-E/opennmt-gen/blob/master/train_gen.sh)。

_从这个示例可以看出，opennmt-py的官网文档更新的有些落后，有些参数的使用还是需要读源码。_

### lambda\_coverage

该参数是一个数值，最终损失函数中，coverage\_loss前的参数值，默认为值为1。通过调节该参数，可以控制最终的生成效果。

### self\_attn\_type

Transformer的decoder层使用的attention类型，有两个选择，分别是点积(scaled-dot)和平均(average)。

### generator\_function

有两个选择，分别是softmax和sparsemax，具体参考文献3。

除此之外，还有几个与Transformer相关的参数设置。

从整体上看，opennmt-py在train的时候，与attention有关的参数设置分为基本attention机制设置，copy相关设置，coverage机制设置，transformer相关设置(self-attention)等，这样思路上就清楚了。这里值得说明的是，虽然opennmt-py实现了这些相关技术，但是从issues的讨论来看，相关技术的有效性需要不断地在实践中检验以形成经验。

引用王垠的一段话，共勉。

_"什么是洞察力？洞察力就是透过现象看到本质的能力。有洞察力的人很容易得到经验，然而有经验的人却不一定有洞察力。再愚钝的人，总是可以通过大量的时间获取经验，然而就算你花再多的时间和精力，也难以得到洞察力。所以洞察力是比经验宝贵很多的东西。很难说清楚如何才能有洞察力，也很少有人会告诉你如何去得到它。当然，我也不会告诉你。"_

希望多点洞察力，少点经验。多点理论指导实践，少点炼金乱炖。



参考文献

1.《Get To The Point: Summarization with Pointer-Generator Networks》

2.《Incorporating copying mechanism in sequence-to-sequence learning》

3.[《From Softmax to Sparsemax: A Sparse Model of Attention and Multi-Label Classification》](https://arxiv.org/pdf/1602.02068.pdf)

4.[Softmax vs. Softmax-Loss: Numerical Stability](http://freemind.pluskid.org/machine-learning/softmax-vs-softmax-loss-numerical-stability/)

5.[opennmt-py中的train模块参数列表](http://opennmt.net/OpenNMT-py/options/train.html)











