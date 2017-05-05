---
layout: post
title: "[Optimization]基于反馈的随机梯度下降算法"
excerpt: "《IMPROVING STOCHASTIC GRADIENT DESCENT WITH FEEDBACK》算法复现记录，这是一篇来自ICLR 2017的顶会论文。同时提出了自己针对这篇论文的分析和想法，以及进一步follow的做法。"
date: 2017-05-05 10:48:00
mathjax: true
---
<script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=default"></script>

这篇博客是近期晚上的工作，白天的工作会等做完之后，在另外一篇博客中总结。博客是围绕ICLR 2017的一篇文章的工作，优化相关。主要内容包括文章的算法和思路复盘，和阿里流行音乐预测大赛的亚军方案的类比，文章代码的评论，文章可以继续做的方向，例如可能和SAG/SVRG等方案的结合。

由于这是自己读的第一篇DL领域的优化相关文章，就本文来说，感受如下：

*1.* 优化不推Bounds(据师兄说，DL的文章没有很多数学的东西，还是很多DL的文章没有很数学的东西?)

*2.* 实验做到颈椎炎复发(老板组会上说过一句话：现在的科研都是实验科研。老板本人是做优化的，但是不是Learning领域中的优化，是PSO的大咖)

*3.* 故事讲的好(文中很多启发性的东西，好的文章是在讲一个好的故事)

*4.* 文章公开代码(愿所有文章有实验就公开代码)

---

文章是基于[Adam]((https://zhpmatrix.github.io/cellar/Optimization_Algs_For_Learning.pdf))的一种改进算法，,加入了来自目标函数的反馈(Feedback)信息，简单来说就是参数更新之后，目标函数值相较于参数更新前的目标函数值的变化率。算法伪代码如下：

![sgd-with-feedback](http://wx2.sinaimg.cn/mw690/aba7d18bgy1ffa709x3a1j20gu0jsq6d.jpg)

如图中黄色框所示，在原来Adam的参数更新项的分母上添加Feedback信息。目的很简单，如果参数更新之后目标函数值变化比较大，则放慢学习速率，小心翼翼的学习；如果变化较小，加快学习速率，大步快走。从代码整理来看，相较于Adam的原始算法的更新主要在蓝色框内，其中蓝色框内的红色框是对目标函数值变化率的一个平滑。这里有一个非常有意思的**Clipping**操作:

$$c_t \leftarrow min \lbrace max \lbrace \delta_t,\frac{f(\theta_{t-1})}{\hat f_{t-2}}\rbrace,\Delta_t\rbrace$$

首先，什么是[clipping](https://docs.scipy.org/doc/numpy/reference/generated/numpy.clip.html)操作？

简单来说：给定一个范围[A,B],对于任意小于A的数NA,都使得NA=A；对于任意大于B的数NB，都使得NB=B；对于任意NC大于A且小于B，使得NC=NC(此处没有笔误！！！)；

其次，为什么上式可以实现clipping？

给定三个数a,b,c,令:


$$c_t \leftarrow min \lbrace max \lbrace a,b\rbrace,c\rbrace$$

\\(c_t\\)的取值情况是怎样的？

a,b,c三个数之间比大小，共有6种结果。如下：

1.  a>b>c,a>c>b,b>a>c,b>c>a:    \\(c_t=c\\)

2.  c>a>b:  \\(c_t=a\\)

3.  c>b>a:  \\(c_t=b\\)

所以，单纯的使用上式，任给a,b,c三个数，该式clipping后的结果不等概率！！！为了能够等概率取到a,b,c三个数，得加上**constraints**。

怎样寻找**constraints**?

情况2和3必选，1中四选一。比如两种解决方案：

(1).    b>c>a,c>a>b,c>b>a

和

(2).    a>c>b,c>a>b,c>b>a

为什么要上述两种解决方案，因为两种方案有共同的特点，三个不等式都存在共性。（1）中满足c>a;(2)中满足c>b;这样**方便构造constraints！！！**其实，文章中采用的就是（1）的解决方案，构造constraints的方式就是:令\\(a=\delta_t\\),\\(b=\frac{f(\theta_{t-1})}{\hat f_{t-2}}\\),\\(c=\Delta_t\\)，会看蓝色框中的嵌套层的if-else语句中关于\\(k\\)和\\(K\\)的构造表达，始终满足\\(c>a\\)。

这里会出现第一个想法。既然文章中使用了方案(1)，那么我们使用方案(2)如何构造呢？此外，在等概率的情况下，还有另外两种方案我们没有提到，就是\\(a>b>c\\)和\\(b>a>c\\)的情况，这两种方案虽然没有共性存在，但是可否也寻找到一种clipping方案呢？

在文章中，作者提到，原来他们只是使用红色框中内容，不使用clipping操作，但是**这样就导致了发散和不稳定**。为了解决这个问题，首先他们采用的clipping是:

$$min \lbrace max \lbrace k,d_t\rbrace,K \rbrace$$

但是这种方案也不work，给出的原因是**abrupt nature of the clipping**,于是最终调整成Eve算法，也就是我上文分析的伪代码，学术名词称为*smooth tracking*，同时这样的改良带来了一个优点：对mini-batch操作带来的高可变性不敏感。

下面给出作者在文章中的实验结果。在公布的代码中，有一些ML中的实验，似乎效果并不太好，但是在DL中的实验表现，还是不错的。

small CNN（CIFAR10）和big CNN(CIRAR100)分类任务表现：

![cnn](http://wx3.sinaimg.cn/mw690/aba7d18bgy1ffa9r4ed03j20nf09gjtv.jpg)

RNN上的测试包括语言模型(Penn Treebank)和QA测试(bAbI):

![rnn](http://wx3.sinaimg.cn/mw690/aba7d18bgy1ffa9raeqmej20ns0gmq5w.jpg)

在公布的代码中作者在数据集MNIST,CIFAR10,CIFAR100上测试了Batch Logistic Regression,Logistic Regression,MLNN(Multi Layer Neural Network),**可能由于效果一般，故论文中也没有给出(效果确实一般，为了不砸场子，我就不放图了)**。

原则上，一般作为论文笔记到这里就可以结束了。如果仅仅只对文章感兴趣，到这里就可以结束阅读了。但是还可以聊点别的不是吗？这里谈四点，不做过多阐述。

#### 1.想法都是相通的。

这是阿里流行音乐预测大赛亚军方案，基于规则的方案，在使用规则之前，对流量序列进行了编码，这是一种编码方案，是不是看出了什么呢？

---

![alibaba](http://wx4.sinaimg.cn/mw690/aba7d18bgy1ffa9xmspflj20em092jti.jpg)

___

#### 2.对手都是强大的。

这是论文放出没几天，同学给pytorch提出的pull request。这个真的是为开源做贡献的一个好的方法。

[Issues#1329@pytorch](https://github.com/pytorch/pytorch/issues/1329):[proposed feature]Eve:Improving Stochastic Gradient Descent with Feedback 


#### 3.代码都是有用的。

作者放出的代码中，是基于keras+Theano+Tensorflow的，是对Optimizer的自定义。所以，一个好的库应该在接口设计上给用户留下自定义的空间，这点xgboost，keras都做到了。这样的好处之一就是能够快速验证我们的想法，而不用为了验证想法写很多"周边代码"（与问题解决没有太强联系的代码）。这点对于做优化的同学可能启发性更强，核心代码量不多，但是为了验证想法，要写的"周边代码"很多，例如Eve的代码也就是在Adam的代码上添加了蓝色框内的内容而已。也从另外一方面说明了为什么对手都是强大的？

#### 4.观点都是想象的。

这个想法的关键是将目标函数变化的信息体现在对梯度的更新上，具体来说是学习率的改进上。本文是基于Adam进行的改进，实际上这个想法不拘泥Adam本身，原则上基于梯度的方案都可以尝试这样的想法。但是问题是Adam是在DL领域中目前来说平均表现最好的Optimizer，如果将这样想法应用到别的算法上，最起码不能比Eve要弱吧。但是基于梯度不一定只在DL领域做，不一定只做到一阶，不一定只做共享内存，不一定只做同步？有没有黑到什么？这其实也是这篇论文带给followers的启发。

**参考**：

1.[CIFAR 10/100](https://www.cs.toronto.edu/~kriz/cifar.html)

2.[What is the class of this image?](http://rodrigob.github.io/are_we_there_yet/build/classification_datasets_results.html)

3.[Why is the natural gradient not used more in machine learning?](https://www.reddit.com/r/MachineLearning/comments/2qpf9x/why_is_the_natural_gradient_not_used_more_in/)

