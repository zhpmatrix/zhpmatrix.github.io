---
layout: post
title: "论文思考-神经机器翻译中的六个挑战"
tags: [NLP]
excerpt: "这篇博客是一篇为讨论班报告写的论文笔记，论文原题《Six Challenges for Neural Machine Translation》，时间2017年，作者来自JHU的Philipp Koehn等人。虽然有标题党之嫌，但是论文很实用。论文指出了NMT中的domain mismatch, amount of training data, rare words, long sentences, word alignment,beam search相关问题。"
date: 2018-12-22 18:43:00
mathjax: true
---

首先给出文章地址吧。[Six Challenges for Neural Machine Translation](https://arxiv.org/abs/1706.03872)

Google的翻译模型在上线神经机器翻译(NMT)之前是使用统计机器翻译(SMT)的。SMT一般指基于phrase的翻译，NMT通常指端到端的翻译。假设在**二哈语言-人类语言**翻译任务中，SMT是首先将输入的二哈的“语言”和人类的语言分别切分成phrase，然后对每个二哈的phrase，**对齐**到人类语言的phrase，最后**重新组合**成人类的语言作为二哈“语言”的翻译结果。而NMT的方式是直接将二哈的“语言”输入到一个神经网络结构中，输出就是人类的语言。

NMT的出现大大提升了翻译质量，围绕NMT的工作非常多，同时来自NMT的研究成果对其他任务的辐射效果也很明显，因此研究NMT不一定是为了做一个很棒的翻译系统，可能更多的是带来一些具有启发意义的想法。虽然NMT成果显著，但是NMT方法仍然面临很多基础性问题，这些文章主要采用**经验分析**(_较多的实验+一定的理论解释，可能理解的有偏颇。_)的方式讨论这些问题。

#### Domain Mismatch

该问题是指，基于法律领域语料训练的翻译模型在翻译来自医学领域的文本时，可能效果不佳。看下图，

![image](http://wx4.sinaimg.cn/mw690/aba7d18bgy1fyfu0flfpzj20vq0kfjup.jpg)

图中横坐标表示训练集的领域文本，纵坐标表示测试集的领域文本，绿色是SMT的BLEU值，蓝色是NMT的BLEU值。比较特殊的是，表格中最上一行表示该行之下的所有文本的并集。

从上表中可以得出结论：除第一行，对角线上表示same domain的测试结果，显著高于其他cross domain的结果。同时，从某行来看，面对cross domain时，NMT模型的degrade比SMT要显著，BLEU值比same domain要**低的快**，说明相对于SMT，NMT模型对domain更加的敏感。看第一行，不同domain的训练集合并时，相比于单一domain作为训练集，SMT模型的在多个domain的测试集效果要更好，NMT模型除了IT domain，其余指标均有下降。虽然，从直观上看，合并训练集增加了数据的规模，但是从上述实验结果来看，该数据规模的增加，只是提升了SMT的效果，但是NMT的效果却下降了。这里要格外注意的前提是，**测试集是训练集中的一个domain！**，但是，即使测试集也是cross-domain的，测试指标仍然有所下降。同时SMT和NMT相比，从上图可以看出，多数情况下NMT效果优于SMT，**显著优于**。

这好像和我们对于DL中增加数据规模的效果，印象不同啊？

#### Amount of Training Data

给定一个任务，在选定模型的时候，我们需要多少训练数据？看下图，SMT和NMT对比性能和语料规模的关系。

![img2](http://wx2.sinaimg.cn/mw690/aba7d18bgy1fyfurtg7nwj20g10nhn15.jpg)

其中，**phrase-based**是指SMT，**with Big LM**表示使用预训练语言模型。上图说明，在小规模语料下，SMT效果远比NMT要好，同时带有预训练LM的SMT比不带预训练的SMT要好，同时三者随着语料规模的增加，性能都有提升。重要的不同是，NMT对语料规模表现的相对敏感，也就是性能更快的变好，最终可以超过其他两个模型，"强劲"！

虽然作者没有明确给出到底需要多少数据，但是给出了一种关系的描述。由此得到的两个启发是，第一，小数据规模下，尝试一下SMT或许不错，基于统计的方法可能不会弱与基于神经网络的方法（实际上在[中文检错任务](https://zhpmatrix.github.io/2018/12/17/chinese-spell-checker/)上，也可以得到证明。）；第二，对于基于神经网络的方法，数据多点总没有错。

#### Rare Words

针对词分布的问题，经常被讨论的是**OOV**和**稀有词**的问题。针对NLP各个任务中的OOV问题，相当多的方法已经提出来了。这里需要讨论的是稀有词，实际上，虽然OOV问题可能更重要一些。我们用一个更好听的名字来命令，称为**低频词**吧。SMT和NMT对于低频词的处理都有困难，特别是对于一些**highly-inflected**的词。

为此，作者探讨了输入端词频对于翻译质量的影响。使用BPE编码的NMT在处理低频词问题上表现的比SMT系统要好，因此BPE可以将低频词分解，当然这种分解方式不一定按照形态学边界。

其实，低频词当频率为0时，就会导致OOV问题。经常会看到的一种情况是，句子中出现的命名实体。将词分成更小的粒度，小粒度的组合可以成为词，预测在小粒度上进行。类似的思路包括中文领域的按词预测还是按字预测等，如果按字预测，会基本解决基于词的OOV问题，同时词典更小，对计算和存储都是一件好事，理论上，对模型性能或许也有一定程度的提升，更小的词典意味着更小的搜索空间。

除了上述的问题，一般在预处理阶段，也会去做命令实体的替换或者删除，以此减少对下游任务的影响。

#### Long Sentences

基于RNN的模型会经常讨论的一个问题是，梯度消失和爆炸，本质原因在于连乘的性质。放在输入端，就要考虑输入的长度了，因此也就是NLP中常常讨论的句子长度的处理。SMT和NMT对于句子长度的反应是怎样的？

![img3](http://wx1.sinaimg.cn/mw690/aba7d18bgy1fyfv2rnhtbj20km0men0y.jpg)

上图很明确的表达了句子长度对两类模型的影响。在最优句子长度之前，NMT的效果一直优于SMT。虽然BLEU的峰值相同，但是相同峰值，SMT可以处理更长的句子。对于NMT来说，随着句子长度的增加，性能持续下降，**还很厉害呀!**但是看SMT，虽然有一定程度的下降，但是某个地方峰回路转，效果回升。当超过最佳句子长度，NMT系统性能的下降，作者给出的解释是：
    
    The quality of the NMT system is dramatically lower for these since it produces too short translations.

注意，上图中给出的最佳句子长度为60左右，是基于subword的统计。理论上，基于word的统计要小于60，不过现在多数seq2seq系统的实现都是支持BPE的，所以句子长度设置的时候，注意一下长度的粒度。虽然在超过最佳句子长度的时候，NMT表现弱与SMT，但是实际上我们看到在NLP的具体问题中，有不同的方式去处理句子长短不一致的问题，因此这并不意味着当句子很长时，SMT就是一个合理的选择。在最佳句子长度之前，NMT随着句子长度的增加，是持续优于SMT的。

Bengio在2014年的一篇文章中[《Overcoming the Curse of Sentence Length for Neural Machine Translation using Automatic Segmentation》](https://arxiv.org/pdf/1409.1257.pdf)针对句子长度对NMT的影响给出的原因如下：

    Training on long sentences is difficult because few available training corpora include sufficiently many long sentences, and because the computational overhead of each update iteration in training is linearly correlated with the length of training sentences.

    Additionally, by the nature of encoding a variablelength sentence into a fixed-size vector representation, the neural network may fail to encode all the important details.

总之，在翻译任务中，句子长度需要合理选择！

#### Word Alignment

Attention虽然在一定程度上可以实现词对齐，但是二者之间的关系到底是什么？看下图，

![img4](http://wx2.sinaimg.cn/mw690/aba7d18bgy1fyfw5e3edpj20jh0nigof.jpg)

这是一张非常棒的图，也就是说Attention一定程度上可以实现词对齐的作用。既然是一定程度上，那就是不完全吗，看下图，竟然偏移一个单位。

![img5](http://wx4.sinaimg.cn/mw690/aba7d18bgy1fyfw7jtibpj20jt0mjdia.jpg)

针对这种情况，作者给出了一个建议：

    Note that the attention model may produce better word alignments by guided alignment training where supervised word alignments(such as the ones produced by fast-align) are provided to model training.

也就是说，虽然Attention能够一定程度上实现词对齐，但是这个词对齐不是很对齐呀。更好的方式是通过监督学习的方式帮助Attention来学习到更好的词对齐。


#### Beam Search

在decoding阶段，使用Beam Search可以在得到不差的结果的同时，减少计算成本和节约存储空间。通常认为，Beam Size越大，可以扩大翻译空间从而得到更好的翻译结果。在SMT中，Beam Size确实可以提高翻译得分(BLEU)，但是当增大到一定程度时，会损害BLEU得分。那么在NMT的结果是怎样的呢？

**影响和SMT一样。**

作者基于English和其他语言的互译，做了四组实验，最佳beam size的范围在**4-30**之间。该区间范围的启发是合适的beam size找到之后，再去调整找到一个最优的beam size的成本很大，但是收益较小。通过增加对输出句子长度的正则化，一般情况下可以进一步增加BLEU值，但是对应的最优的beam size的区间范围也会扩大，基于作者实验给出的区间范围是30-50，超过该区间，BLEU的值会下降。作者给出的原因是**较宽的beam会导致较短的翻译结果。**

    The main cause of deteriorating quality are shorter translations under wider beams.

此处挖坑，具体原因需要后续探讨。直观地思考，Beam Search算法是Greedy Search和Viterbi Search的中间版，更宽的beam size，使得Beam Search的搜索空间更加地接近Viterbi的搜索空间，由于转移概率的值小于1，故越短的序列预期得到更高的分数。

具体实验结果如下：

![实验结果如下](http://wx4.sinaimg.cn/mw690/aba7d18bgy1fyftvbdcxjj20kk0qwgse.jpg)



#### Interpretable

可解释性是基于Neural Network的工作的硬伤，不瞒您说，秘密都藏在模型的参数矩阵中。虽然围绕可解释性的研究无论在CV还是NLP社区都有一些成果，但是距离我自己想要的解释性似乎还有很多距离。自己希望得到的是模型本身的可解释性，这种可解释性可以去指导我们做模型结构设计和改良，虽然目前可解释性的相关研究也有相关作用，但是还是距离还是很远的。想到冯博说的一句话：

    “在机器学习里，Explainable 和 Interpretable 是不一样的。Explainable ML指的是构建另一个模型来解释一个黑盒模型，而Interpretable ML指的是模型本身在设计的时候就具备解释自己的功能。 ”

我想，我希望的是Interpretable而不是Explainable吧。

总结：围绕**Domain Mismatch**，迁移学习相关的同学讨论的最多。理解这个问题，能够帮助我们更好的去准备训练语料，是选择什么语料的问题？**Amount of Training Data**，是选择多大的语料的问题？这两个都是在准备数据阶段相当重要的问题。**Rare Words**无论在预处理阶段还是在解码阶段都是要去考虑的问题，重视OOV问题就没错了。**句子长度**在NLP的任务中常常是一个超参数，而且是不经常被调节的那个参数，好的句子长度选择或许会带来一定程度的增益。**Word Alignment**在传统SMT中被讨论了很多了，近年来的NLP模型中，Attention已经成为标配组件，虽然Attention能够一定程度上实现词对齐，但是这种实现不是完全等价的，我们需要更好的Attention，比如有一波人是研究稀疏化的Attention。围绕解码算法，beam size也不是越大越好。

对文章的感受是，主要通过对比SMT和NMT，探讨一下我们一直以为的问题是否是一个问题吧。

最后推荐一篇文章《Massive Exploration of Neural Machine Translation Architectures》，对比了NMT中不同组件和模型超参的实验影响。














