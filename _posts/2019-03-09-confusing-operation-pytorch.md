---
layout: post
title: "代码复现时的拦路虎-维度操作"
tags: [PyTorch]
excerpt: "可能是多数萌新在代码复现时遇到的最大的问题，shape不对齐。这篇博客目的就是讨论这些基础操作，以求复现时的随心所欲。"
date: 2019-03-09 18:43:00
mathjax: true
---

<script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=default"></script>

### 前言:

PyTorch封装了numpy的大部分操作，二者之间通常可以实现无缝的切换。比如，从numpy到PyTorch的转化，通过from\_numpy()；从PyTorch到numpy的转化通过.numpy()。知道二者之间的联系之后，如果遇到PyTorch中存在numpy不支持的操作，一个很直观的想法是将PyTorch的Tensor转化为numpy，实现相关操作后，再打包回PyTorch。

这部分内容主要包括如下：

1. Tensors相关：创建OPs(torch.ones()类似)，索引，切片，联合和分割等；

2. 随机化；

3. 序列化；

4. 并行化；

5. 梯度计算的局部取消；

6. 数学操作：逐点操作，规约操作，比较操作，BLAS&LAPACK操作等。

7. 一个工具函数：torch.compiled\_with\_cxx11\_abi()

PyTorch提供了模型实现的多数部分，但是细节部分很多时候需要从上述几个方面来扣，重点如1，5，6三个模块。这篇博客主要结合自己的使用经历，围绕1来进行一些关键OP的梳理和回顾。

需要提示的是，这部分的内容主要参考官方文档的torch模块，实际上torch.Tensor模块有些功能存在重叠，可以参考2进行了解。二者的区别如下：

torch中对data的操作：torch.narrow(data,...)

torch.Tensor中对data的操作：data.narrow(...)

也就是说，存在某个OP，有三种实现：numpy，torch，torch.Tensor。在自己写代码的时候，个人感觉还是要尽量保持一致，但是读代码的时候难免会遇到上述情况混合杂糅的场景。

### 重点操作

#### 1.torch.cat(tensors, dim=0, out=None)->Tensor

第一个参数是tensors而非tensor,需要注意的是当tensors非空的时候，除了cat的维度，tensors中tensor的其他维度必须相同，这很容易理解，不相同就没了cat的意义了。在MySQL中的一个经典问题是表的水平/垂直的合并/切分，因此数据库领域中的一个想法对于了解这些基本操作也是大有裨益的。从这个操作来看，既然有合并，必然有分割，也就是反操作。对应的反操作有两个torch.split()和torch.chunk()。chunk()是将Tensor沿着某个dim平均切分，返回的是一个Tensor列表。此处需要考虑的问题就是不等分的情况了，在PyTorch中，这个问题处理的很好，不等分就保留余数。不仅在此处，在其他多个地方遇到不等分的情况，都基本可以认为保留余数。split()的一个功能是实现不等分，可以按照自己想要的切分比例来划分，通过传入参数split\_size\_or\_sections来控制。当传入一个列表时，表示每个chunk想要的size；当传入一个整型数时，表示等分，也就是单个chunk的大小。该函数返回的是tuple类型。

对比split和chunk，处理返回类型的区别外，传入参数的区别在于前者传入的是分割后每份的大小，而后者则传入的是分几份的问题。虽然存在区别，但是又存在功能上的区别。

既然是合并，还有一个非常有意思的函数torch.stack()，目的是将一个输入Tensor列表沿着某个维度进行堆叠，要求列表中的所有Tensor都是shape一致的。该函数在自己的使用经验中也是常见的。

#### 2.torch.gather(input, dim, index, out=None)->Tensor

对于这个函数的理解，可以从两段代码来看，如下：

```
data = torch.Tensor([[1,2,3],[4,5,6]])
print(data)
index_1 = torch.LongTensor([[0,1],[2,0]])
index_2 = torch.LongTensor([[0,1,1],[0,0,0]])
print(torch.gather(data, dim=1, index=index_1))
print(torch.gather(data, dim=0, index=index_2))
```

输出结果如下：

```
1  2  3
4  5  6
[torch.FloatTensor of size 2x3]


1  2
6  4
[torch.FloatTensor of size 2x2]


1  5  6
1  2  3
[torch.FloatTensor of size 2x3]
```

关于该函数的使用，给出一个经典的场景。多分类问题中，对标签one\_hot编码后，会得到一个标签的one\_hot\_label矩阵。模型的预测输出是一个logits矩阵，那么为了得到对应真实标签的预测值，怎么做？

假设one_hot矩阵为(batch, N)，其中N表示类别数目；logits矩阵为(batch, N)，则，

```
torch.gather(logits, dim=1, index=torch.max(one_hot_label, dim=1)[1].reshape(one_hot_label.shape[0],1))   

```

从整体上看，gather实现的功能是沿着某个dim取出对应值，给定dim后，就可以沿着dim进行index了，这是一个非常有趣的实现。不过，上述一行代码显然不够PyTorch呀。

#### 3.torch.reshape(input, shape)->Tensor

这是一个使用频率非常高的函数。关于该函数需要注意的有两个地方。第一：纯PyTorch的写法，杜绝data.reshape(),使用torch.reshape(data,...)；第二：copying和viewing的关系。见官方文档对这一问题的讨论。

When possible, the returned tensor will be a view of input. Otherwise, it will be a copy. Contiguous inputs and inputs with compatible strides can be reshaped without copying, but you should not depend on the copying vs. viewing behavior.

经常看到代码中numpy和PyTorch的操作混合使用，虽然这是一个PyTorch的优点，但是总觉得代码很乱，体验很差，要尽可能PyTorch化呀。

一个很微妙的地方在于，reshape表面上是可以实现转置的，但是是shape依赖的。转置的事情还是交给PyTorch吧，比如这个函数torch.t(input)->Tensor。该函数的扩展版是torch.transpose(input, dim0, dim1)->Tensor，所以，

torch.t(input)等价于torch.transpose(input,0,1)。

此处，体现了使用PyTorch的一个思维：把对函数的理解放到多dim场景下。


#### 4.torch.squeeze(input,dim=None, out=None)->Tensor

在实现时，有时候会得到某个dim的长度为1的情形，只有一个元素，那就不要嵌套了吧。缺点至少有两个，第一是增加了dim的数量；第二是访问元素的时候需要显式的data\[0\]，不能直接用data。PyTorch说，我来帮你删掉这些冗余的dim吧，于是给我们送来了torch.squeeze(...)。直观地讲，比如：

输入的shape是(Ax1xBx1xC)，输出的shape就是(AxBxC)了。既然默认是全部压缩掉，但是有些情况可以只压缩某一个dim的，这也就是接口中dim的存在意义了。但是，值得注意的是：

If input is of shape: (Ax1xB), squeeze(input, 0) leaves the tensor unchanged, but squeeze(input, 1) will squeeze the tensor to the shape (A×B).

也就是虽然指定了dim，但是该dim不可压缩，那么就保持原来状态吧。个人不是很喜欢这种方式，但是暂时想不到什么比较好的方式。

当然存在一个反操作，torch.unsqueeze(input, dim,out=None)->Tensor。这其实是一个非常有用的函数，相信在多数场景下都会遇到。将torch.Size(\[4\])变为torch.Size(\[1,4\])或者变为torch.Size(\[4,1\])。

上述操作当然可以通过reshape等操作实现。

#### [非主流系列]5.torch.where(condition, x,y)->Tensor

比较相同shape的两个tensor，按照condition从x或者y中选择元素落位合并成新的tensor。

#### [非主流系列]6.torch.take(input, indices)->Tensor

将一个tensor中的所有元素合并成一个列表，通过给出indices，取得indices对应的元素。在实现上猜测reshape类似。

#### [非主流系列]7.torch.nonzero(input, out=None)->Tensor

给出tensor中所有的非零元的位置。

#### [非主流系列]8.torch.narrow(input,dimension,start,length)->Tensor

更加灵活的tensor元素获取方式，可以对比上述1和2的描述，实现一些需要更加灵活控制的函数。

#### [非主流系列]9.torch.masked\_select(input, mask, out=None)->Tensor

在NLP的一些模型实现中，重要性不言而喻。mask矩阵是一个01矩阵，对应位置的input的元素输出。

#### [非主流系列]10.torch.index\_select(input, dim, index, out=None)->Tensor

沿着某一维度，按照index选择部分tensor的数据。对比使用参考1，2和8。

主要参考：

1.[torch模块官方文档](https://pytorch.org/docs/stable/torch.html#)

2.[torch.Tensor相关操作](https://zhuanlan.zhihu.com/p/31495102?utm_source=qq&utm_medium=social&utm_oi=52727124066304)

3.[torch.Tensor模块官方文档](https://pytorch.org/docs/stable/tensors.html#)












