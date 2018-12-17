---
layout: post
title: "[生活杂谈]Eigen实习总结"
excerpt: "围绕在Eigen的实习内容，回顾了任务分析，论文复现，拼写检查，经验教训四个方面的内容。讲述一个小白掉入NLP坑中的辛酸史。"
date: 2018-09-28 16:21:00
mathjax: true
---

_[Eigen](https://www.eigentech.ai/)是一家AI初创公司，A轮，实习时间共十周。实习很大的一个感受是，公司风格Google Style，成员学历都很不错，浙大，科大为主，实习生来自海外名校的很多，前端组基本都是硕士，算法组我知道的有三个博士，整体上感觉不错。实习的时候，算法这边感觉很像实验室的生活节奏，不过模型上线的时候，还是很忙。但是产品组紧跟业务，加班挺多的。这篇博客是从实习总结中修改而来的，可能有些内网链接失效。_

### 零. 前言

这篇实习总结报告将围绕四个部分来完成。第一部分对实习任务进行分析；第二部分讲述了中文语法错误诊断（CGED）的工作；第三部分回顾拼写检查（SpellChecker）的工作；第四部分谈一下本次实习的经验和教训。

### 一. 任务分析

本次实习任务是中文语法检纠错。场景是中文，包含两个子目标检错和纠错，对象是语法。针对这个任务，首先需要明确研究对象，也就是要解决的错误类型，以及错误类型的成因。为此，调研了关于中文语法错误相关的文献近20篇，形成文献合集《中文错别字调研论文合集》，结论是中文语法错误类型众多，成因复杂。
围绕该任务的公开数据集和比赛较少。调研过程中，发现该任务和IJCNLP2017承办的一个比赛Chinese Grammatical Error Diagnosis(CGED)类似，于是决定首先从复现这个任务开始，为实习任务提供一个baseline。
    

### 二. CGED

这个比赛已经举办五届，是ICCE, ACL, COLING, IJCNLP的子赛道任务，具体可以查看[官网](http://www.cged.science/)说明。比赛针对HSK的数据集，也就是非母语环境，非母语使用者的中文错误标注，进行四类错误类型的检错，具体包括多词，少词，错词，和词序不当。2018年的比赛添加了纠错任务，实习任务开启时，2018年的比赛尚未结束，所以，可以看到的是2017年的一个不错的结果对应的相关论文《Chinese Grammatical Error Diagnosis with Long Short-Term Memory Networks》，作者群来自HIT的刘挺组。该工作将此任务作为序列标注问题来做，模型主要使用BiLSTM，输入特征分为三类，分别是Bigram Embedding，Character Embedding，Pos Embedding，每个时间步有四个输入，当前时刻和前一时刻的Bigram Embedding，当前对应的Character和Pos的Embedding。后续的工作中，文章做了将CRF的输出作为BiLSTM的输入，融合上述三类特征，发现有进一步提升。注意，这里是不同于常见的BiLSTM+CRF的模型组合去做序列标注任务的，CRF担任的是decode的角色，而文章中CRF担任的是一个特征生成的角色。

针对这篇文章，联系了文章一作郑博，现为刘挺组的在读博士生，拿到了源代码。代码后端基于cnn-v1，前端数据预处理部分基于python。在调试运行该源代码后，发现缺点如下：

* 无GPU支持。CGED16+CGED18作为训练集的前提下，50个Epoch平均耗时6h。考虑到后续的数据增强，目前的代码将会遇到训练速度瓶颈

* cnn-v1是cmu开发的基于C++的小众框架，常见组件和技术文档缺乏，扩展性差。

* 源代码耦合度较高，代码风格较差。比如，在inference模块抽离过程中，遇到了各种由于多个global variable存在导致的问题。

由于上述问题的存在，决定放弃直接使用源代码，自己基于tensorflow重新实现。这里是源码地址，复现结果在评测指标上基本符合预期。

有了一个baseline，接下来做的工作就是能够提供一个接口或者用于测试的交互界面，也就是需要将模型部署。针对这部分工作，实现两个版本的代码。第一种是前端采用Flask框架，后端自己做字典资源的加载，模型载入，预处理，模型预测和后处理等逻辑；第二种是采用tensorflow-serving完成，这也是公司推荐的方式，前端不变，后端有变。tensorflow-serving的方式是将模型放到一个tensorflow model server上，然后提供一个访问接口给后端来用，方便了session管理，模型迭代等诸多工作，源码地址在这里。
部署完成后，实测结果不够理想。限于比赛官方提供的数据集非常少，首先尝试从数据角度出发，去构造更多的数据。针对比赛提供的四种错误类型，具体的构造规则见周报，增强代码在这里。基于上述增强后的数据，重新train了一个新的模型，从评估指标来看，该模型的预测能力不如不做增强的模型，分析原因可能是在做数据增强的时候，错误类型比较密集，导致模型在获取上下文语义的时候比较困难。于是重新做了增强，保证每个文本只有一个错误类型，基于该数据集的模型并未重新train。

由于我们考虑基于CGED的数据集来做，可能距离实用较远，于是暂时中止CGED的工作，转向错误类型更明确，应用场景更实际的拼写检查工作。从市场上的已有产品调研来看，比如无错字和云查错等，也多是针对这种场景做检查，比如输入法检错等。

实际上围绕CGED也做了一些其他的工作，具体代码详见这个[Repo](https://github.com/CGEDJNU)。

### 三. SpellChecker

拼写检查，从做输入法开始，就有一拨人在做这个事情。在实习开始前，征哥就做了一个初版。初版的数据规模和类型较少，模型使用BiLSTM+Multi Head Self-Attention，试图建立拼音->字的映射关系，但是模型似乎对获取上下文的能力较弱。后续训练了一个语言模型，但是效果较差，于是目前所有的精力都Focus在非语言模型上，做持续改进。

从建模方式上，我们着重考虑了两种映射方式，拼音->字和字->字。其中，拼音分为带音调和不带音调，实验证明，带音调对于同音字检查问题是一个重要特征。

从特征层面上，输入特征可以是单独的不带音调拼音，带音调拼音，字，也可以是他们的组合。

从数据层面上，这个是我们的一个重点关注的方向。截止目前，围绕数据层面，做了三个工作。第一是扩大量。围绕这个问题，我们基于LCSTS，做了数据增强，每句一个同音字错误。效果有提升。第二是考虑句子长短。我们基于全网新闻数据集生成了新版数据。第三个工作构建了更具diversity的数据集，数据来源为LCSTS, News，淘宝，微信，中文对话，电影台词六个数据集。

从模型层面上，我们做了对比实验，比较了Multi Head Self-Attention的提升效果，尝试了BiLSTM加不加Dropout的影响，同时也尝试了基于BiLSTM+CRF，但是汉字字典大小为8000，这样CRF转移概率矩阵的大小就是8000x8000，训练速度非常慢。

上述改进的方向，在我和征哥的近期周报中都可以看到具体的参数设置和评估指标等。

最近了解到NLPCC TASK2 GEC这个比赛也是做中文语法检错，不过语料集和CGED类似，都是非母语使用者所犯的错误，错误分布和拼音输入法的错误分布应该存在不一致问题，这个比赛提供了用NMT的方式去自动检错的思路。同时看到云查错这款产品的一个研究人员在知乎的一个回答，如下：

```目前中文文本纠错普遍不太理想。商业版的也就黑马一家，不过比较贵，而且速度慢，对新词处理不理想，尤其是互联网文本的查错比较差。错别字针对应用场景，可以分为：搜索词纠错（这个多半用历史搜索词来校对）、通用文本纠错（一般性的文章）、特定领域纠错（如政府公文、医疗领域）。 考虑计算机文本输入，目前有拼音输入、五笔输入、OCR输入三种主要的方式，需要针对这三种方式去考虑。 目前基于机器统计的办法是主流的。训练阶段，要建立ngram模型和字、词混淆集。建立ngram语言模型，需要考虑ngram的平滑度。字、词混淆集的建立是一个重点，要从字形、字义、音近、音同等几个方面去考虑。 对于要纠错的文本，计算局部位置的ngram概率，找到可能的“嫌疑词”，通过字、词混淆集去构建候选的词，用候选词替换原词，再计算ngram概率，如果显著上升，则是比较可信的候选词。 最后，需要对候选词进一步使用句法依存关系，判断候选词的语义级别的概率，减少误报。 完全基于机器推荐，也不能解决所有问题，还是要积累一些特定规则，对明显是错别字但是难以机器失败的，可以加入规则来解决。 笔者实现了一个错别字算法，云查错，你可以试试：http://www.http://yunchacuo.com
```

我们希望有个general的模型可以做检错，但是短期来看似乎难度很大。只有RNN+Attention或者RNN+CRF似乎不能够完全解决问题，需要同时配合其他的一些统计或者规则方法，模型和工程的结合更好的去解决问题。回到当前，首先尽可能用上述方法去解决同音字全拼错误的问题；其次，同音字简拼错误；最后形近字纠检错。这样的话，才可能有一个针对输入法错误可用的检查器。

### 四. 经验教训总结

在本次实习之前，自己几乎没有接触过NLP的任务，此外也是第一次去使用Tensorflow搭建Pipeline，静态图和动态图的使用体验不是很一样，不过很庆幸，Tensorflow2.0开始默认支持动态图了，同样是第一次使用Tensorflow Serving，了解到Tensorflow生态的部署理念。再者，Eigen提供了一个很好的项目NLP-Onboard，提供了一些推荐论文，同时从组里同事们的周报中也看到一些推荐的阅读论文，自己又从2018年的各个NLP顶会中搜集了一些文章，实习期间大概读了30+篇文章，对NLP领域的前沿有个大致的了解。最重要的是实习期间，从同事们那里学习到了很多。和斌哥，征哥讨论问题的时候，看大家周报的时候，看到俊哥长长的读书笔记后，看到Github学优的代码后，看到兴华的CV后，看到一圣坐在工位的时候（他一直在那里，不是吗？)等等。此外，总是很欢乐的金金同学和前端组的同事们，也总是使得气氛很活跃。

但是，回顾项目实施过程中，也有很多教训需要反思。首先是要重视论文或者比赛SOTA与算法能用之间的距离。从一开始，征哥就强调，我们需要的是能用的，而不是SOTA。其次，要针对业务有合适的评估指标。CGED从比赛角度有自己的评估指标，实际上在做的时候，我自己采用了Confusion Matrix看P, R和F1-score三个指标，这个是更细粒度的指标。但是在SpellChecker中我们则定义了五个有针对性的评估指标，尽可能全面评估模型的效果，实际上定义合适且正确的指标可能是最重要的事情。最后，要贯彻一套代码的原则，整理出适合自己的一个Pipeline。在复现过程中，走了一些弯路，因为对框架的不熟悉，导致自己在实现的时候遇到一些细节上的问题。很多任务具有相似性，一个Pipeline可以用来做很多任务，这个是后续需要注意的地方，提高代码的可复用性。














