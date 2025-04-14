---
layout: post
title: "逻辑回归并行化"
tags: [工程架构]
excerpt: "讨论了并行化的一些话题，对于逻辑回归用于分类问题，采用MPI进行并行化，优化过程采用批量梯度下降(BGD)"
date: 2017-03-14 20:23:00
---

逻辑回归(Logistic Regression)是用于解决二分类问题的一种方法，本质上一种线性分类器。在工业界推荐系统的实践过程中，LR是"大红人"，曾经有人开玩笑说，"一招鲜，吃遍天"，理由是LR的可解释性，易控性。同时，在机器学习面试中，LR的推导通常是必知必会的内容，至于LR的原理，由于相对简单，不是本文的陈述重点，本文重在讨论LR并行化过程中踩过的"坑"，并且为了简化问题，使用了批量梯度下降(BGD)做参数更新。

---


![regression](http://wx4.sinaimg.cn/mw690/aba7d18bgy1fdmnie82vzj20hs0dcgoo.jpg)

---


#### 一.基准程序

刘文志在《并行算法设计与性能优化》中提出了14个并行算法设计的一般准则，最后一条是"步步验证"。验证需要一个基准程序，也就是一个串行LR版本。在[矩阵乘法的分布式实践](https://zhpmatrix.github.io/2017/03/06/matrix-multiplication-mpi-openmp-cuda/)中，我们谈到了加速比和效率两个衡量指标，基准程序是一个串行矩阵乘法版本。在编写串行LR的时候，为了更好的支持向量化和矩阵运算，引入了[Eigen](http://eigen.tuxfamily.org/index.php?title=Main_Page)库的使用。由于代码采用C++编写，我们不用自己去实现基本矩阵运算，这大大提高了我们的开发效率，[代码这里](https://github.com/zhpmatrix/parallel-computing/blob/master/LogisticRegression_with_MPI/base_lr.cpp)。一个基准程序的存在满足了我们性能考察和步步验证的目的。

#### 二.并行程序

我们在基准程序中的训练数据包括两种类别：随机生成数据和文件数据。考察算法的并行性的时候，通常要考虑任务并行和数据并行。分析串行代码，在数据量大的时候，显然，参数更新过程是热点，热点通常是计算密集的部分，但是也可能是IO密集的部分。并且由于采用BGD做参数更新，满足数据独立性，所以我们的重点在于数据并行化，简单来说，就是对求和的分解，这个过程可以参照矩阵乘法的过程，按照起始地址和偏移量进行数据分发。在计算节点进行参数更新，然后将更新后的参数发送给管理节点，管理节点做参数累和后作为权值的更新值。重复这个过程，直到满足迭代条件，比如500次迭代上限。

算法伪代码如下：

    设置参数，例如最大迭代次数，学习率，初始权重等；
    Repeat Until MaxIterTimes{
        训练数据分发给计算节点；
        计算节点参数更新；
        计算节点将更新后参数发给管理节点；
        管理节点收集参数做累和后更新参数；
    }

这样我们就实现了一个简单的LR的并行版本。回顾上述过程，一个明显的缺点是管理节点在每次迭代的时候又重新分发了一次训练数据，这是不必要的。对训练数据的使用，一次分发，多次使用。

#### 三.踩坑经历

1.MPI_Send和MPI_Recv使用。MPI_Recv在接收数据的时候，接收顺序最好和MPI_Send顺序保持一致，否则会发生消息截断错误：
    
    MPI_ERR_TRUNCATE:message truncated
    
问题的关键是，MPI只能返回这些错误信息了。所以，由于小疏忽导致的问题，可能实际解决起来相对困难。在写代码的过程中，这个问题困扰了自己好长一段时间，最后是由于自己在不断试错的时候，由于不经意调整了两行代码的位置，运行OK才发现了这个问题。注意，使用MPI的时候，DEBUG确实是一个问题！

2.Eigen的使用。

在串行程序中，Eigen是有力工具，但是由于使用MPI进行数据分发，MPI对Eigen内置的矩阵结构MatrixXd支持较差，这让我联想到不知道MPI对于STL的支持怎样。在代码调试的时候，GDB就不支持STL，导致调试困难，但是已经有些解决方案，LLDB对于STL的支持非常好。由于MatrixXd的特殊性，必须做一个trade-off。所以，我的做法是，做MatrixXd和Array互相转换的接口，在发送MatrixXd的时候，转换为Array进行数据分发，接受到Array之后，恢复为MatrixXd进行矩阵运算。这实际上添加了转换开销，但是目前我们实际上做了一件历史串行程序并行化的工作，如果历史程序较大，重写为原生Array的时间成本较大，所以，我们只能在通信的时候，加厚通信层，进行数据转换。

由于MatrixXd的使用，这同时带来了一个问题。在矩阵乘法一文中，我们提到了在多CPU环境下，采用MPI通信，在单机多核环境下，可以采用OpenMP的方案进行加速，但是OpenMP加速针对的是原生for循环。在计算节点接受到原生Array之后，为了方便矩阵计算，我们将其转换为MatrixXd，此处如果为了单机加速，从MatrixXd拆解出for来，已经背离初衷了。如果这样，我们可以在接受到Array之后，直接for循环计算，或者更彻底的解决方案，代码全部使用原生Array。

3.程序正确性验证。

在第一版代码中，由于没有进行程序正确性的步步验证。程序"正常运行"，但是和串行结果不一致。然后就进入了步步验证的过程，在步步验证的时候，发现了由于数据类型转换的问题，导致数据接收不正确。串行程序并行化，应该是在保证正确性的前提下加速，保证正确性的第一步通常是理论证明，我们的并行LR方案很容易证明正确，其实是保证程序运行正确，也就是程序输出和期望输出保持一致。这其实是一个非常繁琐的过程，在上文中提到MPI调试困难，因此DEBUG查看中间值几乎不可能，只能设置多处断点，运行程序，和串行程序进行结果对比。

#### 四.总结

文章梳理了简单并行化LR的过程，有很多需要进一步优化的地方，同时回顾了踩坑经历。MPI在提供灵活性的同时，也带来了调试问题。并行化一个串行程序，通常要考虑任务并行和数据并行，这个过程考察我们的任务分解能力和数据分解能力，当然，这是需要数据理论证明来提供支持的。并行化调试是一个难点，必要的时候，步步验证。总之，并行化没有绝对完美的方案，需要在多个因素之间做一个trade-off，focus重点。最后给出[代码地址](https://github.com/zhpmatrix/parallel-computing/tree/master/LogisticRegression_with_MPI)，**代码的目的是快速原型呈现**，故有诸多槽点。

在之前的文章中多次提到过李沐，感兴趣可以读读《Scaling Distributed Machine Learning with the Parameter Server》，在写完这篇文章后，我翻了李的论文，同时在参考中给出了一个中文的论文思路。我在做并行化的时候，假设集群拓扑是一个管理节点和四个计算节点，而真实的集群拓扑是多管理节点(server)多计算节点(worker)，在论文中给出了各种设计细节，包括通信格式，异步处理，参数更新设计，容错处理，扩展性考量等。


##### 参考：

1.[详解并行逻辑回归](http://blog.csdn.net/zhoubl668/article/details/19612215)

2.[大规模逻辑回归并行化](http://wenku.baidu.com/link?url=ZpJz3xin6_vPozZx9FNbRjYmLtsefg1OOnwvBdWJVlh1oS2fCIn11jRkaAGzrEBqV2xjzAArtyKz6--pzUQshKuhk9pdafl8PLnRiM_3YgK)

3.[MPI并行编程](http://wenku.baidu.com/link?url=0Ghp5qxEK6ZejCXp8ioIkEZatgPCXt4RbqJR3FiRbQODJrMXmAHWTVdyfX-pl-yd5d-F3_8zmsoa8LhcQRzz_fLL-7mqRZqvr0lK3B1naiq)

4.[大数据集群计算利器之MPI/OpenMP---以连通域标记算法并行化为例](大数据集群计算利器之MPI/OpenMP---以连通域标记算法并行化为例)(_个人非常喜欢这篇文章的风格_)

5.[Paxos算法](https://zh.wikipedia.org/wiki/Paxos%E7%AE%97%E6%B3%95)

6.[Parameter Server详解](http://blog.csdn.net/mydear_11000/article/details/54948149)

7.[贾扬清谈到的SGD+MPI+Allreduce](https://www.zhihu.com/question/56676679)

8.[Allreduce(or MPI) vs. Parameter server approaches](http://hunch.net/?p=151364)

9.[MPI Reduce and Allreduce](http://mpitutorial.com/tutorials/mpi-reduce-and-allreduce/)










