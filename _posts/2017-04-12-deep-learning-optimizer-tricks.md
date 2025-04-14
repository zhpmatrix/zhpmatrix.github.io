---
layout: post
title: "Deep Learning Optimizer Tricks"
tags: [深度学习]
excerpt: "论文阅读。这篇文章主要讨论了深度学习中的优化技巧。"
date: 2017-04-12 18:00:00
mathjax: true
---
<script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=default"></script>

看图说话，比较一下常见优化算法在正常和非正常(saddle point)情况下的表现。

**正常情况下：**

![Algs Compare](http://wx2.sinaimg.cn/mw690/aba7d18bgy1fehvxkvlclg20h80dc4n1.gif)

图片来源: Alec Radford

对比六种优化算法，Adagrad,Adadelta,Rmsprop能够很快的找到minimum，而Momentum和NAG则随之到来，而SGD奔着目标，姗姗来迟。

鞍点附近情况:

![saddle point 1](http://wx2.sinaimg.cn/mw690/aba7d18bgy1fehvvz9orng20h80dc1ca.gif)

_下面是一张看起来不那么好的的图_

![saddle point 2](http://wx3.sinaimg.cn/mw690/aba7d18bgy1fehvy2j12ug20h80dc7lw.gif)

图片来源: Alec Radford

这是六种优化算法在鞍点处的表现，Adadelta表现出色，悲剧了SGD。

---

在利用SGD作优化算法的时候，会面临两个困难：

*1.* 怎样选择合适的学习率？

相比于BGD，SGD收敛速度快，但是精度略差。如果学习率较小，收敛更慢，反之如果学习率较大，在靠近最小点附近，由于梯度较小，会导致震荡(Rosenbrock函数)以至于发散(步子太大，没有扯着'0'，囧)。针对学习率的选择有一些解决方案，例如模拟退火，不是一味的下降，适当爬山，可能跳出小水沟，找到真正的深井。同时有一些在训练开始前定义的预调度策略，但是采用这种方式不能很好地适应数据集的特性。采用相同的学习率对不同的参数进行更新而不考虑数据和特征也是不合适的。

*2.* 鞍点的问题？

采用SGD对非凸问题进行优化的时候，会陷入鞍点困境(saddle point)。

为解决上述问题，学术界做出了一系列算法改进工作。DL中常常使用基于梯度的改进优化算法，也就是一阶优化算法。DL中参数众多，计算量大，所以简单work的方案总是会受到青睐。

1.动量方法(Momentum)

没有用Momentum之前是这个样子的：

![before](https://www.willamette.edu/~gorr/classes/cs449/figs/valley1.gif)

在走向minimum的过程中，如果方向是对的，那就加速，如果方向是错的，那就刹车。想像一个场景，站在山顶向山底滚动一个巨大的球，在滚向山底的过程中，由于惯性的作用，球会越滚越快，但是当球滚过山底时，滚向对面山顶的过程中，球会越滚越慢。惯性是保持事物本来运动状态的一种性质，在问题1中提到，如果学习率设置不合适，在接近minimum的时候，由于梯度较小，梯度更新较大，会跨过minimum，继而形成震荡，如果我们在寻找minimum的过程中，使得在搜索方向错误的时候，梯度更新不要太冒险，或许可以在一定程度上解决这个问题，**不要太冒险，就要尽量保持原来状态**。

更新表达式：

$$\nu_t=\gamma\nu_{t-1}+\eta\nabla_\theta J(\theta)$$

$$\theta = \theta - \nu_t$$


自从使用Momentum之后是这个样子的(卖钙片滴)：

![after](http://wx2.sinaimg.cn/mw690/aba7d18bgy1fes5em9gurg20be04uwe9.gif)


2.Nesterov Accelerated Gradient(NAG)

Geoffrey Hinton在lecture中的描述是这样的：

- First make a big jump in the direction of the previous accumulated gradient.
- Then measure the gradient where you end up and make a correction.

表达式如下:

$$\nu_t = \gamma\nu_{t-1}+\eta\nabla J(\theta-\gamma\nu_{t-1})$$

$$\theta = \theta - \nu_t$$

在上式中，可以认为\\(\theta-\gamma\nu_{t-1}\\)是参数下一个位置的近似。Momentum和NAG的区别如下(来自Hinton课件)：

![pic](http://wx1.sinaimg.cn/mw690/aba7d18bgy1fej0qns796j20lt06c759.jpg)

蓝色向量表示动量方法，其中较短的蓝色向量表示计算当前梯度，较长的蓝色向量表示big jump(\\(\gamma\nu_{t-1}\\))。 其余向量表示NAG方法的两个迭代过程，左侧棕色向量表示big jump, 红色向量表示计算当前梯度\\(\nabla J(\theta-\gamma\nu_{t-1})\\)，绿色向量表示合成的更新参数\\(\nu_t\\).

3.Adagrad

在问题1中谈到有些场景下不同的参数对应的学习率不同，adagrad实现了这个目标。Jeffrey Dean在Google的从Youtube视频中识别猫的神经网络训练中用到这个方法来提高SGD的鲁棒性，同时也实现了稀疏场景下的学习问题。表达式如下:

\\(g_{t,i} = \nabla_\theta J(\theta_i)\\)表示目标函数在\\(t\\)步中在\\(\theta_i\\)的梯度，则对传统SGD有\\(\theta_{t+1,i}=\theta_{t,i}-\eta g_{t,i}\\)，而adagrad的更新方式为：

$$\theta_{t+1,i}=\theta_{t,i}-\frac{\eta}{\sqrt{G_{t,ii}+\epsilon}}g_{t,i}$$

其中，\\(G_t \in R^{dxd}\\)是一个对角矩阵，对角上的元素\\(i\\)为\\(\theta_i\\)的历史值的平方和，\\(\epsilon\\)是为了防止分母为0的项，通常取值为\\(1e-8\\),\\(\eta\\)通常不需要调整，默认值\\(0.01\\)。此处也正是adagrad缺点的体现，随着训练过程的进行，分母越来越大，导致学习率变小，学习不足。

4.Adadelta

在Adagrad方法中, \\(G_t\\)中的元素是历史值的平方和，Adadelta对于Adagrad中的改进主要是**采用一个固定窗口内的值的平方和的平均**。第\\(t\\)步对应的值为：

$$E[g^2]_t=\gamma E[g^2]_{t-1}+ (1-\gamma)g_t^2 $$

同时有：

$$\triangle\theta_t = -\frac{\eta}{\sqrt{E[g^2]_t+\epsilon}}g_t$$

用新的记号\\(RMS[g]_t\\)来重写上述分母，有：


$$\triangle\theta_t = -\frac{\eta}{RMS[g]_t}g_t$$

针对\\(\eta\\)的改进是：

$$\eta = RMS[\triangle\theta]_{t-1}=\sqrt{E[\triangle\theta^2]_{t-1}+\epsilon}$$

最终的表达式是：

$$\triangle\theta_t = -\frac{RMS[\triangle\theta]_{t-1}}{RMS[g]_t}g_t$$

$$\theta_{t+1}=\theta_t+\triangle\theta_t$$

从上面可以看出，Adadelta的关键是固定窗口而非历史所有值的利用，学习率不需要调整。

5.RMSprop

RMSprop没有经过正式发表，是Geoffrey Hinton在课上提出的，是Adadelta对学习率不改进前的版本，其中\\(\gamma=0.9\\),\\(\eta=0.001\\),想到自己在《神经网络》课程上的大作业中，利用keras做一个分类问题利用的优化方法就是RMSprop。

6.Adam

Adam的全称是Adaptive Moment Estimation,是一种对不同参数更新计算不同学习速率的新方法，同样要维持一个关于梯度的指数衰减平均。更新规则如下：

$$m_t = \beta_1 m_{t-1}+(1-\beta_1)g_t$$

$$\nu_t = \beta_2 \nu_{t-1} + (1-\beta_2)g_t^2$$

$$\hat{m}_t=\frac{m_t}{1-\beta_1^t}$$

$$\hat \nu_t = \frac{\nu_t}{1-\beta_2^t}$$

$$\theta_{t+1}=\theta_{t}-\frac{\eta}{\sqrt{\hat{\nu}_t}+\epsilon}\hat{m}_t$$

作者给出的参数默认值是\\(\eta=0.001,\beta_1=0.9,\beta_2=0.999,\epsilon=10^{-8}\\),其中\\(m_t\\)和\\(\nu_t\\)分别是第一动量和第二动量(梯度平方)的估计,\\(\hat{m}\\)和\\(\hat \nu_t\\)是对动量估计的修正方式。

【补充】：史春奇在[文章](https://mp.weixin.qq.com/s?__biz=MzIzMjU1NTg3Ng==&mid=2247485870&idx=1&sn=3c40e9a2865dd45fbe14f745be62315f&chksm=e8925da5dfe5d4b30f05b19b55e313adc493e026d646004927dea299ecaeb0e6c8ddca9c8a74&mpshare=1&scene=23&srcid=07064tSquHJV9jnQTeqYqKUk#rd)中谈到为什么主流平台都实现该优化算法？

1.实现简单

2.计算高效，动量+自适应，提高了收敛速度

3.内存消耗小，更新完就丢

4.**对于极具变化，带噪声，甚至稀疏的梯度能够较好的适应** 

5.不太需要人工干预，初始化和调参不需要高级技巧(_这点从主流平台的参数设置也可以看出_)


#### 如何选择优化算法？

实际情况下，现在的一些文章还是使用标准SGD算法和一个简单的学习率退火调度过程来训练模型。在很多场景下，RMSprop，Adadelta和Adam表现几乎一样，但是在某些场景下，Adam的表现较优与其他算法。

**结合分布式场景，SGD如何优化？**

典型的算法有Hogwild!,Downpour SGD,Delay-tolerant Algorithms for SGD,Elastic Averaging SGD等。

同时有一些其他策略：Shuffling and Curriculum Learning,Batch Normalization,Early stopping,Gradient noise等。

**总结**：本篇博客以DL领域中的优化review为纲，梳理了常用的优化算法。对比在之前的文章中反复提到的Bottou关于SGD的review文章，前者主要围绕学习率和saddle point来考虑，后者则关心noise和二阶信息的利用。而在noise处理方面，和DL中的优化策略类似，是对当前梯度信息和历史梯度信息的共同使用。二阶优化方法是为了挖掘更多可利用信息，而一阶优化是为了更好的利用历史信息。

**参考**：

1.[An Overview of Gradient Descent Optimization Algorithm](http://sebastianruder.com/optimizing-gradient-descent/index.html#challenges)

2.[算法优化之道：避开鞍点](http://mp.weixin.qq.com/s?__biz=MzAwNDI4ODcxNA==&mid=404482412&idx=1&sn=3fb245d1893487a1beaa6abd56147b30&scene=25#wechat_redirect)

3.[Momentum and Learning Rate Adaptation](https://www.willamette.edu/~gorr/classes/cs449/momrate.html)

4.[迭代优化算法之直观概述](http://mp.weixin.qq.com/s?__biz=MzIzMjU1NTg3Ng==&mid=2247483805&idx=1&sn=83f2e6e1e9f021e9227ef2fbbcefbeda&chksm=e8925596dfe5dc80844b67e5e020ee2e7b79b00bc95184fcb0ab0f08d03793441beea2d2e97c&mpshare=1&scene=23&srcid=0504OdKe8hESi7SWQS9TSL76#rd)

文章中有一张更细致的优化算法关系图，同时对近期的经典优化算法进行了实验上的对比。