---
layout: post
title: "[NLP]pycorrector统计语言模型部分源码阅读"
excerpt: "统计语言模型用于中文纠错，这部分代码可能有一定的启发性。"
date: 2019-04-04 18:43:00
mathjax: true
---

[pycorrector](https://github.com/shibing624/pycorrector)主要用于中文纠错技术，该实现包含两大类思路。分别是规则模型和深度模型，在该项目中，将统计语言模型包括在规则模型中。代码模块之间的独立性很高，因此可以将自己感兴趣的部分抽取出来。下述是一个单独将统计语言模型独立抽取出来的代码结构。

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

该目录中包含一些常见的辅助功能实现，具体包括繁简转换(langconv.py&zh_wiki.py)，编辑距离的计算，字符串处理等(math
\_utils.py)，io处理，包括logging，load/dump等(io_utils.py)，判断unicode类型，全半角转换等(text_utils.py)，



















