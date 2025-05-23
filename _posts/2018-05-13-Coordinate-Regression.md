---
layout: post
title: "坐标回归"
tags: [CV]
excerpt: "坐标回归作为经典问题出现在检测任务中，这篇博客站在几何变换和数值优化的角度，尝试正推和逆推两个方向理解一下坐标回归，殊途同归。"
date: 2018-05-13 18:43:00
mathjax: true
---

在上篇博客中提到RP的概念，这篇博客继续沿用这种表达。首先提出的问题是，给定RP和ground truth，坐标回归要学习什么？怎么学？回顾ground truth的概念，一张图片中的一个物体，该物体对应的类别和位置坐标。

为了方便下述描述，这里一定要给出一组符号，不过足够简单。假设RP的中心点坐标和宽高分别用rpx, rpy, rpw, rph表示，ground truth的对应表达为gx, gy, gw, gh，预测框的对应表达为px, py, pw, ph。

学习目的是获取一个精确的预测框位置，目的都在网络的前向推断过程中体现。抛开具体任务，考虑一个几何问题，给定RP和ground truth，可以怎样表示预测框的位置呢？我们的目的当然是预测框和ground truth非常地接近。为了简化问题讨论，考虑给定RP，怎么将RP变换到ground truth的位置。首先，两者大小可能不一样，需要一个尺度变换；其次中心点位置不一样，需要平移，包括水平和垂直。直接斜着把RP的中心点拉到和ground truth中心重合，还是可以分解为水平和垂直移动。嗯，应该OK了。现在需要形式化表达了。

尺度变换，需要RP的宽高分别乘上一个变换因子，单纯的线性运算，实现宽高的拉伸和压缩；平移变换，需要原始RP的中心点坐标加上平移量，这个平移量还是对应一个变换因子乘上RP的宽高。

给定RP和ground truth，我们想通过两种变换，对RP的位置进行更加精确的表达。而这个过程中，变换因子和平移量不知道具体值是多少？到这里，学习目标很明确了。希望通过坐标回归过程，学习到这个变换过程。

这里明确一下输入和输出。输入是RP对应的卷积特征，输出是要学习的内容，也就是变换因子和平移量。针对坐标回归过程的ground truth就是RP和真实框的位置差了。

这样看来，似乎一切都是顺理成章。

换个角度，跳出来看一看这个问题。坐标回归过程的ground truth能否直接为gx-rpx, gy-rpy, gw- rpw, gh-rph?没毛病，这表明，我们希望网络学习到坐标的位移量。

能够直接为x-rpx, gy-rpy, gw/rpw, gh/rph？没毛病，这表明，我们希望网络学习到宽高的缩放因子。

能够直接为(gx-rpx)/rpw, (gy-rpy)/rph, gw/rpw, gh/rph？没毛病，这表明，我们希望网络学习到中心坐标和宽高的缩放因子。

这些讨论的都是几何上的一些问题，放到数值优化角度，哪种比较不错呢？首先考虑值过大或者过小的问题，这意味着优化的难易程度。(gx-rpx)/rpw, (gy-rpy)/rph，分母上有大于1的值，似乎会比其他更好一些。如果过大，当然可以做纯数值变换，比如log，但是log要求对象>0，从这个角度来看，宽高的减法操作都不能满足，所以选择gw/rpw，gh/rph会比较不错。

这样就有(gx-rpx)/rpw, (gy-rpy)/rph, log( gw/rpw )，log( gh/rph) 。

其实log(gw/rpw) = log(gw) - log(rpw)，从这个角度也可以看做直接多gw和rpw做尺度缩放，因为gx-rpx和gy-rpy的正负性很难保证，虽然不能取log，但是分母上有>1的值，也算OK。

其实上述的所有结果都可以从几何的角度顺推出来，不过形式上，数值的问题无论在正推和顺推时候，都是需要考虑的问题。

写到这里，一切似乎都是顺理成章，水到渠成。理解坐标回归，关键之一就是要理解几何变换和数值优化，看似繁琐的背后，都是科学地推断过程。

补充一张讨论的结果图片：

![res](http://wx3.sinaimg.cn/mw690/aba7d18bgy1fsxv45ndwbj20q60a3wh8.jpg)


















