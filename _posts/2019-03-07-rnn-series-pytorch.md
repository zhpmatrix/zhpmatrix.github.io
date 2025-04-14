---
layout: post
title: "RNN遇上PyTorch"
tags: [PyTorch]
excerpt: "解释了PyTorch中RNN系的参数，输入和输出。接口包括两类，分别是多层结构和Cell结构。相比于Tensorflow中的多个版本实现，PyTorch中的要清晰很多。"
date: 2019-03-07 18:43:00
mathjax: true
---

<script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=default"></script>

这篇博客，主要梳理一下PyTorch中的RNN系实现的相关接口和参数，输入和输出维度的对应。结合使用其他框架的体验，做一些简单的对比。PyTorch老鸟可以直接飞走了。

GRU的Cell结构如下，

![img1](http://wx4.sinaimg.cn/mw690/aba7d18bgy1g0uet6s5t8j20kd06jgmj.jpg)

PyTorch中对应的类是**torch.nn.GRU**。其中参数如下：

input\_size: 输入特征的维度

hidden_size: 隐藏层的维度

num\_layers: 堆叠的GRU的层数

bias: 是否添加bias项，可以有bias，也可以没有。weights和bias的初始化都是按照U(-根号(k),根号(k))，其中k=1/hidden\_size来做的。但是要和输入的h\_0有区别，当h\_0不以显式的方式提供时，h\_0 = 0!

batch_first：这是一个关于input和output的维度排列的参数。需要重点关注，默认情况下，input和output的都是seq\_len first的，input的格式如(seq\_len, batch, ...)，output的格式如(seq\_len, batch, ...)。设置该参数为True，则对应的input和output的维度可以对应得出。对比其他框架的使用体验，多是batch\_first，所以初次使用该函数，需要注意。见下图：

![img3](https://pytorch.org/tutorials/_images/seq2seq_batches.png)

dropout: 设置dropout率

bidirectional: 是否是双向GRU

通过上述七个参数，就可以搭建一个GRU的结构了。通常定义语句出现在类的\_\_init\_\_方法中，在forward函数中可以使用该定义，那么使用的时候需要考虑输入的类型。输入参数格式如下：

input: (seq_len,batch,input\_size)，主要注意的两个地方：第一是默认情况下是seq\_len优先的。第二是，如果想要处理变长序列，可以借助torch.nn.utils.rnn.pack_padded_sequence()来实现。

h_0: 如上图所示，在第一个时间步，需要一个初始化的隐藏层向量。其中格式为(num_layers\*num\_directions, batch, hidden\_size)

有了上述参数，模型已经可以执行forward函数了。那么，输出是怎么样呢？

output: 最后一层GRU，所有时间步的隐藏层向量。格式为(seq\_len, batch, num\_directions\*hidden\_size)，显然,

output.view(seq\_len, batch, num\_directions, hidden\_size)有时是很有用的。

通常来说，output是我们在使用RNN时比较关注的，但是在seq2seq框架下，我们希望得到最后一层，所有时间步的隐藏层向量，此处应用场景很多，不做过多阐述。

h\_n: (num\_layers\*num\_directions, batch, hidden\_size)，类比上述output，可以有：

h\_n.view(num\_layers, num\_directions, batch, hidden\_size)

上述描述包括三块内容，结构定义，input和output。其中需要重点关注的细节包括维度，初始化等。好了，可以测试一波了。用PyTorch可以获得非常棒的测试体验。代码如下：

```
import torch
gru = torch.nn.GRU(10,20,2)
input = torch.randn(5,3,10)
h0 = torch.randn(2,3,20)
output, hn = gru(input, h0)
```

完事儿，对一个函数的认识基本结束了。

沿着这种思路，类比可以快速Get到原生的RNN和LSTM的相关参数和注意细节。这里需要提示的是，PyTorch对原生RNN的参数说明中暴露了非线性函数的选择，可以使用tanh或者relu；LSTM相对于GRU，input中需要对记忆状态(cell\_state)初始化，同时output中有最后一层，所有时间步对应的记忆状态。在seq2seq框架中，LSTM将隐藏层状态hidden\_state和记忆状态cell\_state共同作为encoder端的输入的表示传递给decoder作为初始化向量。

上述描述的所有内容，目的都是搭建一个类似于下图的结构，

![img2](http://wx1.sinaimg.cn/mw690/aba7d18bgy1g0uer231rej20k807u75t.jpg)

这也是多数情况下，我们对RNN系的使用场景。但是，PyTorch为我们提供了更加灵活的Cell的定义。有了Cell，可以使用for-loop实现一个上述的结构。具体参数不再赘述，一个使用例子如下：

```
import torch
gru_cell = torch.nn.GRUCell(10,20)
input = torch.randn(6,3,10)
hx = torch.randn(3,20)
output = []
for i in range(input.shape[0]):
    output.append(gru_cell(input[i], hx))

```

总之，Cell接口的开放给我们提供了更加灵活的处理RNN系结构的能力，相信一定存在相应的模型场景，但是自己现在暂时没想到。

对比Tensorflow中实现地多个RNN系的版本，PyTorch中的RNN系要清晰的多。可以开心地复现模型了。

主要参考：

1.[PyTorch官方文档](https://pytorch.org/docs/stable/nn.html)

2.相关图片地址：[图片1](http://colah.github.io/posts/2015-08-Understanding-LSTMs/),[图片2](https://pytorch.org/tutorials/beginner/chatbot_tutorial.html), [图片3](http://colah.github.io/posts/2015-08-Understanding-LSTMs/)














