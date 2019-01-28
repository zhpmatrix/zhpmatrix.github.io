---
layout: post
title: "[NLP]Rethink系列-Attention"
excerpt: "回顾了Bahdanau和Luong的工作，讨论了围绕self-attention的一点想法，重新思考了Transformer/BERT。"
date: 2019-01-27 18:00:00
mathjax: true
---

一.[Rethink系列-CNN/RNN/GRU/LSTM/BiLSTM](https://zhpmatrix.github.io/2019/01/27/NLP-rethinking-base-blocks/)

二.Rethink系列-Attention

三.[Rethink系列-seq2seq](https://zhpmatrix.github.io/2019/01/28/NLP-rethingking-seq2seq/)


沿着DL的路线，目前为止，解决NLP问题的主要方式包括CNN，RNN和Attention三种。其中，Attention近年来已经成为了一个明星，以Transformer为代表模型，以致于有些人会去讨论"Transformer能否替代RNN在NLP领域中的地位？"这样的问题。

既Transformer之后，2018年年末BERT如一声惊雷炸出了2019年NLP的春天，个人认为是2018年最值得铭记的NLP历史事件。围绕Attention的讨论同样很久前就开始于CV和NLP领域，故事很多需要单开一篇博客讨论Attention。

讨论这个问题之前，限定一种场景，seq2seq。围绕seq2seq的讨论将在另外的博客中单独成文，这里简述一下。比如机器翻译的任务，可以用seq2seq的思路来做，也就是encoder-decoder的框架。在推断的时候，encoder将输入序列进行编码，得到一个中间表示向量，decoder利用这个中间表示向量解码得到输出序列(_此处描述很不清晰，不过不会影响下文的理解，将在seq2seq的博客中具体讨论多种解码方式_)。

这里隐藏的一个大问题是：encoder将所有长度的序列都压缩为一个中间表示向量。对比较短的输入序列，当输入序列较长的时候，由于中间表示向量形式固定，因此会造成较长序列的信息损失。

(_中间表示向量的大小和长度共同决定输入序列的信息表示，在多数时候，这个中间表示向量长度固定，大小可以通过学习的方式得到。因此有些文献在描述这个大问题时，强调是中间表示向量的长度固定，这里采用形式固定描述。_)


于是，2014年Bahdanau带着Attention站出来说，我来试一试？他写道：

_we conjecture that the use of a fixed-length vector is a bottleneck in improving the performance of this basic encoder–decoder architecture, and propose to extend this by allowing a model to automatically (soft-)search
for parts of a source sentence that are relevant to predicting a target word, without having to form these parts as a hard segment explicitly._ 

改造前：decoder端的每一个输出Output(i)=f(中间表示向量C，Output(i-1)，HiddenState(i-1))，为了方便后续说明，用C来表示上文中提到的中间表示向量，此处的下标是精华。

改造后：decoder端的每一个输出Output(i)=f(中间表示向量C(i)，Output(i-1)，HiddenState(i-1))

对比改造前后，在解码时，使用的中间表示向量不同，改造前使用固定的中间表示向量，改造后每个时刻i的解码输入中，中间表示向量都不同，用C(i)表示。C(i)是输入序列HiddenState层的加权和。

最重要的问题来了，这个权值哪里来的？

看C(i)的表达式，输入序列HiddenState层是固定的，那么变化量一定出现在解码端的第i个时刻了。由于输入序列与每个时刻i的输出最相关的部分(HiddenState)都不一定相同，因此有了C(i)的存在必要性。

权值也就是相关性的一个度量手段，在Bahdanau[文献1]和Luong[文献2]的文章中都有讨论，剩下的内容就不是这里要关注的了。

这里头脑风暴一下。对于LSTM而言，CellState似乎一直没有被使用过。HiddenState是序列中每一个时间步对象的表示，被充分的挖掘。原始的encoder-decoder架构，将整个句子压缩为一个中间表示用于解码，而现在利用相关性，重新构造带有时刻差异性的中间表示，提升seq2seq的效果。可以不严格的认为前者是句子粒度的，后者是句子中对应单元粒度的(词，字符)。

另一方面，虽然可以通过相关性计算重新构造上下文向量，无论句子有多长，总可以针对每个输入句子构造每个时刻的权值，作为注意力分数，从而构造一个上下文向量。但是退一步思考，相关性的计算是基于HiddenState的，RNN系列存在梯度消失和爆炸的问题，过长的序列可能导致得到的HiddenState质量不佳，这样即使有上文中Attention机制的引入，似乎仍然不能有效解决问题。

所以，如果基于RNN系列做研究，梯度消失和爆炸是个避免不开的问题，Attention机制只是表面上看起来能够处理句子长程的问题，但是并没有直抵问题根源。

看过Bahdanau和Luong的工作，可以建立对Attention的基本印象。目前很多开源的seq2seq的库实现的Attention基本都包括两位的工作。围绕Attention，针对不同任务，CV和NLP领域都有许多不同的变种，讨论这些变种并不是这篇文章的目的。同时，有很多工作在讨论Attention的分类，从多个不同角度进行评估。

但是，self-attention是无论如何都要去讨论的变种，代表模型Transformer/BERT。

要知道他们是打倒了RNN系列土地主的无产阶级，是不使用RNN系列，只用self-attention构建的模型，是高度可并行的结构。在讨论CNN用于NLP时，计算速度难道不是最吸引我们的一个地方吗？同时他们似乎可以学习到语法/句法结构，比如用于指代消解，比如国外同学做的基于BERT的语言学实验结果等。

上述讨论的内容场景限定在seq2seq下，比如具体的机器翻译任务。但是，诸如序列到值这样的任务，具体如情感分类，能不能利用Attention机制的优点呢？

所谓self-attention，就是自己和自己的HiddenState做相关性计算，从而能够发现一些句子本身内置的结构性特征。例如用于指代消解时，代词和对应的指代的名词之间的相关性分数较高。

Transformer是用于解决seq2seq任务的encoder-decoder模型，不过encoder和decoder端都是基于self-attention实现的。encoder端由多个相同的层堆叠而成，每个层由两个子层组成，分别是self-attention(可以使用multi-head)层和前馈网络层，每个子层后是LayerNorm层，并且每个子层按照残差方式连接。decoder端也是由多个相同的层构成，不过每个层由三个子层构成，其中中间的子层和encoder的每层的第一个子层相同，用于encoder-decoder之间的attention交互。按照Transformer中提到的Q,K,V的概念，encoder后得到的中间表示形式为K,V，decoder端的中间self-attention层作为decoder的Q，通过Q,K之间的相似性计算得到attention分数，乘上V，继而得到新的"中间表示形式"。

从结构上来看，Transformer的并行性来自两个方面。第一，前馈网络层是作用在每个位置上的；第二，多头之间的并行性；

此处头脑风暴一番，encoder和decoder都可以是RNN系，在Transformer中，encoder和decoder都是self-attention模块，那么能否用self-attention模块做RNN系列干的事情呢？比如序列标注，分类等。不考虑性能的影响，起码没有输入长程导致的梯度消失和爆炸问题。虽然BERT做出了非常好的结果，但是self-attention模块的研究还有很大的空间。

BERT较小程度地改造了Transformer的encoder端，通过特殊设计的任务(完型填空)，使得模型能够获取文本的深度双向表示。配合巨大的语料，得到了一个性能非常好的预训练模型，可以用于各种下游任务。

关于BERT，能否用于seq2seq是一个需要思考的问题。

跳出上述讨论的所有来看，attention机制解决的问题仍然是一个"相关"问题，怎样计算相关关系？对谁计算相关关系？如何高效的计算相关关系？等，这个过程不涉及对"因果"的讨论，因此要获取"推理"能力，在现有框架下似乎看不清楚该怎么发展。Transformer通过self-attention组合其他组件，构建了一个可以获取文本好的表示的结构(通过学习的方式)，在BERT中进一步说明了self-attention组件的潜力。


本节参考文献：

1.[《Neural Machine Translation by Jointly Learning to Align and Translate》](https://arxiv.org/abs/1409.0473)

2.[《Effective Approaches to Attention-based Neural Machine Translation》](https://nlp.stanford.edu/pubs/emnlp15_attn.pdf)

3.[  Attention in NLP](https://medium.com/@joealato/attention-in-nlp-734c6fa9d983)

4.《Attention Is All You Need》

5.《BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding》



















