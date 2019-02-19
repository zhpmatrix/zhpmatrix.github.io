---
layout: post
title: "[NLP]Rethink系列-词法/句法/语义"
excerpt: "这是一篇写给自己的扫盲短文。我们希望DL的方式能够获取语法和语义信息，但是评估的方式多是通过下游任务的性能，没有从过程上去分析是否确实获得了期望的语法和语义信息，个人对这种分析方式并不认同。直接对词法，句法和语义信息进行分析的技术作为NLP的底层技术，值得进一步探索和思考。"
date: 2019-01-31 18:43:00
mathjax: true
---

一.[Rethink系列-CNN/RNN/GRU/LSTM/BiLSTM](https://zhpmatrix.github.io/2019/01/27/NLP-rethinking-base-blocks/)

二.[Rethink系列-Attention](https://zhpmatrix.github.io/2019/01/27/NLP-rethinking-attention/)

三.[Rethink系列-seq2seq](https://zhpmatrix.github.io/2019/01/28/NLP-rethingking-seq2seq/)

四.[Rethink系列-copy和coverage机制](https://zhpmatrix.github.io/2019/01/29/NLP-rethinking-copy-and-coverage/)

五.[Rethink系列-词法/句法/语义](https://zhpmatrix.github.io/2019/01/31/NLP-rethinking-basic-techniques/)

### 词法

#### 分词

中英文的自然语言文本存在的一个显著的不同是词汇是否连续。比如表达相同的意思：

    中文1：外面在下雪。

    英文1：It's snowing outside.

(_写这篇博客时，外面在下雪，枸杞已泡。_)

假设，我们的中文都是按照这种方式来表达，如下，

    中文2：外面 在 下雪。

那事情就相对好办多了。中文分词正是将中文1变为中文2的过程，是否对中文的自然语言文本处理时，都要进行中文分词？未必。因此有各种任务中，基于字和基于词的方案。学术界和工业界对于分词工具的关注一直热度不减，虽然是中文NLP处理的基础技术，但是分词并未得到完全解决，因此有必要持续关注。

#### 词性标注

为每一个词赋予一个词性，例如形容词，动词等。

#### 命名实体识别

识别句子中的人名，地名，机构名，日期等。

上述三者是词法分析提供的三大功能。分词并不是讨论的重点，就此打住。

### 句法

句法分析中需要先确定一个语法体系，然后由此得到句子的表示形式。其中，重点关注的两种语法体系分别是短语结构语法和依存句法，对应得到的表示分别为成分句法树和依存句法树。短语结构语法关注短语之间的关系，依存句法关注词与词之间的关系。成分句法树可以转化为依存句法树，但是该过程不可逆。举例如下：

    西门子将努力参与中国的三峡工程建设。

短语结构语法表示如下：

![img1](http://wx2.sinaimg.cn/mw690/aba7d18bly1fzoz9oydzij20b20aewf0.jpg)

依存句法表示如下：

![img2](http://wx3.sinaimg.cn/mw690/aba7d18bly1fzoz9ti5qcj20hd0683zc.jpg)

### 语义

#### 语义角色标注(SRL)

谓词是一个句子的中心，SRL关注谓词-论元结构，标注论元的角色。举例如下：

    我正在泡茶。

    我 正在 泡 茶。

    Agent Time Predicate Patient。 

通常SRL要基于句法分析，分析句子中成分与谓词之间的关系，不对句子包含的语义信息进行深入分析。因此，有人提出，SRL是实现浅层语义分析的一种方式。

#### 语义依存分析

和句法依存分析(短语结构/依存结构)相比，该依存分析不受句法结构影响，将具有直接语义关联的语言单元直接连接上依存弧并标上对应的语义关系。[LTP](https://www.ltp-cloud.com/intro#sdp_how)给出了语义依存分析对应的标注列表。

语义在这篇博客中并不打算讨论过多，就此打住了。

本篇文章参考：

1.[Stack Oveflow: Difference between constituency parser and dependency parser](https://stackoverflow.com/questions/10401076/difference-between-constituency-parser-and-dependency-parser)

2.[NLP中深度学习模型是否依赖于树结构？](https://mp.weixin.qq.com/s?__biz=MzIxMjAzNDY5Mg==&mid=209300177&idx=1&sn=4d24467ee27da15ae05effaa0ded9332&scene=2&srcid=1015LyJAMxAtArMzdyKyIRHh&from=timeline&isappinstalled=0#rd)

3.[句法分析在NLP领域的应用是怎样的？jiangfeng的回答](https://www.zhihu.com/question/39034550/answer/79392998)

4.[自然语言理解太难了！系列](https://github.com/fighting41love/hardNLP)

5.[解密英语语法-王垠](https://blog.csdn.net/zhenyu5211314/article/details/85304247)















