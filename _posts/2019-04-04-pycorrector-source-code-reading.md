---
layout: post
title: "pycorrector统计语言模型部分源码阅读"
tags: [NLP]
excerpt: "统计语言模型用于中文纠错，这部分代码可能有一定的启发性。"
date: 2019-04-04 18:43:00
mathjax: true
---

<script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=default"></script>

## 1.前言
[pycorrector](https://github.com/shibing624/pycorrector)主要用于中文纠错技术，该实现包含两大类思路。分别是规则模型和深度模型，在该项目中，将统计语言模型包括在规则模型中。代码模块之间的独立性很高，因此可以将自己感兴趣的部分抽取出来。下述是一个单独将统计语言模型独立抽取出来的代码结构。

## 2.代码结构

```

├── config.py
├── corrector.py
├── data
│   ├── common_char_set.txt
│   ├── custom_confusion.txt
│   ├── custom_word.txt
│   ├── kenlm
│   │   └── people_chars_lm.klm
│   ├── same_pinyin.txt
│   ├── same_stroke.txt
│   └── word_freq.txt
├── detector.py
├── README.md
├── test.py
├── tokenizer.py
└── utils
    ├── __init__.py
    ├── io_utils.py
    ├── langconv.py
    ├── math_utils.py
    ├── text_utils.py
    ├── tf_utils.py
    └── zh_wiki.py
```
为了运行上述代码，需要预装kenlm，安装命令如下：

```
 pip install https://github.com/kpu/kenlm/archive/master.zip
```

## 3.文件分析

接下来，读一读代码，理一理逻辑。

### test.py

入口函数，通过config.py中的参数初始化一个corrector，调用corrector.correct(seq)可以返回检纠错结果。corrector的初始化参数中需要预训练好的语言模型，因此一个好的语言模型是关键。在该项目中语言模型默认是通过人民日报语料训练的，可以替换为搜狗预料等。混淆集的路径等都在config.py中。

### corrector.py

纠错逻辑的实现类Corrector，继承自Detector类。在Detector类中初始化参数多了**常用字，同音字和形近字集**三类。

### detector.py

检错逻辑的实现类Detector，初始化需要**预训练的语言模型，混淆集(词)，常用词，和（自定义的分词）**。

上述就是核心逻辑实现了，接下来是一些辅助功能模块。

### tokenizer.py

分词功能的封装，使用jieba实现。

### utils目录

该目录中包含一些常见的辅助功能实现，具体包括繁简转换(langconv.py&zh\_wiki.py)，编辑距离的计算，字符串处理等(math\_utils.py)，io处理，包括logging，load/dump等(io\_utils.py)，判断unicode类型，全半角转换等(text\_utils.py)，

## 4.核心逻辑梳理及优化想法

整体逻辑分为检错和纠错，逻辑入口为corrector.py中的correct函数，该函数的输入为待检错的句子sent，逻辑步骤如下：

（1）初始化纠错器(self.check_corrector_initialized)。

（2）检错。返回可能的出错的位置(self.detect)。

（3）纠错。主要分为两个步骤：第一是候选集构建(self.generate\_items)；第二是语言模型选择最合适的纠正词(self.lm\_correct\_item)。

从上述过程可以看到，检错和候选集构造是关键的模块。检错的逻辑实现在detector.py的detect函数中，该函数的输入为待检错的句子sent，逻辑步骤如下：

（1）初始化检错器。

（2) 输入文本的预处理。具体包括：全角半角转换，大小写转换，**分词**。这里的一个关键步骤是分词，包含错误的句子在分词上可能出现混乱，理想的情况是错词附近分词效果差，远离错词的句子分词效果好。默认的分词器是jieba。

（3）检错。检错逻辑分为三种，分别对应三种错误类型，具体如下：

第一："confusion"。错误词出现在自定义的混淆集中。这种自定义的混淆集比较灵活，支持badcase的手动修正，其实就是写规则。在检错之前的一个重要步骤是分词，错句会导致分词的不正确，这样就需要一种规则机制。

第二："word"。有一类词不在词典中，也认为是错误。这类词包括一些实体，一些错词，一些没有在词典中出现过，但是是正确的词等。这条规则比较严格，错词不放过，但是也错杀了一些其他正确词。但是优点同第一，可以灵活修改词典。因此，这步需要一个好的预先构造的词典。

第三：“char”。通过语言模型检错。这里需要关注的是，需要一个好的训练好的语言模型和一个好的检错逻辑。默认的语言模型的训练是基于人民日报语料的。检错逻辑如下：

计算基于字的2-gram和3-gram的得分列表，二者取平均得到sent的每个字的分数；

根据每个字的平均得分列表，找到可能的错误字的位置(self.\_get\_maybe\_error\_index)；因此，这里要考虑找错的具体逻辑。代码中的实现是基于类似**平均绝对离差（MAD）**的统计概念，这里也是一个策略上的改进的方向，甚至多种策略的共同组合判断。

其中MAD的计算如下：

$$

MAD=\frac{1}{n} \sum_{i=1}^{n}\left|x_{i}-\overline{x}\right|

$$

代码中的实际计算不同与上述方式，以代码实现为主。这里可以抽象出的一个问题是：输入是一个得分列表，输出是错误位置。能否通过learning的方式获得一个最优策略。


最后的结果是上述三种情况的并集。

接下来就是候选集的构造了(self.generate\_items)。分情况讨论如下：

第一种情况："confusion",如果是自定义混淆集中的错误，直接修改为对应的正确的值就可以了。

第二种情况：对于"word"和"char"两种情况，没有对应的正确的值，就需要通过语言模型来从候选集中找了。

候选集的构造逻辑如下，输入是item，也就是检错阶段得到的可能的错误词。首先，同音字和形近字表共同可以构建一个基于字的混淆集(confusion\_char\_set)。其次，借助于常用字表和item之间的编辑距离，可以构建一个比较粗的候选词集，通过常用词表可以做一个过滤，最后加上同音的限制条件，可以得到一个更小的基于词的混淆集(confusion\_word\_set)。最后，还有一个自定义的混淆集(confusion\_custom\
_set)。

有了上述的表，就可以构建候选集了。通过候选词的长度来分情况讨论：

第一：长度为1。直接利用基于字的混淆集来替换。

第二：长度为2。分别替换每一个字。

第三：长度为3。同上。

最后，合并所有的候选集。那么通过上述的构造过程，可能导致一些无效词或者字的出现，因此要做一些过滤处理，最后按照选出一些候选集的子集来处理。代码中的规则是基于词频来处理，选择topk个词作为候选集。

梳理上述过程之后，可以思考的几个问题如下：

第一：混淆集的构建。confusion\_word\_set的构建逻辑可以有更好的吗？如何处理混淆集的构建方式使得能够完整覆盖？（需要思考set之间的逻辑运算）这个过程的加速处理？

第二：检错。基于词的n-gram方案没有做，效果怎样，能否和基于字的n-gram合并起来？（分词不等长率=16%）更好的（全局阈值调整），更加多样的检错策略？kenlm的训练粒度？（字和词两种语言模型需要和检错策略对应）

第三：更好的语言模型。由统计语言模型到神经语言模型？
























