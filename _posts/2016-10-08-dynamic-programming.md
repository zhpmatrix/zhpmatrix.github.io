---
layout: post
title: "再聊动态规划"
tags: [LeetCode]
excerpt: "从问题中验证思想"
data: 2016-10-08 08:58
mathjax: true
---

<script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=default"></script>

0-1背包问题：
给定n中物品和一个背包，物品i的重量是\\(w_i\\),其价值为\\(v_i\\),背包的容量为C。如何选择装入背包的物品，使得装入背包中物品的总价值最大？

0-1背包问题等价于一个**整数规划**问题：

$$
\begin{align}
&max\quad \sum\limits_{i=1}^nv_ix_i\\\\
&s.t.\quad
    \begin{cases}
        \sum\limits_{i=1}^nw_ix_i \leq C \\\\
        x_i \in\lbrace0,1\rbrace,1 \leq i \leq n
    \end{cases}
    (*)
\end{align}
$$

* 最优子结构：原问题的最优解包含子问题的最优解。

精彩来了，下边是一个**形式化的证明**：

设\\((y_1,y_2,\cdots,y_n)\\)是\\((*)\\)的一个最优解，则\\((y_2,y_3,\cdots,y_n)\\)是下面子问题的最优解：

$$
\begin{align}
&max\quad \sum\limits_{i=2}^nv_ix_i \\\\
&s.t.\quad
    \begin{cases}
        \sum\limits_{i=2}^nw_ix_i \leq C - w_1y_1 \\\\
        x_i \in\lbrace0,1\rbrace,2 \leq i \leq n
    \end{cases}
\end{align}
$$

证明：（反证法）假设\\((z_2,z_3,\cdots,z_n)\\)是上述子问题的最优解，则：

$$
\sum\limits_{i=2}^nv_iz_i \ge \sum\limits_{i=2}^nv_iy_i \\\\
w_1y_1+\sum\limits_{i=2}^nw_iz_i \leq C
$$

所以有

$$
v_1y_1+\sum\limits_{i=2}^nv_iz_i \ge \sum\limits_{i=1}^nv_iy_i
$$

说明\\((y_1,z_2,z_3,\cdots,z_n)\\)是比\\((y_1,y_2,y_3,\cdots,y_n)\\)更优的一个解，矛盾！

* 重叠子问题：在0-1背包问题中，在选择是否要把一个物品加到背包中，必须**把该物品加进去**的子问题的解与**不取该物品**的子问题的解进行比较。这种方式形成的问题导致了许多重叠子问题，满足动态规划的特征。

在验证0-1背包问题能够使用动态规划算法解决的过程中，利用两个条件即刻画了该问题的结构特征，由[设计动态算法的步骤](https://zhpmatrix.github.io/2016/10/07/algorithm-review/)可进行第二步，定义最优值(_战术层面关键而又具有挑战性的问题_)。

定义最优值为**m(i,j)**：

* 假设选择物品前，已经给所有物品编号，i是可选物品的最小编号
* j是背包剩余容量

综合理解m(i,j)：在背包剩余容量为j的前提下，可选物品编号为\\(i,i+1,\cdots,n\\)的时候，背包的最大价值。其中\\(i\\in Z,i \in [0\sim n],j\in[0\sim C]\\)。如何想到这样定义最优值的？我的想法是，最优值是一个“时间剪影”，考虑“选物品，装背包”的过程，在某一个时刻停下，描述此刻的状态(值)。具体的定义则是过程下一步，如下：

$$
m(i,j)=
\begin{cases}
        max\lbrace m(i+1,j),m(i+1,j-w_i)+v_i\rbrace\quad j \geq w_i \\\\
        m(i+1,j)\quad 0 \leq j < w_i
\end{cases}
$$

$$
m(n,j)=
\begin{cases}
    v_n\quad j \geq w_n \\\\
    0\quad 0\leq j < w_n
\end{cases}
$$

当剩余背包容量j不小于当前编号最小物品的重量\\(w_i\\)的时候，该物品可以从重量角度可以放进背包，但是为了背包价值最大化的考虑，该物品可以放进背包，此时最大值为\\(m(i+1,j-w_i)+v_i\\),如果不放进背包，此时最大值为\\(m(i+1,j)\\)，也就是说，背包剩余容量不变且保持为j，但是由于不选择物品i，则下一步可选物品编号最小为i+1。回顾重叠子问题性质考察的内容，子问题对应两种情况。

当剩余背包容量j小于当前编号最小物品的重量\\(w_i\\)的时候，下一步只能从编号i+1的物品开始选择。

有了上述两种情况下的分析，理解m(n,j)就相对容易了，那m(0,C)呢？

一般来说，利用动态规划思想解决问题，核心步骤基本搞定。不要忘了最优值和最优解的区别，还需要从最优值的构造过程中构造最优解，在计算过程中，记录下每次选择的物品编号和重量就OK，该问题构造最优解的过程相对容易。

***

纯手打Latex公式，已经打不动了。此处安利两个资源：

下里巴人：[动态规划教学必备题](https://www.zhihu.com/question/23995189/answer/35324479)

这个answer通过给出“数列中最长递增子序列问题”的两种拆分方式，验证了动态规划的两个要素：对状态的定义和状态转移方程的定义，指出**动态规划的核心是拆分方式**，也就是站在一个可数学化描述的角度重新看问题。同时也指出了关于动规几个关键词的认识，如”递归“，”无后效性“，”缓存“，”记忆等“。

阳春白雪：[动态规划本质探讨](https://www.zhihu.com/question/23995189/answer/35429905)

这个answer的两大贡献在于，第一给出了状态机的描述(很有意思)，第二讨论了依据状态转移选择递推，搜索，贪心，动态规划的条件。

***






