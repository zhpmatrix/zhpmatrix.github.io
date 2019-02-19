---
layout: post
title: "[NLP]Rethink系列-copy和coverage机制"
excerpt: "从一篇论文出发，讨论了与attention相关的两种机制，这两种机制在opennmt-py中都有相应的实现，同时提了一些可以进一步思考的问题。"
date: 2019-01-29 10:26:00
mathjax: true
---

一.[Rethink系列-CNN/RNN/GRU/LSTM/BiLSTM](https://zhpmatrix.github.io/2019/01/27/NLP-rethinking-base-blocks/)

二.[Rethink系列-Attention](https://zhpmatrix.github.io/2019/01/27/NLP-rethinking-attention/)

三.[Rethink系列-seq2seq](https://zhpmatrix.github.io/2019/01/28/NLP-rethingking-seq2seq/)

四.[Rethink系列-copy和coverage机制](https://zhpmatrix.github.io/2019/01/29/NLP-rethinking-copy-and-coverage/)

五.[Rethink系列-词法/句法/语义](https://zhpmatrix.github.io/2019/01/31/NLP-rethinking-basic-techniques/)

机器翻译和文本摘要是NLP中的经典任务，seq2seq的很多研究工作一般都会在机器翻译上首先尝试。同时由于文本摘要和机器翻译在任务上的相似性，在机器翻译任务中有效的工作一般也可以用于文本摘要的任务，基于两个任务的相关研究工作互相借鉴，共同发展。一个不严格的感受是机器翻译的进展要快于文本摘要。

传统意义上的机器翻译是语言翻译，输入和输出域不同。例如输入是英语域，输出是中文域。文本摘要的输入和输出域相同，通常是根据中文文章输出中文摘要。注意，这里的域是指通俗意义上的领域，比如语种差异。

在文本摘要中，会想要在摘要文本中出现一些输入文本中不存在的词，由此达到摘要生成的目的。(_学术上区分文本摘要为基于生成式的和基于抽取式的。想像一下，小学语文考试需要用自己的话概括一段话的意思，理想情况下，用自己的话，不是段落中的话来概括段落的含义。有些老师会告诉你，如果不会自己概括，那就从段落中摘抄一些句子。前者可以认为是生成式，后者就是抽取式了。_)

经典的seq2seq+attention可以实现生成式摘要。但是生成的摘要存在两个明显的问题：

第一.摘要会去重复他们自己。这里分两种情况，其一是单句摘要，看到一个字不断重复的现象，在机器翻译领域也会出现；其二是多句摘要，看到某个句子重复。

第二.摘要的内容存在事实性错误。尤其是稀有词和OOV词带来的负面影响，这是主要问题。(_围绕OOV的问题，学术界的研究成果也是非常丰富的。_)

第二个问题显然比第一个问题严重的多。如何解决？

OOV是词汇非常稀有以至于没有出现的特例。不考虑细微差异的前提下，后续使用的稀有词包含OOV。稀有词较少，属于语料的问题。无论如何强大的模型，对于该类词的直接的特征学习能力都不会令人满意。

既然很难学习，那就不学了，直接copy。

假设存在一个合理的copy机制，那么我们的模型就兼具abstractive(generating)和extractive(copying)能力了。那么，最重要的问题就是如何设计一个合理的copy机制？合理性体现在既能实现copy，又能兼具生成和抽取的能力。

经典的CP组合decoder端每个时间步会得到一个词典长度的概率向量，表示当前时间步为词典中某个词的概率，概率向量和为1，保证是一个合理的概率分布。

类比，在encoder端也有一个合理的概率分布，就是attention分数的分布，和为1。那么，也就意味着输入序列的词汇也可以构造出一个词典，而attention分数可以当做输入序列构成词典的每个词汇的满足某种含义(相关性)的概率。

decoder端的每个时间步的输出词取决于某个词典的概率分布。按照上述的逻辑，想让存在于输入序列中的OOV出现在摘要中，OOV就要出现在这个词典中。那么显然，输入序列构成的词典和输出端的词典的并集就是我们要的了。

从另外一个角度，这个输出词汇的概率可以认为是由两端的词典的词汇概率按照某种比例组合而成。而这个比例可以是encoder端的利用attention得到的中间表示(上下文向量)，decoder端的输入，decoder端的上一时刻的HiddenState的函数。

为啥可以？因为经典的CP输出的概率不也是上述三个量的间接函数表示吗？

参考文献1给出了一种copy机制，具体细节可以参看论文。opennmt-py也实现了论文对应的模型，不过上文中提到的"比例"的计算方式和论文有细微差别。上述讨论给出了基本动机，能否设计出更好的copy机制是一个值得思考的问题。

基本解决了重要的问题(第二)，就要去考虑不重要的问题(第一)。

重复的可能原因是什么？从重复的内容来看，文本摘要任务中是输入文档中的某些句子，那么在这个任务中，就是要减少输入文档中重复的句子量。进一步思考，为什么？如果attention机制使得decoder老是盯着相同的句子，那么就有大概率会导致重复。这里更加细致的讨论，应该需要考虑decoder端每个时间步三种输入的比重问题。

假设是这个原因，那就需要思考减少过分关注的发生。attention分数是关注的度量，因此一种可行的思路是从attention分数下手。那么如何去度量过分呢？

在decoder端的每一个时间步都需要利用前一时间步的HiddenState和encoder端的所有时间步的HiddenState计算一遍，得到attention分数，进而得到对应decoder端当前时间步的中间表示。

假设encoder的时间步长度为N，decoder端的时间步长度为M，则解码到第M步时，encoder端会得到M组N维向量。那么，基于M组N维向量，度量过分的方式大致有一些，比如：

第一.encoder端对应时间步的attention分数求和。

第二.encoder端某个时间步对应的attention分数历史序列的某个窗口的统计值，比如最大，中值等。

当然，可以设计一些其他的度量方式。

我们希望过分关注的HiddenState就不要再过分关注了，这个需要一个量化的操作来实现。

在文献1中，通过减少decoder端当前时间步对应的

encoder端的attention分数(一个N维向量，用A表示)      

和

历史attention求和分数之间的(一个N维向量，用B表示)

交集(每维求min后，对所有维度求和)

来实现。

上述建立了A和B之间的函数关系，作为约束(惩罚项)出现在原始的负对数似然函数中。这种函数关系想必也可以有多种，比如建立一个关于输入的衰减函数等。

上述谈到的问题在机器翻译中同样存在，不过具体的表现形式存在微小的差异。值得一提的是，上述讨论的内容多是围绕参考1展开来的，copy机制和coverage机制还是有不同的表现方式，具体可以找些文章来读。此外，此二者都是基于attention机制的，是attention机制的再利用。在opennmt-py中围绕attention的实现包括上述两种机制，[具体包括](http://opennmt.net/OpenNMT-py/options/train.html)：基本的attention机制(Bahdanau,Luong等)]，copy_attn，coverage_attn，copy_loss_by_seqlength等，其他相关机制四类。文档中这部分参数，看起来有些乱，代码中有一些简单的[注释](https://github.com/OpenNMT/OpenNMT-py/blob/master/onmt/opts.py)，可能后续会单独对opennmt-py中这部分与attention有关的机制实现做个讨论，理清思路。

_后记：_

_这趟回家，无锡，上海，郑州在KFC的平均停留时间超过三个小时。这篇博客是在郑州火车站的KFC中完成的。在上海KFC期间读了一篇CTO极力推荐的论文，NIPS2018汤晓鸥组林达华等人做的image captioning的工作，这个思路或许可以用于其他语言生成类任务中，稍后关于这篇文章的想法会形成一篇博客作为输出。同时作为对比，可能写一篇同组师弟在投的CVPR2019的关于视觉问答的工作。吃鸡腿去了。_


本文主要参考文献：

1.《Get To The Point: Summarization with Pointer-Generator Networks》

2.[上文对应Poster](http://forum.stanford.edu/events/posterslides/GetToThePointSummarizationwithPointerGeneratorNetworks.pdf)

3.《Modeling Coverage for Neural Machine Translation》

4.[《Pointer Network》](https://arxiv.org/pdf/1506.03134.pdf)















