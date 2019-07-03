---
layout: post
title: "[Pytorch]forward中的复杂tensor操作"
excerpt: "收集了一些在模型实现中可能会遇到的一些不太好写的tensor操作，后续持续补充中。"
date: 2019-07-03 18:43:00
mathjax: true
---

在[模型实现中的Debug问题](https://zhpmatrix.github.io/2019/06/30/model-debug-tips/)
这篇博客中，提到：**时间分配上，在得到一个可用的模型之前，我们80%-90%的时间都在debugging和tuning，只有10%-20%左右的时间在推导数学和实现（自己在基于Pytorch的模型实现中，80%的时间会花在forward中的复杂tensor操作）。**

因此，这里收集整理一些模型实现中的相对复杂的tensor操作。围绕tensor的操作，通常情况下可以看到两种call的方式，

第一：torch.；例如，torch.reshape()

第二：tensor.；例如，torch.randn(2,4).view(4,2)

具体地区分，在实现的时候可以查一下文档。

pytorch中forward函数的实现常见的有两个问题：

（1）不知道怎么实现。多数情况下是由于对tensor的操作不熟悉造成的，pytorch的tensor提供的基础操作可以灵活地解决很多问题。

（2）实现的部分操作不可导。自己的一个想法是多种矩阵乘法实现。

具体操作如下。

(1)**tensor转置的两个函数**（通过transpose可以实现permute）：

permute：对任意高维矩阵进行转置

transpose：对2维矩阵进行转置

(2)**tensor对dim=1的压缩和扩张**（当tensor中出现为1的dim时，可以使用。当出现多个dim为1时，可以通过dim的index指定要压缩和扩张的dim）：

squeeze:压缩

unsqueeze:扩张

(3)**掩码**

掩码操作在NLP的模型实现中应用较广，而且形式多变。关键函数是torch.masked\_select。比如，为了获得一个tensor中所有值大于0的元素，可以这样：

```
	threshold = 0.32
	x = torch.randn(2,4)
	mask = x > threshold
	torch.masked_select(x,mask)
```

也就是说，mask定义了一个operator，但是这个operator不是万能的，比如**不支持如下定义**：

```
	mask = (x > 0.5 and x < 1.0)
	
	mask = (x == 0.3)
```

(4)**数学操作（带有'_'的函数都是in-place,例如add\_, copy\_）**

mul, **div**, pow, sqrt, round, **argmax**, sigmoid, tanh, abs, ceil, **clamp**

(5)**tensor操作万花筒**

torch.cat: 合并多个tensor

torch.chunk：等分一个tensor；等等，还有一个切分函数torch.split，该函数是沿着某一个dim按照index选择，如下：

```
torch.index_select(torch.randn(3,4),0,torch.tensor([0,2]))
```

上述代码也就是选择第0和第2行。

torch.reshape: 改变tensor的形状

view: 改变tensor的形状，典型调用方式如torch.randn(3,4).view(4,3)

(6)**大杀器：torch.gather和torch.scatter\_**

scatter\_的用法示例：

```
x = torch.rand(2, 5)

y=torch.zeros(3, 5).scatter_(0, torch.tensor([[0, 1, 2, 0, 0], [2, 0, 0, 1, 2]]), x)

z=torch.zeros(2, 4).scatter_(1, torch.tensor([[2], [3]]), 1.23)
```


关于scatter\_，一个经典的应用场景是：将class标签转化为one-hot向量。如下：

```
class_label = torch.tensor([[2],[0],[1],[2]])
torch.zeros(4,3).scatter_(1,class_label,1)
```
对应的输出如下：

```
tensor([[0., 0., 1.],
        [1., 0., 0.],
        [0., 1., 0.],
        [0., 0., 1.]])
```

关于gather的使用，如下：

```
x = tensor([[0, 1],
        [2, 3],
        [4, 5]])
#index按照列看
torch.gather(x,0,torch.tensor([[0,0],[1,1],[1,0],[1,1],[0,2]]))
#index按照行看
torch.gather(x,1,torch.tensor([[0,0,0],[1,1,0],[0,1,0]]))
```

(7)**where(相当于c++中的三元操作符)**

```
	#如果x>0，对应位置为x的值，否则为y的值
	torch.where(x>0, x,y)
```

（8）**nozero（tensor中的bool类型）**

nozero返回的是0和1，结合其他条件可以实现选择特定元素。如下：

```
x = torch.arange(12).view(3,4)
(x>4).nonzero()
```


 


 





