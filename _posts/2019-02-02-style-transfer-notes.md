---
layout: post
title: "[NLG]论文阅读-文本风格迁移"
excerpt: "慢慢地需要从自然语言理解过渡到自然语言生成，生成的应用场景较广，值得关注。这篇博客是最近读的几篇文章的一个论文笔记，主要目的是帮助自己建立一个对风格迁移任务的印象。"
date: 2019-02-02 18:00:00
mathjax: true
---

文本生成在模型上的变化主要包括生成对抗网络(GAN)系，自编码(AE)系，增强学习(RL)系和其他系。整体上的思路发展和CV保持一致，但是CV中的流(Flow)系目前还没有看到在NLP领域中的相关工作，值得密切关注。这篇文章，主要围绕文本风格迁移读一些论文。

1.《Dear Sir or Madam, May I Introduce the GYAFC Dataset:Corpus, Benchmarks and Metrics for Formality Style Transfer》

这篇文章主要针对文本风格迁移任务，构建了一个数据集，提供了五个benchmark，做了一些度量。这里的风格迁移是正式文本和非正式文本的双向迁移，这是的正式是指"是不是正式的说话"，数据集来源为Yahoo Answers问答论坛。

没有仔细看平行语料的构造方式，这里想一下方案。正常情况下可以是给定一句话，如果这句话是正式的，写出对应的不正式的表达；如果是非正式的，写出对应的正式的表达。关于正式和非正式应该是可以训练一个分类器，这样在构建新的平行语料的时候，可以免去判断正式和非正式的繁琐过程。

benchmark主要包括三类：基于规则的方法，基于按照短语进行机器翻译的方法，基于神经机器翻译的方法。

这篇文章的数据集是做正式和非正式文本的双向迁移，实际上迁移的内容包括：礼貌和非礼貌，有想象力和没有想象力等。理论上，只要构建基于某个表达维度的平行语料，这个任务就可以做。类似文章如2所示。

2.《Shakespearizing Modern Language Using Copy-Enriched Sequence-to-Sequence Models》

这篇文章任务上实现现代英语到莎士比亚英语的风格转换，模型上使用带有copy机制的seq2seq思路。由于在这种任务场景的设定下，冗余存在OOV问题，因此使用上述解决思路也是讲的通的。除此之外，还有散文风格迁移的数据集，如3所示。

3.《Evaluating Prose Style Transfer With The Bible》

这篇文章构建数据集的方式很有意思。拿到Bible的几个版本的数据，就可以得到多组平行语料了。

从上述三篇文章来看，文本风格转换的问题在于平行语料的获取难度较高。一旦有了语料，从模型上，可以按照经典的seq2seq相关技术解决此类问题。但是，风格是一个比较抽象的概念，由此导致任务本身可能难度较高。因此，通过无监督的方式来做此类任务是一个理想的途径。

4.《Evaluating Style Modification in Text》

NLG的问题，难免要去讨论评估的问题。上述这篇文章主要阐述三个方面的评估。具体如下：

第一，style transfer intensity. 具体来说，可以通过训练一个分类器，判断是转换前的文本还是转换后的风格文本，将分类概率作为intensity的度量；

第二，content preservation. 具体来说，就是常见的基于n-gram的BLEU指标，用来评估生成文本和目标文本的相似度；

第三，naturalness. 这类指标的实现需要人工评估，具体包括fluency/readability, grammaticality,naturalness等；

和之前读过的文章相比，第二和第三的两套指标作为实验评估的手段比较常见，但是第一种不是很常见。由于第一种需要重新训练一个分类器，而该分类器的训练数据正是生成的数据，因此使用的时候可能会存在一些问题，同时评估成本较高也是显而易见的。

CV中的风格迁移取得了很不错的效果，但是NLP领域的风格迁移要落后于CV，主要原因应该包括两个方面：NLP中缺少平行数据和没有可靠的评估指标。因此，有很多工作想尝试没有并行数据的情况下来解决该问题。

5.《Style Transfer in Text: Exploration and Evaluation》

这篇文章使用adversarial networks学习各自的content representation和style representation从而能够利用non-parallel的数据。为了解决缺乏可靠评估方法的问题，提出了两种新的评估方法，分别是transfer strength和content preservation。同时在两个任务上测试了模型和评估方法的效果，分别是paper-news title transfer和positive-negative review transfer。这篇文章的两个评估指标在文献4中也有重点提到，但是这里使用的评估方式不代表确定方法，而是评估的两个方面。

比如文章中针对style representation还是通过训练一个分类器的方式，针对content preservation是利用source端和target端关于embedding的统计指标的的相似性，最后对两个方面的指标进行加权平均。

adversarial network已经被成功的应用到domain separation problems，比如学习domain-invariant特征，获取多任务框架中每个句子的share和private表示等，而style transfer也是包含了两个方面content和style，因此当将adversarial network应用于style transfer中，关键的问题是如何学习到content和style？为此，作者提出两个模型，分别是multi-decoder和style-embedding，具体细节可以参照论文。

由这篇文章也可以看到，直接将其他任务中的好用的模型或者框架引入到一个新的任务中，看似没有原创有水分，但是如果能够抓住问题的本质，合理地针对任务本身做设计，也确实是一个创新的方法。这篇文章是AAAI2018的，个人认为文章写作上也是很好的。

6.《Multiple-Attributes Text Rewriting》

通过对抗的方式获得disentangled representation已经是style transfer任务的通用方式。但是，这篇文章作者认为并不是必须的，提出基于去噪自编码的改进工作使得能够用于多个属性的文本重写，多个属性包括性别，情感，产品类型等。文章中的两个数据集值得关注，分别是[Yelp](https://www.yelp.com/dataset/challenge) Reviews和Amazon Reviews关于餐馆，产品等的评论数据。

7.《Style Transfer Through Back-Translation》

ACL2018的文章。这篇文章首先通过一个语言翻译模型学习输入句子的latent representation，目的是在风格化文本的同时能够保持句子的含义不变，这个过程就可以使用back-translation，然后通过adversarial generation技术使得输出能够match到期望的风格。无论是back-translation还是第二个阶段的adversarial generation技术都是在style transfer任务中比较常见的技术。但是这篇文章能够做到SOTA，还是很强。此外，这篇文章的实现是基于opennmt-py，值得后续跟进学习。

8.《Style Transfer from Non-Parallel Text by Cross-Alignment》

[代码这里](https://github.com/shentianxiao/language-style-transfer)，其中模型的总体架构如下：

![img1](http://wx1.sinaimg.cn/mw690/aba7d18bgy1g0bndtoy35j20yp0cgq69.jpg)

这篇文章主要提出了两个AE的变种，分别是aligned ae和cross-aligned ae。在三个任务上进行了实验，分别是sentiment modification，decipherment of word substitution ciphers和recovery of word order。我个人比较关注的是第一个任务上的结果。在和Zhiting Hu的工作对比时，结果虽然在量化指标上(accuracy)比Hu的工作稍差，但是实际生成结果来看要好一些。如下：

![img2](http://wx2.sinaimg.cn/mw690/aba7d18bgy1g0bmbr68xdj20nz0n5wil.jpg)

上图中每组例子第一行是输入文本，第二行是Hu的结果，第三行是这篇文章的结果。可以看到，Hu的工作在content preserving方面弱于本文。这里可以展开讨论的一点是，对于任务输入和输出的定义。在中文检纠错任务中，可以只输出错误的地方(错误类型标注)；也可以输出修改后的整体的句子(句子改写)。选择什么样的技术方案，需要考虑到什么样的输出对于该任务是合适的。同时，从这组实验结果来看，对于生成的评估需要持续思考。不仅要思考general的评估指标，同时结合任务本身做特殊评估指标设计。值得一提的是，模型中针对discrete和non-differentiable的问题，作者的解决方法是gumbel-softmax(_和Hu的工作一样_)和Professor Forcing两种方式。

9.《Toward Controlled Generation of Text》

[代码这里](https://github.com/asyml/texar/tree/master/examples/text_style_transfer)，其中，还是基于VAE的工作，模型的总体架构如下：

![img3](http://wx1.sinaimg.cn/mw690/aba7d18bgy1g0bndpbrzyj20q40e3q4p.jpg)

这篇就是上文提到的Zhiting Hu的工作，属于较早期的工作，后续又出现了很多相关文章。这里值得一提的是，模型会遇到discrete和non-differentiable的问题，作者的解决方法是gumbel-softmax。

万小军老师在一次报告中提到：**"我想强调的是，基于神经网络模型的NLG并不成功，虽然我们做了很多学术研究，发表了很多学术论文，但很多任务上只要性能提高1%-2%，都可以发论文，但是从实用性角度来看，这些技术很难达到理想的满意程度，所以我们还需要进一步在数据与模型上不断完善。"**

总结：关于风格迁移，style transfer，style modification，controlled text generation等是常见的术语。这个任务可以采用seq2seq的方法，基于encoder-decoder框架来做。既然是文本生成，自然在学术界中GAN，AE等相关方法也有采用。由于该任务下平行文本预料获取的困难，因此针对非平行文本的研究相当的多。此外，要结合任务本身去思考，将通用架构设计地更加的符合style transfer任务本身的需求，适合多个transfer设定才是这个任务本身的特色之处。从应用上，可以用于各种改写任务，而改写任务的场景较多，同时便于和上游任务结合使用，从而完成更加高级的任务。比如data2text->style transfer，或者translation->style transfer等，甚至更深的级联深度。从另一方面来看，style transfer属于小众研究领域，看了多篇文章开源的代码，更加印证了这个想法，不过这个任务本身还是非常棒的。


主要参考：

1.[GAN和文本生成](https://zhuanlan.zhihu.com/p/36880287)

2.[文本风格迁移论文列表](https://github.com/fuzhenxin/Style-Transfer-in-Text)

3.[万小军老师关于NLG的想法](https://mp.weixin.qq.com/s?__biz=MzAxMzA2MDYxMw==&mid=2651567544&idx=1&sn=df1375d7f3eb737ca548eafb3fa48395&chksm=80574ad2b720c3c48a7339137128c21248709b7f69f887c443cae8bb171b2e55517e6523f967&mpshare=1&scene=23&srcid=%2523rd)













