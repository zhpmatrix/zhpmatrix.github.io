---
layout: post
title: "Recursive Decompose for Noncovex Optimization"
tags: [深度学习]
excerpt: "论文阅读。这篇文章主要讨论了非凸优化问题的一种递归分解方法。"
date: 2017-05-17 18:00:00
mathjax: true
---
<script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=default"></script>

前言：相比于之前的论文笔记，这篇笔记侧重于大框架的梳理，帮助读者建立一个读该论文的初始印象。

#### Intuition&Motivation

AI中有很多问题是非凸的，即使使用**随机启动**和**模拟退火**策略，某些优化算法也容易陷入局部最优。作者观察到某些非凸目标函数的组合结构(递归结构)，想法也就来自组合优化(Divide&Conquer)。自己的理解是作者将超图分割用于目标函数的分割，主要是term之间分割，找到一个优化问题的递归描述，递归求解，也就是作者文章标题递归分解。(_昨天和老板讨论，老板说他当时看这篇文章，也就是看到图分割，就把想法写进基金本子了_)。

#### 伪代码

![rdis](http://wx1.sinaimg.cn/mw690/aba7d18bgy1ffvjj52045j20em0egtbm.jpg)

这是作者给出的伪代码，代码的整体结构上类似我[这篇](https://zhpmatrix.github.io/2017/05/11/adding-grouping-recursive/)文章中提到的。在那篇文章中提到的递归的并行，其实也是适合本文算法的并行化。伪代码中给出了三个子函数，**CHOOSEVARS**用于变量选择能够最大化的分割开目标函数，**SIMPLIFY**是用常数替换掉变量，该常数与term的bound有关，这样待优化的变量个数就减少了。在**SIMPLIFY**之后，**DECOMPOSE**就水到渠成。优化函数是*S*，分解后的问题就可以递归并行求解，子问题求解之后合并结果，也就是第11行代码的表示。第12和13行代码用于记录新的较小的值。分解目标函数的过程如下：

![recursive](http://wx2.sinaimg.cn/mw690/aba7d18bgy1ffvk7kebnyj20gp0aq412.jpg)

#### 基本概念

文章最重要的一个概念是**超图分割**，围绕这个概念，可以考虑的问题有：**什么是超图？**(在PaToH库中的manual中有非常具体的表示，不过这个manual有个小错误，很容易发现)**超图分割的依据是什么？**(与cut-set的cost有关)，**为什么超图分割可以用于非凸目标函数分解？**(个人认为是将目标函数用一个超图来表示，超边权值为1，但是具体的证明还没有读)

#### 代码实现

为了验证实验，我做了一个与粒子群优化(PSO)相关的目标函数，进行分割后，使用RDIS来求最值。下面是实验的过程。

1.多项式展开(matlab实现)

    syms s

    ps=((s^2+1))^3*(s+5)^2*(s^4+4*s^2+7)

    ps_new=expand(ps)

直接转换到最简项，这部分主要是关于**符号计算**的内容。论文给出的代码，要求代码的输入是化简到最简项的目标函数。

2.依赖库安装

mac下boost 1.55.0的安装可以参考9，默认安装路径/usr/local/include和/usr/local/lib,测试程序:

<script src="https://gist.github.com/zhpmatrix/f6879b053a0bdafb942a3deb801bfb2d.js"></script>

注意：可能不同的boost的版本的对应数据结构的路径不太一样，可以参照include中具体文件路径在头文件中引入。

代码的依赖库还有PaToH,在作者提供的代码中已经给出了预编译版本，故不需要重新编译。同时作者也提出可以使用别的超图分割库HMetis。此外，还有一个数值计算库levmar,不过HMetis和levmar都不是编译必须的依赖库。

3.代码结构

查看代码的树形目录结构:

    tree .

递归统计代码行数（非常优雅的方式）:

    find . -name '*.h' | xargs wc -l

**rdis的.h和.cpp文件共计16000+行！！！**RDIS算法的实现文件代码行2000+，每个优化函数的实现平均代码行300+。

4.编译调试

和读xgboost源代码方式类似，首先要在CMakeLists.txt文件中添加**-g**选项，使得程序可以用来调试。程序的代码量巨大，在编译的时候采用**make -j**，用来实现单机并行编译。类似提高编译速度的方式还有tmpfs（内存中编译）,distcc(分布式编译),ccache(缓存中间临时文件)。

5.代码阅读

代码的顶层调用逻辑：

    #选择子空间优化器(真正的优化器，对cutset相关的vertex优化求解)
    CGDSubspaceOptimizer ssopt( fpoly );
    
    #RDIS算法的优化求解
    RDISOptimizer opt( fpoly, ssopt, options );

    #计算目标函数的bound
    NumericInterval bounds = fpoly.computeBounds();
    
    #计算目标函数最优值
    Numeric val = opt.optimize();

    #计算目标函数最优值所在的位置
    State x = opt.getOptState();

6.关于智能指针的使用

shared_ptr,make_shared

7.boost的数据结构

tuple,graph,vector

8.代码优化

针对Cache的优化作者还没有做。

总结：本以为要Follow这篇文章，可是和老板讨论过后，老板建议去做Powell算法+互信息+图像配准相关，要做到**能用**。这篇论文是当年的最佳论文，最起码从工作量来说，实至名归。代码时间戳表示写了两年，同时文章做了三组实验，都是相对较大的实验。从思想来说，收到的启发还是如何将组合优化的策略和优化问题结合，同时Google了这篇文章其他人的follow，似乎不多呀。❤，❤️，🏀，一周多时间，没有严格意义的产出，淡淡的忧伤。

参考:

1.[Fiduccia-Mattheyses算法](http://blog.csdn.net/peterchan88/article/details/68952839)

利用FM算法对电路进行超图建模

2.[超图理论与应用PPT](https://wenku.baidu.com/view/6b1b0527a5e9856a56126021.html)

刘未鹏的PPT

3.[Levenberg–Marquardt算法学习](http://www.tuicool.com/articles/jEzaIbR)

从高斯牛顿算法讲到LM的优化，这二者的结果让我想到了带正则项的线性回归，这两个问题在解的形式上是类似的。同时谈到了上述两个算法和最速下降算法的联系，给出了两个具体的算法代码(C++)。比较了线性搜索和信赖域方法的对比。另外一个算法代码(matlab),[点击这里](http://www.cppblog.com/abilitytao/archive/2010/12/10/136058.html)

4.[LM算法浅谈](http://blog.csdn.net/liu14lang/article/details/53991897)

给出了一些推导，相对清晰。而且对LM的总结比较简洁。

5.[LM算法](https://wenku.baidu.com/view/b27b577d453610661ed9f4a8.html)

比较学术的资料。

6.[PaToH v3.2](http://bmi.osu.edu/~umit/software.html#datacutter)

7.[针对大规模机器学习和数据挖掘的超图并行计算框架](http://www.docin.com/p-1070025242.html)

硕士开题报告，在文章和作者关系这个问题的表达上，做了简单图和超图的对比。同时提出了Pregel和GraphLab的对比。

8.[ADMM算法原理和实例讲解](https://wenku.baidu.com/view/443092cb650e52ea54189840.html)

在RDIS算法中，子问题的Optimizer是选用共轭梯度法+LM算法，个人认为共轭梯度，坐标下降，ADMM方法均可以作为Optimizer。

9.[Mac下boost的安装与使用](http://blog.csdn.net/pyang1989/article/details/41725747)

10.[关于Linux静态库和动态库的分析](http://www.cnblogs.com/hzh1024n/archive/2009/09/17/1568357.html)

以问答的方式回答了关于静态库和动态库的关系，同时给出了关于动态库和静态库使用的例子。