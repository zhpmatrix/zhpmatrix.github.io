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

















