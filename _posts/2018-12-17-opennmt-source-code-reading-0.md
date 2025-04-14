---
layout: post
title: "预处理模块源码剖析"
tags: [工程架构]
excerpt: "讨论预处理模块的相关设计"
date: 2018-12-17 18:43:00
mathjax: true
---

前言：我本机的源码的commit号是**38df8665e3ce55102d45b8bb26a749ea0f3d42b4**，部分分析会直接去读OpenNMT-py的在线repo，**版本号为v0.2**，master上的代码。OpenNMT的实现有三个版本，分别是Torch，PyTorch和TensorFlow，后续的分析会以PyTorch为主，TensorFlow为辅。这两个版本相比，PyTorch版本的更加完善，实现了NMT中的很多有效Trick，相比下来，TensorFlow的发展较为缓慢。

OpenNMT-py纯Python实现，不需要像读C++项目的代码的时候，需要先编译为可调试版本。

预处理模块的入口代码文件是**OpenNMT-py/preprocess.py**。调用方式如下：

    python preprocess.py -train_src data/src-train.txt -train_tgt data/tgt-train.txt -valid_src data/src-val.txt -valid_tgt data/tgt-val.txt -save_data data/demo

上述命令行，传入训练集，验证集和持久化文件保存的路径。进入preprocess.py文件中，关键处理逻辑如下：

1.get\_num\_features

2.get\_fields

3.build\_save\_dataset

4.build\_save\_vocab

上述4个逻辑顺次执行。逻辑1和2解析存储在磁盘上的文本数据，3和4将解析后的数据存储在本地，为训练过程过准备。对于翻译任务来说，解析后的数据包括分片后的训练/验证集和词典。分片是为了避免将大量的数据载入内存时遇到OOM的问题，和生成器的思路类似，这个工程Trick在很多源码中都可以看到。

从架构上，讨论一下逻辑1和2的代码结构。

这两个逻辑的实现在inputter类中，具体代码路径为OpenNMT-py/onmt/inputter/，这个目录下包含的具体文件分别为text\_dataset.py，image\_dataset.py，audio\_dataset.py，dataset\_base.py和inputter.py。

OpenNMT显式支持的数据类型有三种，分别是text/image/audio，对应三个预处理文件，三个预处理文件的实现是dataset_base.py的子类，inputter.py中实现的是一个工厂模式，工厂模式的使用在很多源码中同样是很常见的，比如XGBoost的[源码实现](https://zhpmatrix.github.io/2017/03/15/xgboost-src-reading-2/)中，Caffe的源码实现中同样也有应用，而且在这种预处理的逻辑下使用工厂模式是一个很自然的想法。

```

def get_num_features(data_type, corpus_file, side):
    """
    Args:
        data_type (str): type of the source input.
            Options are [text|img|audio].
        corpus_file (str): file path to get the features.
        side (str): for source or for target.

    Returns:
        number of features on `side`.
    """
    assert side in ["src", "tgt"]

    if data_type == 'text':
        return TextDataset.get_num_features(corpus_file, side)
    elif data_type == 'img':
        return ImageDataset.get_num_features(corpus_file, side)
    elif data_type == 'audio':
        return AudioDataset.get_num_features(corpus_file, side)
    else:
        raise ValueError("Data type not implemented")

```

看上述代码，通过传入预处理的数据类型，调用对应类的方法。此外，传入的另一个参数表明处理的是源端还是目标端，对于seq2seq任务，输入的是平行语料。对于OpenNMT-py来说，数据的组织方式是将源和目标对齐分开。当需要基于源码扩展数据类型的时候，这里就是入口。

沿着上述逻辑，进入TextDataset类中，这里就是对文本数据的具体处理逻辑了，例如读取数据，数据解析，数据读取生成器(yield实现)等，不同类型的数据对应不同的处理方式。在代码中，主要使用PyTorch提供相关数据处理函数，例如torchtext库，torchvision库(PIL，cv2)，torchaudio库等。在入口处扩展数据类型后，或者说"注册"后，在该目录下新建一个对应类型文件，继承dataset_base类，基于PyTorch或者其他第三方工具实现具体的处理逻辑。

_提示：在我本地的版本中，源码中get\_fields的逻辑在各自对应的子类中，但是在v0.2中，将该逻辑放到了inputter.py的实现中。_

逻辑1和2执行完成后，回到preprocess.py中执行逻辑3和逻辑4，这两个逻辑主要用于生成中间数据（数据分片后）和词典的本地持久化(torch.save)，对数据工程上的性能不满意的时候，此处可以从内存和并行角度持续进行优化。由于自己并没有用OpenNMT处理大规模数据的经历，故目前对此处没有优化需求。

除了上述关键逻辑，还有参数解析和日志模块，此处忽略。处理模块组织层面，该部分涉及语法知识较少，具体来说，assert，抛异常，继承，类变量，静态方法(装饰器)，yield等。


总结：数据预处理逻辑借用工厂模式，灵活的组织了文本，图片和音频三类数据，并且扩展容易。OpenNMT-py的具体实现逻辑要基于PyTorch内置操作及其第三方库。之前大致读过[tensor2tensor](https://github.com/tensorflow/tensor2tensor)的数据预处理代码，tensor2tensor在该逻辑上同样封装良好，可以互相参考。














