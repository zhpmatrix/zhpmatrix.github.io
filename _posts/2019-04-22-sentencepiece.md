---
layout: post
title: "sentencepiece"
tags: [NLP]
excerpt: "无监督分词器的对比，两个subword算法以及tensor2tensor中subword的实现思路，以及讨论一些subword regularization的东西，其中sentencepiece中某些部分的理解需要去读源代码中的注释才行。"
date: 2019-04-26 18:43:00
mathjax: true
---

<script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=default"></script>

### 一.前言

为了对[sentencepiece](https://github.com/google/sentencepiece)有一个宏观的认识，在这篇博客中先给出sentencepiece，subword-nmt和wordpiece的对比情况，具体对比结果如下（表格来自sentencepiece的readme）：

|Feature|SentencePiece|[subword-nmt](https://github.com/rsennrich/subword-nmt)|[WordPiece](https://arxiv.org/pdf/1609.08144.pdf)|
|:---|:---:|:---:|:---:|
|Supported algorithm|BPE, unigram, char, word|BPE|BPE*|
|OSS?|Yes|Yes|Google internal|
|Subword regularization|[Yes](#subword-regularization)|No|No|
|Python Library (pip)|[Yes](python/README.md)|No|N/A|
|C++ Library|[Yes](doc/api.md)|No|N/A|
|Pre-segmentation required?|[No](#whitespace-is-treated-as-a-basic-symbol)|Yes|Yes|
|Customizable normalization (e.g., NFKC)|[Yes](doc/normalization.md)|No|N/A|
|Direct id generation|[Yes](#end-to-end-example)|No|N/A|

为了简化后续的描述，用sp来简写sentencepiece。在这篇博客中，主要讨论的内容如下：

**第一：和subword-nmt，wordpiece对比，sp的特色**

**第二：sp实现了两个subword算法，bpe和unigram language model**

**第二：sp为了实现subword regularization，实现了subword sampling算法**

**第四：重要参数**

### 二.sp的特色

(1)token的数目需要预先指定（词典大小）

通常nlp的任务都会在训练之前得到一个固定大小的词典。但是，多数无监督分词算法都假设词典大小不固定并且是无限的。虽然sp也是无监督分词，但是通过预先指定词典的大小，可以得到一个固定大小的词典。

(2)不需要预先分词，直接在原始句子上训练

其他的无监督分词器需要预先分词，这样的话就会形成语言依赖，也就是对于不同的语言需要不同的分词器，如果考虑分词器本身的效果不理想，势必会造成后续过程的结果不理想。而sp可以直接在原始句子上训练，这就大大提高了sp的可用性。

（3）tokenized和detokenized的可逆交换

之前的一些分词器将whitespace看做特殊的符号，会导致tokenized后的文本不能恢复到原始文本。但是sp把序列看作是unicode字符序列，这样whitespace就和其他字符一样都是基础符号了，这就实现了可逆性。举一个具体的例子：

输入：

	Hello World.

sp看到的序列：

	Hello▁World.

tokenized之后的结果：

	[Hello][▁Wor][ld][.]

对上述piece做detokenized的过程：

	''.join(piece).replace('_','')

### 三.两种subword算法介绍

1.bpe算法

该算法全称为byte pair encoding，原始是一种压缩算法。放在nlp的setting下，就是将一个大词典可以压缩为一个小词典，这样有助于解决rare和unknown词的问题。想一想中文场景下，基于字的词典大概2000+，但是基于词的字典大小就大多了。既然是压缩算法，自然少不了huffman encoding了，不过和前者比起来，subword具有更好的解释性，同时基于这些subword，网络可以产生新词！（基于组合）具体细节可以读论文《Neural Machine Translation of Rare Words with Subword Units》

作者在原始论文中给出了对应的python实现代码：

```

import re, collections

def get_stats(vocab):

	pairs = collections.defaultdict(int)
	for word, freq in vocab.items():
		symbols = word.split()
	for i in range(len(symbols)-1):
		pairs[symbols[i],symbols[i+1]] += freq
	 return pairs

def merge_vocab(pair, v_in):
	v_out = {}
	bigram = re.escape(' '.join(pair))
	p = re.compile(r'(?<!\S)' + bigram + r'(?!\S)')
	for word in v_in:
   		w_out = p.sub(''.join(pair), word)
		v_out[w_out] = v_in[word]
	return v_out
	
if __name__ == '__main__':

	vocab = {'l o w </w>' : 5, 'l o w e r </w>' : 2, 'newest</w>':6,'widest</w>':3}
	num_merges = 10
	for i in range(num_merges):
		pairs = get_stats(vocab)
		best = max(pairs, key=pairs.get)
		vocab = merge_vocab(best, vocab)
		print(best)

```

2.unigram language model算法

subword sampling和基于unigram的language model算法都是kudo在一篇文章中提出来的，《Sub word Regularization: Improving Neural Networks Translation Models with Multiple Subword Candidates》，这里可以简单的描述。

给一个序列，假设可以切分为一个subword序列，那么可以通过语言模型对subword序列打分选出比较重要的subword。比如可以通过删除一个subword，计算删除前后的语言模型得分的变化来确定。

具体细节可以参考文章中相应的讨论。

### 四.subword regularization

1.subword sampling

给定一个序列，假设可以切分为多个subword序列，那么当对应subword序列用于下游任务时，则可以实现正则化效果，相关的思想非常多，故不再赘述。


### 五.重要参数

1.vocab\_size

该参数是sp的特色，需要在训练之前指定，比如经验值8000，16000，32000等。

2.character\_coverage

模型覆盖的字符数量比例。对于日文和中文这种有着丰富字符的语言，一个好的默认值是0.9995；对于其他有着较少字符集的语言，可以设置为1.0。对该参数的理解是对sentencepiece理解的核心，可以这样理解，给定词表的前提下，希望对一段文本切词之后的词有多少落在词表中，这样的目的是为了减少oov问题的出现。

3.model\_type

模型类型，从上述表格也可以看出，总共有四种，分别是默认的基于unigram的，bpe，char和word，当指定word类型时，必须提前做分词，此时就需要考虑分词器的效果。针对上述四种模型类型，代码组织层是通过factory来实现的，[具体代码地址这里](https://github.com/google/sentencepiece/tree/master/src)。word类型是通过whitespace进行tokenize，char类型是直接将序列变为char序列。

在tensor2tensor中，subword的生成过程是不同于上述的，简单而言是通过对序列的所有词组合进行排列组合，然后通过词频过滤掉一部分不常见的词。并且tensor2tensor中，并没有采用第三方的subword生成工具，而是自己实现了自己的逻辑。

补充材料：

[Tokenizer: How machines read](https://blog.floydhub.com/tokenization-nlp/)
	
[NLP Subword三大算法原理：BPE, Wordpiece, ULM](https://mp.weixin.qq.com/s?__biz=MzIwNzc2NTk0NQ==&mid=2247485705&idx=2&sn=383b7ca2db3b3a635b26de835f3661ea&chksm=970c21dfa07ba8c95513bfbe8c9041d64a1ebfddece4bb8409289565c92504288447e7e2616c&mpshare=1&scene=23&srcid=0425Vgrv7zQo3ryUJ5iIkRzm&sharer_sharetime=1587800482089&sharer_shareid=0e8353dcb5f53b85da8e0afe73a0021b%23rd)

[基于GPU的分词器](https://medium.com/rapids-ai/preprocess-your-training-data-at-lightspeed-with-our-gpu-based-tokenizer-for-bert-language-models-561cf9c46e15#cid=av01_so-twit_en-us)

补充：Huggingface也写了一个分词器，有同学实测比Transformers内置的要快。

补充：《Fast WordPiece Tokenization》,EMNLP2021的工作，“8.2x faster than HuggingFace Tokenizers and 5.1x faster than TensorFlow Text on average for general text tokenization.“


补充：[中文LLaMA&Alpaca大语言模型词表扩充+预训练+指令精调](https://mp.weixin.qq.com/s/ZS1w8-JLrT0U-5v2nk4w8Q)
























