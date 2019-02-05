---
layout: post
title: "[NLG]论文阅读-《Generating Sentences from a Continuous Space》"
excerpt: "主要从贝叶斯角度讨论了VAE的目标函数的由来，分三步由浅入深讨论VAE，同时给出了VAE应用于文本生成任务的工作。"
date: 2019-02-05 16:34:00
mathjax: true
---

<script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=default"></script>

这篇文章是首次讨论VAE用于文本生成任务，从目前发展的结果来看，GAN在CV领域的生成效果好于VAE，因为VAE的生成图片比较模糊。但是在文本生成任务中，VAE的效果应该要好于GAN的使用。参考5和参考6中给出了一种从贝叶斯角度得到VAE的损失函数的方法，值得品味一番。

假设数据x的真实分布为p(x)，由于p(x)在DL的方法框架下不可知，因此，想要通过一个q(x)来近似p(x)，理想情况下，希望p(x)=q(x)。在这里，不加解释的直接引入隐变量z用于建模q(x)，如下：

$$q(x)=\int q(x,z)dz=\int q(x|z)q(z)dz$$


其中，q(x\|z)就是想要的生成模型了。为了保持一致性，假设真实分布p(x)也是由隐变量z生成的。由于我们对p(x)一无所知，因此这种假设是合理的。既然近似，那就需要评估近似的手段，显然，衡量两个分布的近似程度，KL距离是首先能够想到的(实际上，单纯的度量方法有很多，不过KL距离具有多方面的优越性)。度量表达如下：

$$KL(p(x,z)|q(x,z))=\iint p(x,z)ln\frac{p(x,z)}{q(x,z)}dzdx$$

由于p(x,z)=p(x)p(z|x)，则上式可以展开得到，

$$KL(p(x,z)|q(x,z))=\int p(x) \left[ \int p(z|x)ln\frac{p(x)p(z|x)}{q(x,z)}dz \right] dx=E_{x \sim p(x)} \left[ \int p(z|x)ln\frac{p(x)p(z|x)}{q(x,z)}dz \right] $$

上式将对数项展开，可以得到一个常数项，进而可以得到损失函数，如下，

$$loss=KL(p(x,z)|q(x,z))-const=E_{x \sim p(x)} \left[ \int p(z|x)ln\frac{p(z|x)}{q(x,z)}dz \right] $$

由上式可以观察到const确定了loss的下界，并且由于const本身的取值范围，导致loss可以为负。

当然可以继续将loss函数展开，就得到VAE的损失函数，

$$loss=E_{x \sim p(x)} \left[ E_{z \sim p(z|x)} \left[ -lnq(x|z) \right]+KL(p(z|x) | q(z)) \right]$$

有loss函数的形式来看(上上式更加直观)，我们的目的是找到q(x\|z)和q(z)使得loss函数最小化。至此，VAE的loss函数得到了。

现在注意几个细节。

在上述式子的推导过程中，我们用到的是p(x,z)=p(x)p(z|x)，但是p(x,z)=p(z)p(x\|z)也成立，此处能够带来什么启发呢？直观地从VAE做的事情来看，可以得到p(z|x)，数据本身的分布是p(x)，但是p(z)未知，自然难以得到p(x\|z)，这不正是我们想要学习到的q吗？

这里又出现了两个项的和共同作为loss函数，传统的loss函数，遇到这种结构的时候，多半是普通的损失项加上正则项，通常在正则项前添加一个调节常数因子。而这里的loss函数是作为整体的两项出现的，不同于以往。尝试分析一下这里的loss函数，第一项，需要q(x
\|z)大，这意味着生成能力强。理想情况下，KL项也对应的小就好了，但是这里成立吗？

上述得出了loss函数的形式化的表达，但是不够具体，下面讨论一下详细计算loss函数的需要的三个项，分别是q(z)，q(x\|z)，和p(z\|x)。

在VAE的设定中，假设$$ q(z)=N(0,I) $$

p(z\|x)和q(x\|z)不知道咋搞呀？在前一篇博客中提到的，反正分布也是个函数(松弛条件下)，那就NN来吧。从这两项可以看出，分别对应"编码"和"解码"，或者说描述了一个重构过程。

具体地说，同样假设p(z\|x)也是一个正态分布，那么自然需要分布对应的均值和方差来描述该分布。明确一下此处的输入和输出，分别是输入x，输出均值和方差。这样，loss函数的第二项的KL损失可以计算了。

类比，q(x\|z)可以假设为伯努利分布(二值数据，CE损失函数)和正态分布(一般数据，MSE损失函数)。

假设第一步是得到形式化的损失函数，第二步是具体化每个项的表达形式，第三步则是具体计算。由loss函数的第一项可知，需要通过采样的方法得到对期望的估计。VAE认为采样一个就OK，具体需要借助"重参数化技巧"。一旦只采样一个，loss函数的形式又可以继续化简。那么，为啥一个就OK呢？

重参数化的技巧值得一提。对p(z\|x)建模后得到均值和方差，当此时采样一个满足该均值和方差限定的正态分布的样本时，其实是得到了一个常量。由于是依概率采样，这个常量没有显示地建立与均值和方差的关系，则p(z\|x)得不到采样结果的反馈。

既然没有参数化采样结果，那就参数化呀。借助于概率统计中正态分布和标准正态分布之间的关系实现参数化，有：

$$z=均值+\epsilon*方差，\epsilon \sim N(0,I)$$

那么，至此，VAE的理论部分基本讨论完了，部分细节上的考察需要后续深入思考。

整体上看，VAE是原始AE添加了正则项，表现为KL损失，因此，全部的损失函数为重构损失加上KL损失。而这其中的两个细节在于V(变分)和重参数化技巧。V的来源可以不严格的认为就是KL作为正则项的应用，而重参数化技巧则是为了解决"采样"操作本身的不可导性(采样结果可导)，通过从标准正态分布中采样，简单代数运算后得到非标准正态分布的采样结果。

衡量两个概率分布之间的距离有多种，但是为啥选择KL距离呢？从数值角度来看，KL散度可以写成期望的形式，而期望的计算可以通过[数值计算和采样计算](https://spaces.ac.cn/archives/5343)。

实际上，类似于SeqGAN，存在Conditional SeqGAN一样。对于VAE，同样存在Conditional VAE。并且如果考虑到隐变量的连续性和非连续性，当隐变量是离散变量的时候，可以基于VAE做聚类。

回顾了VAE的基本理论，来讨论一下应用。《Generating Sentences from a Continuous Space》这篇文章应该是首次将VAE用于文本生成的文章，直接给出模型结构如下图，

![变分自编码语言模型结构](http://wx2.sinaimg.cn/mw690/aba7d18bly1fzunj20gylj20lg05pab4.jpg)

其中，encoder和decoder都是一层的LSTM，文章认为在上文中讨论的q(z)是施加在hidden code上的正则化项。在关于z的使用方案中(encoder-decoder的连接部分)，文章尝试了下述方案：

第一，将z作为decoder的每个时间步的一个输入；

第二，读方差进行softmax参数化；

第三，在encoder-latent variable和latent-decoder分别尝试使用前馈网络；

结论是，上述三种方案都差不多。实际上，在传统的讨论的seq2seq方案中，上述的一些尝试同样可以进行。

关于encoder部分，也就是p(z\|x)的高效建模，作者也尝试了一些比较复杂的方案，包括基于正则化流做后验估计等，都发现没有带来显著的效果提升。

这篇只关心VAE在文本生成任务上的首次应用，证明确实是可行的。除了上述讨论的内容，文章还有针对具体任务地一些其他讨论，具体细节可以读论文。(_发现文章写多了，这部分细节不能展开讨论，后续有机会了会重新拉出来讨论吧。_)


主要参考：

1.《Generating Sentences From A Continuous Space》

2.[PaperWeekly-VAE For NLP](http://rsarxiv.github.io/2017/03/02/PaperWeekly%E7%AC%AC%E4%BA%8C%E5%8D%81%E4%B8%83%E6%9C%9F/)

3.[Sentence-VAE，PyTorch](https://github.com/timbmg/Sentence-VAE)

4.[变分自编码器系列一](https://spaces.ac.cn/archives/5253)

5.[变分自编码器系列二](https://spaces.ac.cn/archives/5343)

6.[变分自编码器系列三](https://spaces.ac.cn/archives/5383)

7.[变分自编码器系列四](https://spaces.ac.cn/archives/5887)













