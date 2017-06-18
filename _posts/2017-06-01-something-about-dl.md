---
layout: post
title: "[ML&DL]啊哈，CNN!"
excerpt: "趁着跑Eve代码的时间，读了一些关于CNN的东西，在这之前，只在组会上听实验室的师兄师姐聊。可能会看到一些关于R(2)NN,LSTM的一丢丢东西。"
date: 2017-06-01 14:59:00
mathjax: true
---
<script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=default"></script>

新东西和新课题，我一般是从review或者survey开始，[CNN的发展史](http://www.cnblogs.com/52machinelearning/p/5821591.html),其中有张表做了AlexNet,VGG,GoogLeNet,ResNet在ILSVRC上的战绩对比。带着**一堆**问题，看到这篇文章[An intuitive Explanation of Convolutional Neural Networks](https://ujjwalkarn.me/2016/08/11/intuitive-explanation-convnets/),从一个简单的ConvNet开始谈，极大的帮助自己整理了概念，回头看**CNN的发展史**中的内容，会有新的理解。偶然间看到这篇文章[深度神经网络结构以及Pre-training的理解](http://www.cnblogs.com/neopenx/p/4575527.html)，我只看了**Pre-training**的部分，作者做了大量的调研，很合自己口味，应该不会让读到的同学失望。

读文献中，会自然引起自己兴趣的话题：

[Batch Normalizaton](https://arxiv.org/pdf/1502.03167.pdf),关于BN,这篇[博客](http://blog.csdn.net/elaine_bao/article/details/50890491)画了一张图来讲解motivation(保持分布的同时，要保持模型的表达能力)

[DropOut](https://arxiv.org/pdf/1207.0580.pdf)作为一种防止过拟合的策略，将**输出随机置0**，不同的人有不同的认识。与之类似还有另外一个东西[DropConnect](http://yann.lecun.com/exdb/publis/pdf/wan-icml-13.pdf),将**权重随机置0**,DropConnect的计算量更大却没有显著提高性能。很多文献提到：**如何选择Drop Ratio,需要调参？**

[AlexNet](https://papers.nips.cc/paper/4824-imagenet-classification-with-deep-convolutional-neural-networks.pdf),CNN的发展史中讲到AlexNet，实际论文中还有很多trick。

[零基础入门深度学习](https://www.zybuluo.com/hanbingtao/note/433855)

这是一个系列共7篇文章，从感知器到BP传播算法到CNN，R(ecurrent)NN,LSTM,R(ecursive)NN,讲解简明扼要，但是存在部分小错误。

[谈谈深度学习中的Batch_Size](http://blog.csdn.net/ycheng_sjtu/article/details/49804041),文中讲了需要batch_size的原因,batch_size大小对精度和速度的权衡,同时给出了一个例子LeNet在MNIST上测试结果，很有说服力。同时该作者在知乎相同问题下的回答也是最高票。

[inception模型](http://blog.csdn.net/u014114990/article/details/52583912)给出了一张CNN的结构演化图，同时给出了“网络变大”的三个缺点。
