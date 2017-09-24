---
layout: post
title: "[Python]记一次Debug经历"
excerpt: "最近在备战PAC2017-AI组的决赛，下午写metric模块的时候，考虑到边界条件，必要时需要捕获除零异常。但是，在问题没有发现之前，怎么也捕获不到，这是为什么呢？"
date: 2017-09-24 18:43:00
mathjax: true
---

考虑到数据倾斜的问题，决赛使用了Precision, Recall, F1-score, Accuracy四个指标，其中在定义Recall的时候，代码如下：


code 1:

    try:
        recalls[ labels[i] ] = float('%.2f' % (matrix[i][i] / trueNum[i]))
    except Exception as e:
        print('Error!')
        recalls[ labels[i] ] = 0.0

正常情况下，在trueNum[i] = 0的时候，能够捕获到ZeroDivisionError，可以输出Error的结果，可是上述代码不能捕获。能够捕获到异常，对于上述代码本来应该是一件很正常的事情呀？

好吧，难道我捕获异常的方式不对？于是尝试了捕获方式。结果都是一样的，不能捕获！

是的，我还考虑了Python版本之间的差异性问题，只差考虑到难道Python3.6的异常捕获本身就是个Bug？(相信你绝对有在百思不得其解的时候，质疑一切的经历。不过一般结果都是，这种质疑是没有意义的。)

看一下标准的代码，一般这个时候会加剧问题的神秘感。

code 2:

    try:
        4/0
    except Exception as e:
        print('Error!')

代码成功输出Error的结果！

查看code 1的变量值，trueNum[i]确实为0！！！

进一步查证，直接将trueNum[i]置0，代码如下：

code 3:

    try:
        val = 0
        recalls[ labels[i] ] = float('%.2f' % (matrix[i][i] / val))

未能成功捕获，且输出Warning如下(其实这个bug的发现多亏这个warning，是在想办法解决这个warning的过程中发现的这个bug)：

    RuntimeWarning: invalid value encountered in long_scalars

读了code 3，估计有些同学已经疯了，反正我是疯了。😖，疯了。

继而尝试了下述代码：

code 4:

    try:
        val = 0
        tmp = matrix[i][i] / val
        recalls[ labels[i] ] = float('%.2f' % (tmp))

很显然，还是不能正常捕获。直觉上，我开始type，相信很多同学在debug的过程中，shape+type绝对好用。

**其中val是int，matrix[i][i]是numpy.int64, tmp是numpy.float64。**

好吧，在值相同的前提下，保持类型一致。代码如下：

code 5:

    try:
        val = 0
        tmp = int(matrix[i][i]) / val
        recalls[ labels[i] ] = float('%.2f' % (tmp))

成功捕获到异常！！！

**至此，可以总结：该bug的产生是由于除数0是非int类型！！！** 其次，上述tmp的类型也很有意思，一个numpy.int64 / int会得到一个numpy.float类型的变量。

为了加深问题的神秘感，写了下述代码(假设matrix[i][i] = 0)：

code 6:

    if matrix[i][i] == 0:
        print('True')

恩，是True。由此可以明白，'=='操作符，只是比较变量内容，不比较变量类型，但是异常捕获是对变量类型敏感的(由此想到了本科时经常侃java中的equals的使用方式)。

总结：文章写得很短，但是历时120分钟左右从发现问题到问题解决。其中，为了不耽搁师兄的模型评估，砍掉过所有的异常捕获，直接利用条件判断处理，但是条件判断是直接针对分母的处理，显然OK。问题初看，比较诡异，但是问题的原因却是老生常谈的类型与内容的关系问题。写代码的时候没有考虑到边界条件，导致warning的出现，本着不放弃warning的原则，进一步挖到了这个bug。导致处理时间长的另外一个原因是对Python的异常处理机制的不熟悉，同时对numpy的数据类型也不甚了解。












