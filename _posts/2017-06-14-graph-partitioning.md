---
layout: post
title: "[ML&DL]基于图的目标函数分解策略"
excerpt: "自然科学基金项目，求解大规模数据分析中复杂优化问题的演化算法研究中的一个比较基础的问题，想法是将原目标函数分解成多个子目标函数的和的形式，每个子目标用节点表示，两个子目标的共享变量用边表示，合作协同演化。"
date: 2017-06-14 12:48:00
mathjax: true
---
<script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=default"></script>

这个课题的想法是：将高维目标函数分解，通过在子目标函数之间建立通信来解决子目标函数的变量冲突，从而达到全局最优(次优)。这是我在知乎上的[提问](https://www.zhihu.com/question/60884958)，还没有得到有价值的回答。

问题的关键在于如何计算(有效解决冲突)?但是这里总结一下我做的工作，目标函数分解的工作。关于如何计算，老板说了不让我做，因为那是师兄师姐的博士课题(PSO)。不过我可以做其他的优化算法，但是是否收敛？收敛后的gap的bound怎样？都是没有研究的问题。

**首先如何用图表示?** 将原目标函数展开成sum求和形式，每一个term用一个node来表示，两个node之间的边用term的共享变量来表示。

**为什么以及如何分割?** 通过分割可以将高维优化问题转化为低维优化，个人认为**如何分割**和**如何计算**有着密切联系。可能想到的一种方式是优化每个子目标函数，然后同步变量来解决冲突，直至全局最优，那么同步变量就要涉及子目标的通信开销。

**如何最小化通信开销?** 用边上共享变量的个数当做边的权值，这个问题可以转化为图聚类的问题。减少通信也就意味着子目标函数之间的依赖关系越少越好，但是同时要满足负载均衡，负载均衡是多机环境下提高资源利用率的重要方法。

假设不考虑负载均衡，有两种目标函数可选(为了保证严格定义，直接来源metis的官方文档)：

1.最小化割集

    Consider a graph G = (V, E), and let P be a vector of size |V | such that 

    P [i] stores the number of the partition that vertex i belongs to. The 

    edgecut of this partitioning is defined as the number of edges that 
    
    straddle partitions. That is, the number of edges (v, u) for which P [v] 
    
    != P [u]. If the graph has weights associated with the edges, then the 
    
    edgecut is defined as the sum of the weight of these straddling edges.


2.最小化通信代价

    Consider a graph G = (V, E), and let P be a vector of size |V | such that 

    P [i] stores the number of the partition that vertex i belongs to. Let Vb 

    belongs to V be the subset of interface (or boarder) vertices. That is, 

    each vertex v belongs to Vb is connected to at least one vertex that 

    belongs to a different partition. For each vertex v belongs to Vb let Nadj[

    v] be the number of domains other than P[v] that the vertices adjacent to 

    v belong to.The totalv of this partitioning is defined as:

    totalv = Sum{Nadj[v]| v belongs to Vb}.

不严格的说，edgecut以edge为研究对象，意味着砍掉多少条边可以将原目标函数分开，communication volume意味着在不同子目标函数之间进行通信需要多少通信量。communication volume以node为研究对象，可能存在edgecut的重复计算。

关于图分割有很多研究成果，在metis中有两种分割方式，不过二者是类似的想法。

![Bisection](http://wx3.sinaimg.cn/mw690/aba7d18bgy1fgkm1099jxj20he0fsgo8.jpg)

应用Bisection，可以得到K-way的分割方式，如下：

![K-way](http://wx2.sinaimg.cn/mw690/aba7d18bgy1fgkm0zqrotj20ja0ee0vi.jpg)

从上图可以看出，分为三个阶段(metis的实现中，每个阶段都有相应的多种算法)：

1.coarsening:   直观上的表达是提取图的骨骼，方式是用一个node表示多个node。典型地如下：

![coarse](http://wx2.sinaimg.cn/mw690/aba7d18bgy1fgkm800zwhj20gs09xac9.jpg)

2.initial partitioning: 本阶段，原问题被转换为一个小图的**谱聚类**问题。


3.uncoarsening: 还原，注意在还原的过程中要纠正在小图中的分割结果，原因是小图还原为大图的过程中，大图的**度**明显增多，可能找到更优的解，也就是上图中我们看到的**refined partition**。

至此，结束。

**总结:** 个人还是比较期待基于这种目标函数的分解方式在计算上的表现的，但是首先要解决的问题是收敛性的分析。针对分解的工作本文回答了intuition，what，why，how的问题，在具体实现上，自己写了目标函数符号计算的模块，也就是建立目标函数的图表示，然后将分割交给了metis来完成，做了300维和1000维的Rosenbrock目标函数分解的工作，1000维下耗时300s(符号分解+画图+分解+python)，故在计算时间上还是比较快。


参考:

1.[Four graph partitioning algorithms](http://www.docin.com/p-945277994.html)

比较详细的总结了目前主流的图分割算法。

2.[Graph Partitioning的wiki总结](https://en.wikipedia.org/wiki/Graph_partition#cite_note-chaco-14)

简单介绍了各种图划分的方法同时给出了主流的图划分库。

3.[图分割软件集合](http://glaros.dtc.umn.edu/gkhome/views/metis)

4.[METIS for Python](http://metis.readthedocs.io/en/latest/)

（_This wrapper uses a few environment variables!!!_）

Wrapper for the METIS library for partitioning graphs (and other stuff).
This library is unrelated to PyMetis, except that they wrap the same library. PyMetis is a Boost Python extension, while this library is pure python and will run under PyPy and interpreters with similarly compatible ctypes libraries.

[wrapper代码](https://github.com/inducer/pymetis/blob/master/pymetis/__init__.py)

5.[ 分布式图并行计算框架：PowerGraph](http://blog.csdn.net/zcf1002797280/article/details/50334069)

详细的讨论了PowerGraph的话题，包含两个方面GAS Decomposition和Vertex Partitioning.

6.[Spark GraphX在淘宝的实践](http://www.csdn.net/article/2014-08-07/2821097)

7.[SymPy库常用函数](http://www.cnblogs.com/huiyang865/p/5823751.html)

主要用于符号计算，目标函数的展开。

8.[NSGA-II算法实例](https://wenku.baidu.com/view/465404dbe45c3b3567ec8bc8.html)

对多目标优化建立一个直观的认识。

9.[Spectral Clustering](https://wenku.baidu.com/view/e367fb2401f69e31433294b0.html)

谱聚类在三种目标函数下的处理，令人感动的数学。