---
layout: post
title: "[NLP]Rethink系列-seq2seq"
excerpt: "主要是对encoder和decoder的一些想法"
date: 2019-01-28 18:00:00
mathjax: true
---

一.[Rethink系列-CNN/RNN/GRU/LSTM/BiLSTM](https://zhpmatrix.github.io/2019/01/27/NLP-rethinking-base-blocks/)

二.[Rethink系列-Attention](https://zhpmatrix.github.io/2019/01/27/NLP-rethinking-attention/)

三.[Rethink系列-seq2seq](https://zhpmatrix.github.io/2019/01/28/NLP-rethingking-seq2seq/)

四.[Rethink系列-copy和coverage机制](https://zhpmatrix.github.io/2019/01/29/NLP-rethinking-copy-and-coverage/)

五.[Rethink系列-词法/句法/语义](https://zhpmatrix.github.io/2019/01/31/NLP-rethinking-basic-techniques/)

个人认为，seq2seq是NLP相关技术的核心。2014年开始，seq2seq和attention成为超强CP，活跃在各个任务中。单纯从字面意思来理解，seq2seq的命令只是定义了模型的输入和输出都是seq，这是一个相对空洞的命名。背后则是encoder-decoder的框架，在本系列的第二篇博客[Rethink系列-Attention](https://zhpmatrix.github.io/2019/01/27/NLP-rethinking-attention/)中已经讨论了一部分相关内容。

跳出来，从第一性原理出发，如果拿到一个seq2seq的任务，怎么做？

输入输出端都是seq，按照NLP的通用思路，加之Embedding技术的成熟，两端都做Embedding是必须的。将离散的文本做量化使之能够被计算，同时尽可能保持语义信息。seq2seq描述了一种映射关系，需要建模输入seq和输出seq之间的关系，也就是需要一个量化后的输入seq和输出seq之间的交互操作。显然，交互操作就是关键了。实际上，正是Attention担当了此种重任，但是并不完全。

上面的描述很容易使人联想到句子相似度匹配，问题选择，自然语言推理等相关任务。同样需要两个Embedding组件和交互组件。其中，整体上的一个区别是，seq2seq的输出是在其中一端(decoder)，而前述相关任务的输出则是在交互组件后，也就是交互组件得到的结果是对句子关系的表征。

所以，能否有一个通用的框架可以同时处理上述两类任务就是一个值得思考的问题。BERT目前来看，并不能。

按照上述的逻辑，可以从三个方面做Rethink。

### Encoder

在本系列第一篇，提到目前NLP的主流组件：CNN/RNN/GRU/LSTM/BiLSTM/Attention。也就是说，encoder端和decoder端的选择理论上有多种。这里需要提醒的是，此处的Attention更多的是指self-attention，例如Transformer中的encoder/decoder，为了能够直观的感知，列表如下(_也可以将作为交互组件的Attention考虑进去，划分seq2seq的方法_)：

| 序号 | Encoder | Decoder |
| ------ | ------ | ------ |
| 0 | CNN | CNN |
| 1 | CNN | RNN/LSTM/\* |
| 2 | CNN | Attention |
| 3 | RNN/LSTM/BiLSTM | RNN/LSTM/\* |
| 4 | RNN/LSTM/BiLSTM | CNN |
| 5 | RNN/LSTM/BiLSTM | Attention |
| 6 | Attention |  Attention|
| 7 | Attention |  RNN/LSTM/\*|
| 8 | Attention |  CNN|

从上表可以看出，共有8种方案(decoder端需要考虑语言模型的限制)。目前来看，方案3和方案6(Transformer为代表)是主流，那么是否意味着其余方案不可行，没有必要呢？恐怕未必。方案3已经有几年的历史了，但是方案6依然年轻，可以挖掘探索的空间还有很大。如果考虑其他组合，可以研究思考的空间又大了许多倍。

在知识的海洋面前，我们都是一群小屁孩儿。人类应知自己的渺小和悲哀，但是又不失对未知的好奇和探索精神。放置宇宙，这种微如尘埃的感受又会被无限放大。

encoder以seq2seq中的老大爷RNN/LSTM/BiLSTM为例，也就是方案3。为了描述简单，统称RNN。

2014年的相关工作中，涉及到的seq2seq框架的组成多是由encoder->中间表示->decoder。中间表示是对输入seq的编码表示，decoder能够使用该编码表示用于解码得到输出seq。中间表示作为两端交互的信息，如何得到呢？RNN每个时间步会得到对应输入对象的HiddenState，该HiddenState作为当前输入对象的量化表示。那么对应的输入seq的量化表示很容易想到最简单的方案。


第一，最后一个时间步对应的HiddenState作为整个输入seq的量化表示。因为最后一个时间步含有所有时间步的信息。RNN是一个迭代结构，从第一个时间步开始，信息进行迭代，直到最后一个时间步。但是这里需要考虑的问题是，会不会由于输入seq的过长导致信息的损失和遗忘？

第二，既然有了每个时间步的量化表示，那就全部用上。求和/取平均等操作。

第三，区别于第二，只使用部分，构造一个最近时间步的窗口。求和/取平均等操作。第一，第二和第三，本质上都可以用一个加权方案统一起来。

第四，区别于第二，只使用部分，选出哪些最重要的。对重要性的评估需要一个比较对象，同时需要给出重要性的定义，也即是之前谈到的Attention了。

上述步骤一到四，能否用一个方案统一起来呢？

这里区分一下原始RNN和LSTM的区别，对于原始RNN而言，InternalState=HiddenState；对于LSTM，InternalState=\[CellState，HiddenState\]

由于LSTM和原生RNN的基本组件不同，在具体策略上不会完全相同。比如LSTM中有CellState和HiddenState，而原生RNN只有HiddenState，因此有时候也用InternalState统一描述。此处更加合理的应用就值得进一步思考。

从上述讨论可以看出，目前encoder端的方案使用的大多数是最容易想到的方案，而encoder端的信息利用实际上还有很大的可以挖掘的空间。

这部分内容主要讨论了encoder->中间表示，下面内容讨论中间表示->decoder。

### Decoder

目前seq2seq的精华主要在decoder端了。沿着上述思路，思考如何去decode呢？

从对称角度出发，encoder端的输入包括当前时间步的输入，上一时间步的HiddenState。在解码时，decoder端是没有当前时间步的输入的，不要忘了上文中得到的中间表示，正好可以将其作为decoder的当前时间步的输入。从理论上讲，输出seq与输入seq的相关关系在每个时间步得到体现。有了输入，就有了decoder端的HiddenState。

这种形式是将中间表示作为decoder端每个时间步的输入；因此，很自然可以想到只将中间表示作为decoder端第一个时间步的输入。

这是思考的第一个层次，也就是中间表示如何使用的问题。此处就可以和Attention机制建立起基本的联系，在相关博客中提到，无论是所有还是第一个时间步使用这种中间表示，似乎都不是特别的合理。每个时间步的decoder输出应该利用encoder表示的不同部分，具体来讲，每个decoder的输出用到的中间表示都不是相同的，需要动态变化。

第二个需要考虑的问题是输出反馈。这部分是RNN系的特色。在训练的时候，decoder端当前时间步要不要接受前一时间步的输出结果？

第一种方式是要的，但是这种方式带来的问题是假设前一时间步输出有误，则会造成错误传递；

第二种方式是不要，但是使用前一时间步的正确输出作为当前时间步的一个输入。和前者的区别在于都需要前一步的输入，但是第一种方式是预测直接作为输入，而第二种方式则是标签直接作为输入，这样的好处是，即使前一时间步错了，也不会输入错误的信息导致误差的积累；

其实上述两种方式仍然显得有些僵硬。理论上存在一种中间方式，比如错的时候用标签作为输入，正确的时候用预测作为输入，尽可能增强模型的学习能力。沿着这种思路，仍旧可以带来很多想象。

上述讨论的思路很简单，正确的处理方式并非只有两个极端，或许中间状态更好。按照相同的思想，很多相关技术的提出都是这种思路，所谓狭义上的"泛化"和"通用"。

这是思考的第二个层次，也就是要不要反馈。

上述是相对不细致的描述，只是暂时抛去对细节的考察。通过这种方式，能够对发展的方向有所了解，否则陷入技术细节的汪洋大海就不太好了。

从另外一个方面，"The devil is in the details."，对细节的追求才能更深刻的理解技术的本质，相关细节将会在新的博文中阐述(_主要是我现在写不动了啊。_)。


本文主要参考文献：

1.[《Sequence to Sequence Learning with Neural Networks》](https://arxiv.org/abs/1409.3215)

2.[《Learning Phrase Representations using RNN Encoder-Decoder for Statistical Machine Translation》](https://arxiv.org/abs/1406.1078)

3.[《Neural Machine Translation by Jointly Learning to Align and Translate》](https://arxiv.org/abs/1409.0473)

4.[A ten-minute introduction to sequence-to-sequence learning in Keras](https://blog.keras.io/a-ten-minute-introduction-to-sequence-to-sequence-learning-in-keras.html)

5.[漫谈四种神经网络序列解码模型](http://jacoxu.com/encoder_decoder/)
















