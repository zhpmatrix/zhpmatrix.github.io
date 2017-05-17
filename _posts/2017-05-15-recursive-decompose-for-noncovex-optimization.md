---
layout: post
title: "[Optimization]针对非凸优化的递归分解"
excerpt: "这是一篇论文笔记(无组织，无纪律)，来自IJCAR2015 BestPaper,Pedro Domingos的作品，《Recursive Decomposition for Nonconvex Optimization》文中提出了RDIS算法。"
date: 2017-05-15 23:03:00
mathjax: true
---
<script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=default"></script>

#### 基本概念

1.超图(Hypergraph)理论

  超图分割,图分割和简单图分割

3.Fiduccia-Mattheyses算法

4.共指消解(Coreference Resolution)


#### 优化算法

1.multi-start 共轭梯度算法

2.Levenberg-Marquardt算法

上述算法是Bundle Adjustment思想的一个应用。

如果下降太快，使用较小的λ，使之更接近高斯牛顿法 
如果下降太慢，使用较大的λ，使之更接近梯度下降法

3.非线性最小二乘问题

4.Powell函数

Powell算法是求解无约束优化问题的算法，Powell函数具有的特点是**"误差项的平方和"**形式。

下降关系与semiring的关系(SubspaceOptimizer.h)

共轭梯度下降和NRC优化方法(CGDSubspaceOptimizer.h),在代码中NRC优化方法出现的方式是预先编译。

LM算法和box-constrained minimization的关系

5.SubOptimizer

共轭梯度算法和Powell算法

#### 代码实现

1.多项式展开(matlab实现)

    syms s

    ps=((s^2+1))^3*(s+5)^2*(s^4+4*s^2+7)

    ps_new=expand(ps)

直接转换到最简项，这部分主要是关于**符号计算**的内容。

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

rdis的.h和.cpp文件共计16000+行！！！

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