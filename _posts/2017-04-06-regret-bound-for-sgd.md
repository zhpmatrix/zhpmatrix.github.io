---
layout: post
title: "[Optimization]SGD的regret bound分析"
excerpt: "从一个bound的推导来感受优化中的数学，SGD的次线性收敛来源。"
date: 2017-04-06 20:40:00
mathjax: true
---

<script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=default"></script>

这篇短文假定读者了解SGD，故对SGD的过程不做描述。开篇吐槽markdown中写latex，然后push到Github的过程有多么的不爽，我现在还没有找到一个更舒服的表达的方式，所以可能文中涉及的公式显得有点ugly!阅读完这篇文章的目的在于让读者感受到原来读懂优化理论中的证明并不是特别困难，以此建立对对优化的感性认识。

已知SGD的参数更新过程为:

$$w_{k+1} = w_{k}-\alpha_{k}g(w_{k},\xi_{k})$$

利用regret分析有:

<img src="http://latex.codecogs.com/gif.latex?\Vert{w_{k+1} - w_{*}}\Vert_{2}^{2} - \Vert{w_{k}-w_{*}}\Vert_{2}^{2}="/>

$$2(w_{k+1} -w_{k})^{T}(w_{k} - w_{*}) + \Vert{w_{k+1}-w_{k}}\Vert_{2}^2 \\ $$

$$ = -2\alpha_{k}g(w_{k},\xi_{k})^{T}(w_{k}-w_{*}) + \alpha_k^2\Vert{g(w_{k},\xi_k)}\Vert_{2}^{2} (1) $$


将上式看做一个关于:

$$a^2 - b^2 = (a+b)(a-b)$$

的不等式变换过程，进行项的拆分和合并，注意向量和变量乘法的不同，然后带入SGD的更新式子就可以。矩阵本身是一个线性变换，而矩阵的norm表示矩阵的大小，上式是一个比大小的过程，用来衡量每次更新完参数之后得到的参数改进幅度，这其实也是regret分析的想法。

我们经常提到凸问题的假设，看看这个假设可以为我们带来什么？

<img src="http://latex.codecogs.com/gif.latex?F(w_{k}) - F(w_{*}) \geq g(w_{*})^T(w_{k} - w_{*})     (2)"/>

上述不等式学名叫做SubGradient Inequality。注意我们假设目标函数是凸函数，这里目标函数的含义可以包含正则项，也可以不包含，但是有时候正则项由于非光滑不可导，导致目标函数非凸，问题也就变得稍微复杂了些。由于\\(F(w_{k})\\)是第\\(k\\)次迭代后目标函数的值，而\\(F(w_{*})\\)表示对应最优参数\\(w_{\*}\\)下的目标函数的值，故显然：

$$ F(w_{k}) - F(w_{*}) \geq 0$$

对\\(F(w_{k})\\)在\\(w_{k}\\) = \\(w_{*}\\)处Taylor展开：


<img src="http://latex.codecogs.com/gif.latex?F(w_{k}) \geq F(w_{*}) + g(w_{*})^T(w_{k} - w_{*})" />

注意，此处我们假定了
<img src="http://latex.codecogs.com/gif.latex?g(w_{*})^T(w_{k} - w_{*}) \geq 0"/>


在进行下一步的说明之前，我们进行一个符号的陈述：用\\( f(w_{k};\xi_{k}) \\)和\\( f(w_{\*};\xi_{k}) \\)分别表示\\( F(w_{k}) \\)和\\( F(w_{*}) \\),用\\( \nabla f(w_{k};\xi_{k}) \\)来表示\\( g(w_{k},\xi_{k}) \\),这里，\\(\xi_{k}\\)表示SGD随机选取的样本。则：

<img src="http://latex.codecogs.com/gif.latex?||w_{k+1} - w_{*}||^2 - ||w_{k} - w_{*}||^2 \leq -2\alpha_{k}(f(w_{k};\xi_{k}) - f(w_{*};\xi_{k})) + \alpha_{k}^2|| \nabla f(w_{k};\xi_{k}) ||^2     (3)" />



(3)很容易由(1)和(2)得到。

为了进一步的推导，我们给出两个非常重要的假设:

$$
|| \nabla f(w_{k};\xi_{k}) ||^2 \leq M (4)
$$

$$
||w_{k} - w_{*}||^2 < B (5)
$$

其中(4)和（5）满足：\\(M > 0,B > 0\\) for all k \\( \in \mathbb{N}\\)

进而得到:

<img src="http://latex.codecogs.com/gif.latex?\alpha_{k+1}^{-1}||w_{k+1} -w_{*}||^2 - \alpha_{k}^{-1}||w_{k}-w_{*}||^2 \leq -2(f(w_{k};\xi_{k})-f(w_{*};\xi_{k}) + \alpha_{k}M + (\alpha_{k+1}^{-1} - \alpha_{k}^{-1})||w_{k} - w_{*}||^2 \leq -2(f(w_{k};\xi_{k})-f(w_{*};\xi_{k}) + \alpha_{k}M + (\alpha_{k+1}^{-1} - \alpha_{k}^{-1})B" />

对不等式左右两边求和：其中\\(\alpha_{k} = 1/\sqrt{k}, k={1,2,...,K}\\)有：

$$
\left(\sum_{k=1}^{K}f(w_{k};\xi_{i})\right) \leq \left(\sum_{k=1}^{K}f(w_{*};\xi_{i})\right)+M\sqrt{K}+o(\sqrt{K})
$$

上式的得到需要计算一个积分，三个迭代求和，同时涉及算法时间复杂度的o(small)的概念定义。如果将上式的左边第一项移到右边，则右边合并同类项之后的结果大于等于0，想想为什么？**上式对任何噪声序列\\({\xi_k}\\)成立**。


如果**假设噪声序列独立**，可以得到更一般的形式：

$$
\mathbb{E}\left[ \frac{1}{K}\sum_{k=1}^{K}F(w_{k})\right] \leq F_{*} + O(\frac{1}{\sqrt{K}})
$$

一般形式的得到需要不等式两边同除一个常数，重新调整算法时间复杂度的界，得到O(Big)的表达。

在li Ita@Zhihu中的一篇文章中提到: 在SGD的收敛性分析中需要假设样本梯度的的方差是有常数上界的，然而正是因为这个常数上界导致了SGD无法线性收敛。

在我们的这篇文章中，可以看到实际上SGD的次线性收敛需要依赖的假设不仅有样本梯度大小的上界，还有参数更新大小的上界。实际上，学术界有很多人在不断的改进SGD算法，使其达到线性收敛的速度，类似的工作在li Ita的专栏文章中有提到。

总结：在本篇文章中，从SGD的regret分析中来品味优化过程，从问题定义到推出bound，涉及到很多细节。典型的有：问题的假设，矩阵范数的计算和意义，简单不等式的计算(有时会有复杂trick)，随机变量独立性，时间复杂度的基本概念，微积分，迭代思想等。自己认为这里的关键是对问题的假设，一般文章中给出的证明是先给出假设，在假设意义显著的前提下，这种给出假设的方式是合理的，但是纯数学理论推导的前提下给出的假设可能是由果索因的产物，同时假设对于最终结论的得出起着决定性作用。文中用简单优雅的方式得出了一个SGD中非常重要的一个结论，从证明过程中来看，似乎涉及的数学并不困难，但是如何系统的证明，可能才是真正的难点。

参考:

1.[Optimization Methods for Large-Scale Machine Learning](http://xueshu.baidu.com/s?wd=paperuri%3A%28972713604bb4784237ea58a8a34f65b9%29&filter=sc_long_sign&tn=SE_xueshusource_2kduw22v&sc_vurl=http%3A%2F%2Farxiv.org%2Fabs%2F1606.04838&ie=utf-8&sc_us=8945861777932518409)

Leon Bottou是SGD的作者，他以一作身份在2016.06.16当天在Arxiv上挂出这篇review，内容全面，值得一读！

![Bottou](http://wx1.sinaimg.cn/mw690/aba7d18bgy1fec3aonut9j2023023742.jpg)

放上一张Bottou的照片，以此感谢。

2.[线性收敛的随机优化算法 之 SAG、SVRG](https://zhuanlan.zhihu.com/p/22402784)

这篇文章是因为看到作者投NIPS 2016年没有中的一篇文章的时候，偶然间搜索到的作者写的专栏文章，在博客中，我引用了其中的一段话，当然，这篇专栏文章也是很值得读一读，关于SAG和SVRG，或许后续有时间的时候也要写一篇相关文章。



    