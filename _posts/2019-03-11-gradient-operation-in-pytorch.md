---
layout: post
title: "[PyTorch]默参都是全局的，局部学习率调度和局部梯度Clipping，咋搞？"
excerpt: "PyTorch中模型分层设置学习率和灵活的梯度操作，比如梯度Clipping问题。"
date: 2019-03-11 18:43:00
mathjax: true
---

<script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=default"></script>

这两天浏览到苏神的文章，也就是参考1中的博客，讨论了Keras的分层学习率设置和梯度操作问题。最近刚好在重刷PyTorch1.0的文档，顺道关注了一下这两个需求在PyTorch中的实现。

### 模型分层设置学习率

近些年来围绕学习率改进的工作较多，同样在实际使用中，有时候会要求不同层有不同的学习率。比如，典型的fine-tuning的过程；比如使用可变卷积的时候(通过设置该模块自己的学习率，使得模型更加容易训练。)；

PyTorch中给出了非常优雅的方式，实现该目的。示例代码如下：

```

torch.optim.SGD([{'params':model.base.parameters()},{'params':model.classifier.parameters(),'lr':1e-3}], lr=1e-2, momentum=0.9)

```

上述代码的含义是model的classifier使用的学习率是1e-3，除此之外，其他所有组件使用相同的学习率1e-2，momentum的值是0.9。优化器的第一个参数是参数列表，常见的情况是直接传入model.parameters()。必要的时候也可以使用如下方式：

```
torch.optim.SGD([val0,val1],lr=1e-2)
```

而上述代码的风格就和这种方式类似。除此之外，需要关注参数列表中的值，通过显式给组件命名的方式，比如命名为base&classifier，从而实现方便的调用。

但是，对于二阶优化算法，比如LBFGS，暂不支持上述学习率操作方式。DL的场景下，目前主要还是使用一阶优化算法。官方提示如下：

```
This optimizer doesn’t support per-parameter options and parameter groups (there can be only one).
```

这里面有两个重要的概念，分别是per-parameter options和parameter groups。在上述代码中model.base和model.classifier分别是两个group，每个group的参数可以有自己的options。

### 分Epoch设置学习率

除了模型分层设置不同学习率，更为常见的一种情况是分Epoch设置学习率。相关的学习率策略较多，主要思想是模型训练的后期，参数接近最优，就得小心翼翼的探索了，学习率小一些，但是前期属于优化过程的蛮荒时代，大步快走。这样的一个组件称之为Scheduler，但是Scheduler在训练过程中并不是必须的，但是很多时候可以作为一个Trick出现，有奇效。PyTorch内置的实现可以分类三类来看。


#### 初级版Scheduler

按照固定的范式随着Step/Epoch更新学习率，例如学习率的指数衰减等。包括函数torch.optim.lr\_scheduler.StepLR，torch.optim.lr\_scheduler.MultiStepLR，torch.optim.lr\_scheduler.ExponentialLR，torch.optim.lr\_scheduler.CosineAnnealingLR。

#### 中级版Scheduler

torch.optim.lr\_scheduler.LambdaLR接口给与了我们更大的Scheduler定制能力，如果说初级版Scheduler是按照某种固定范式实现调度，那么该接口可以让我们定义这个范式。比如代码如下：

```
lambda1 = lambda epoch: epoch // 30

lambda2 = lambda epoch: 0.95 ** epoch

scheduler = torch.optim.lr_scheduler.LambdaLR(optimzier, lr_lamdba=[lambda1, lambda2])

for epoch in range(100):
    scheduler.step()
    train(...)
    validate(...)

```

#### 高级版Scheduler

在调参阶段，调整学习率的目的是在验证集上获得更好的指标，比如验证集的损失函数小或者准确率高；如果将验证集的度量指标当做学习率调度的反馈信号，那么就直接抵达目标了。PyTorch已经帮我们实现了一个函数torch.optim.lr\_scheduler.ReduceLROnPlateau。比如可以实现这样的目的：

当连续10个Step发现验证集的损失函数不变小之后，那么自动将学习率变小。

早停的策略与之类似，不过早停就是停下来了防止Overfitting。而高级版Scheduler是通过自动将学习率变小，进一步优化过程。从另外一个角度来看，更像将交叉验证中对学习率的参数选择单独给了一个实现。不过对DL的模型做CV显然不太现实，因此这个接口的实现其实很有必要，我喜欢这个接口。

### 灵活的梯度操作

PyTorch中为了防止梯度消失和爆炸，实现了两个接口用于控制梯度。分别是torch.nn.utils.clip\_grad\_norm\_和torch.nn.utils.clip\_grad\_value\_。但是这两个接口的问题在于是对全局的grad进行操作，比如计算grad\_norm的时候，是将全局所有的参数concat成一个向量，然后计算norm。但是一个很显然的需求就像上述的模型分层设置学习率一样，只希望部分梯度参与clip操作。比如代码如下：

```
x = torch.tensor([1., 2.]) #此时，x.grad=None

x.grad = torch.tensor([0.3, 1.]) #可以显式的操作x.grad，那么可以为所欲为了。

torch.nn.utils.clip_grad_value_(x, clip_value=0.4)

print(x.grad)

```

结果为：

```
tensor([0.3000， 0.4000])
```

由于可以访问x.grad，那么这自然为后续灵活的操作梯度提供了极大的便利。近两年的一些工作也是围绕梯度来进行的，通过直接对梯度进行操作实现某些优化目的，提升性能，因此后续实现一些模型或者策略的时候可能需要注意这个地方。

### 模型中的权值共享

这是一个很经典的场景，比如支持多任务的模型。给定两个输入A和B，要求模型的前三层共享相同的权值，后两层针对不同的输入进行参数更新，也就是权值不共享。示例代码如下：

```
class MyModel(torch.nn.Module): 
    def __init__(self):
        self.base = ...
        self.head_A = ...
        self.head_B = ...
    def forward(self, input1, inptu2):
        return self.head_A(self.base(inptu1)), self.head_B(self.base(input2))

```

在NLP中，围绕权值共享也有一些工作。主要是将Embedding层的权值共享到其他地方去。举两个典型的场景：

第一：语言模型。编码器可以是一个Embedding层，解码器是一个线性层，那么二者的词向量权重可以共享；代码如下(具体代码可以参看[这里](https://github.com/pytorch/examples/blob/master/word_language_model/model.py))：

```
self.encoder = torch.nn.Embedding(vocab_size, embed_dim)
self.decoder = torch.nn.Linear(embed_dim, vocab_size)
self.decoder.weight = self.encoder.weight
```

注意，在PyTorch中，self.decoder.weight的shape是(vocab\_size, embed\_dim)，和输入接口的定义相反，但是self.encoder.weight的shape和输入接口保持一致。

第二： Transformer。可以在源端(encoder)，目标端和生成器端(decoder)三个地方共享词典的权值向量。

参考:

1.["让Keras更酷一些！":分层的学习率和自由的梯度](https://spaces.ac.cn/archives/6418)

2.[torch.nn](https://pytorch.org/docs/stable/nn.html)

3.[How to create model with sharing weight?](https://discuss.pytorch.org/t/how-to-create-model-with-sharing-weight/398/2)















