---
layout: post
title: "[算法设计]计算理论"
excerpt: "带着一个LeetCode题目能否有一个形式化的数学描述，并且存在一个数学的解决方法，梳理了计算理论的基本概念，然而疑惑并没有得到解决。"
date: 2017-11-24 18:42:00
mathjax: true
---

最近做题总是想着将一个问题先形式化描述成一个数学问题，继而就会带来两个问题，第一是能否转化？第二是转化后是不是有对应的很"数学"的解决方案?数学强大的抽象能力能够描述很多问题，如果上述两个问题得到解决，就意味着我可以用相同的方式解决更多的问题，生产力得到极大解放。这对我而言是一件很有吸引力的事情。

有一个命题是这样的："John Michael Robson在1983年证明了围棋不存在多项式时间的算法，证明了围棋问题等价于指数时间停机问题。"

这意味着不需要花费很多的精力去寻找一个多项式算法来解决围棋问题，因为不存在。这个结论很显然也很直白，但是很重要。因为它划定了问题解的边界，首先一个问题是不是可解，其次才是怎样解。

为了满足自己的好奇心，我搜索到了**计算理论**。

计算理论关心的三个问题：

1.  采用什么计算模型？（形式语言，自动机）

2.  解决哪些是能计算的，哪些是不能计算的？（可计算性理论及算法）这里的能不能计算，是指该问题能否用计算机来解决(算)。

3.  要用多少时间，要用多少存储？（计算复杂性理论）

问题2**部分**可以转换到对3的讨论，能不能算，要考虑存储和时间。存储是物质的概念，可以通过加硬件解决，唯有时间无法完全克服，虽然以存储为代表的硬件技术可以一定程度上改善时间的问题，但是这种改善已经超出计算理论的范畴，是一种具体的改善而已，不能从本质上将一个不可计算的问题变为可计算的问题。

这三个方面的问题用一个问题概括："计算机的基础能力及限制到什么程度？"。这个问题的意义在于帮助自己跳出目前的思维框架，去思考一下有什么是计算机不能干的？(这个好像已经背离了我的初衷。)

为了研究计算理论，需要一个理论上的计算模型。图灵机是一个理论上的计算机模型，通过读入一系列的0和1解决特定问题，数字代表解决某个问题的步骤。图灵机是理论上的通用机，图灵认为，只保留最简单的指令，把复杂的工作分解为几个最简单的操作就OK。很显然，问题的困难之一在于如何确定最简单的指令集，之二在于如何将复杂问题分解为简单指令的问题。

丘奇-图灵论题：一切合理的计算模型都等同于图灵机。

基于该模型，可以对问题做一些有趣的探讨，比如：

停机问题：编译器能否自动检测程序是否会死机?(不可判定)

编译器能否自动检测程序是否会在一百万步内死机?(可判定)

"x=y?"的通讯复杂性？

给定通讯双方各自N位二进制串X和Y，双方需要交换多少位的信息才能判断X是否等于Y？

[Yao, 1979]需要交换N位信息。简要证明参考[课件](https://basics.sjtu.edu.cn/~chen/teaching/TOC/TOC5.pdf)

通常对于不搞理论计算机的同学来说，计算复杂性是我们focus的点。而计算复杂性的核心问题是：**P=NP?**某位图灵奖得主曾说P v.s. NP- a gift to mathematics from computer science.

这里首先给出P, NP, NPC的解释，为了避免解释的歧义，直接给出算法导论中的阐述。

NPC:    No polynomial-time algorithm has yet been discovered for an NP-complete problem, nor has anyone yet been able to prove that no polynomial-time algorithm can exist for any one of them.

**if a problem is in NP and is as “hard” as any problem in NP**

NP:     The class NP consists of those problems that are “veriﬁable” in polynomial time.

P:      The class P consists of those problems that are solvable in polynomial time.

**Any problem in P is also in NP,since if a problem is in P then we can solve it in polynomial time without even being supplied a certiﬁcate.**

这里的一个关键点是 **if any NP-complete problem can be solved in polynomial time, then every problem in NP has a polynomial-time algorithm。**因为任何一个NP问题都可以在多项式时间内转化它的输入，使之成为一个NPC问题。

补充：

1.NP-hard: at least as hard as the hardest problems in NP Problem.

如何证明一个问题是NPC？通过规约，将一个问题转化为另一个已知问题。比如建立映射，把复杂未知问题拆成复杂已知问题和简单未知问题来解决。。这篇[博客](http://www.zitaoliu.com/cs/algorithm/2011/04/15/introduction-to-algorithm-np-problem/)给出了几个具体的例子。

现在回答，如果 NP=P，基本意味这对任何实用的加密系统，存在一个正整数k，有一个运行时间是O(x^k) 的算法可以攻破它。如果这个k足够大，对安全性就没什么影响了。

NP包含成千上万的问题，我们是否要研究所有的问题呢？如果有个多项式时间的图灵机(有限状态自动机)可以求解某个具体NP问题，那么所有的NP问题都有多项式时间的算法。

说这些有什么用？算法导论作者给出如下回答。

**To become a good algorithm designer, you must understand the rudiments of the theory of NP-completeness. If you can establish a problem as NP-complete, you provide good evidence for its intractability. As an engineer, you would then do better to spend your time developing an approximation algorithm (see Chapter 35) or solving a tractable special case, rather than searching for a fast algorithm that solves the problem exactly. Moreover, many natural and interesting problems that on the surface seem no harder than sorting, graph searching, or network ﬂow are in fact NP-complete. Therefore, you should become familiar with this remarkable class of problems.**

总结: 为了成为一个好的算法设计者，你必须懂得NPC理论的入门知识。如果你能证明一个问题是NPC问题，作为一个工程师，你就可以把时间花在开发近似算法和解决该问题在特殊条件下的变种，而不是花费大量精力开发一个快速算法完全地解决该问题。此外，有些问题虽然看起来并不会比排序，图搜索，网络流更难，但是其实是NPC问题，因此，也需要熟悉一些典型的NPC问题(可以规约转化)。总之，我的疑惑还没有解决，囧。

参考：

1.[复旦计算机学院-陈笠佳老师的Theory of Computation课件](https://basics.sjtu.edu.cn/~chen/teaching/TOC/)

2.算法导论












