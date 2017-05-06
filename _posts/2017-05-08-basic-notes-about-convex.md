---
layout: post
title: "[Optimization]一入优化深似海，从此Coding是路人"
excerpt: "这是一篇我读到的比较好的优化的资料整合，可能包括博客，微信公众号，某些论文，某些书中的对某个问题的总结等。采用的形式是提出问题，解决问题的资料来源，和自己对于资料的评论，可能包括资料中某些小的错误瑕疵。"
date: 2017-05-06 18:34:00
mathjax: true
---
<script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=default"></script>

1.[【优化】梯度下降 收敛性 证明](http://blog.csdn.net/shenxiaolu1984/article/details/52577996)

给出了序列收敛性的两个定义，第二个定义是paper中经常出现的，同时在博客中的推导也体现了出来。作为引理，阐述了Lipschitz连续，\\(\beta\\)平滑及两个性质和性质证明。说明了SGD收敛条件和收敛条件物理意义。

在推导\\(f(x_t)\\)极限的时候，第一个公式存在明显笔误。文中的证明很漂亮！！！

2.[收敛率概述(Overview of Rates of Convergence)](http://mp.weixin.qq.com/s?__biz=MzIzMjU1NTg3Ng==&mid=2247483784&idx=1&sn=6082e46e4707bb8192ab67ff6926a870&chksm=e8925583dfe5dc953521b968f168f06c2a9a2373bb24a67abc7a9a9e67caa0af33165e03e8f7&mpshare=1&scene=23&srcid=0503Ml8DTEZGy2Wa8CavBr9Q#rd)

这是史春奇和王雅清的文章，他们的很多文章自己都非常喜欢。

提到了常见的收敛方法，Bisection和Fixed Point，同时给出了Fixed Point的两个具体算法牛顿法和割线法。关于这两个收敛方法，可以结合推荐1的关于序列收敛性的两个定义来琢磨。再次回顾了收敛率的定义，同时也提到了收敛率的估算。

3.[Cost function of neural network is non-convex?](https://stats.stackexchange.com/questions/106334/cost-function-of-neural-network-is-non-convex)

在ML中，涉及优化的东西总是会做一个比较。关于神经网络的优化有很多文章，比如COLT上就看到过几篇。由于自己还没有研究到这块内容，但是总会不经意间看到一个问题就是神经网络目标函数的非凸性，当然这句话本身就是不严格的。在上述这个问题中，给出了一个关于permutation的清晰的解释。

4.[系统学习机器学习之误差理论](http://blog.csdn.net/app_12062011/article/details/50577717)

补充:[误差概念](https://stats.stackexchange.com/questions/87750/what-does-the-term-estimation-error-mean)

这部分内容原则上不应该出现在这个位置，但是真的很不错。文章从bias和variance谈起，通过引入union bound和Hoeffding inequality(Chernoff bound)，结合具体的二分类问题，讨论了机器学习中的样本量下界，误差界限等，最后以VC维结束讨论。适合对计算学习理论感兴趣的同学仔细阅读。



