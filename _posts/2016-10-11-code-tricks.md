---
layout: post
title: "两个tricks"
tags: [C++]
excerpt: "尾递归和回溯"
date: 2016-10-11 11:20:00
---

在前边的部分博文中，说到过递归程序的优缺点，缺点之一是**内存耗费大，调用栈需要同时保存多个调用记录，使得调用栈加深，严重情况下，“StackOverflow”**。同时提到了三种解决方法，其中之一是尾递归，**尾递归保存一个调用记录**，上代码：

---
![尾递归](http://ww4.sinaimg.cn/mw690/aba7d18bgw1f8o5txw19jj20la0il0vi.jpg)
---

factorialA是普通递归程序实现阶乘，在n很大的情况下，调用栈很深。factorialB采用了尾递归实现，将最终的结果值保存在total中。尾递归的想法很棒，但是需要仔细考虑参数接口的设计。比如，在factorialB中，将n和total作为参数传递，结果存储在total中。

如何理解一个递归程序？上代码：

---
![reverse函数的递归实现](http://ww4.sinaimg.cn/mw690/aba7d18bgw1f8o5twkeo1j20l80bg3zp.jpg)
---

上述是一个**反转字符串**的程序，代码一路递归调用下去，直到遇到字符串的结束符'\0'，然后从倒数第二个字符，一路沿着**调用栈的反方向**，打印字符串中的每个字符。

回顾背包问题的回溯实现，代码如下：

---

![背包问题回溯函数代码](http://ww4.sinaimg.cn/mw690/aba7d18bgw1f8o5tyn8juj20ld0deq4w.jpg)

---

回溯的代码套路相似，在上述代码中，实现回溯的关键在于满足约束条件后执行的BackTrack(depth+1)，当到达叶子节点之后，回到递归函数的首次调用的地方，然后逐步恢复父节点状态，为函数实现中第二次调用BackTrack(depth+1)做准备。
