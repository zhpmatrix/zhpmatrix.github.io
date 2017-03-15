---
layout: post
title: "[groot]xgboost源码阅读-启动过程"
excerpt: "这篇短文聊聊xgboost的启动过程，其中包括对rabit的介绍，启动流程等，rabit在之前的文章中也有提到过。"
date: 2017-03-15 14:27:00
---

春节前给出了编译一个可调试版本的xgboost的流程，现在我们可以开心的设断点了。就从demo中的一个二分类问题开始，具体路径：

    xgboost/demo/binary_classification

来到该目录下：

    lldb ../../xgboost mushroom.conf max_depth=9

注意，Mac系统下我采用LLDB作为调试工具，再次提到相比于GDB的一个优点，LLDB对STL的调试输出支持良好。

mushroom.conf中是参数设置,具体包括：模型类型，目标函数，学习率，树的深度(max_depth)，训练轮次，训练和测试数据的路径等信息。在上述脚本的最后一个参数设定:

    max_depth=9

是对配置文件中参数的重新设定。默认参数是:

    max_depth=3

如果使用过xgboost的python封装，一定会对这个默认值非常熟悉。

在main调用地方设置断点，进入函数，实际上来到了cli_main.cc这个文件，也就是client版本，支持命令行交互式传参的main函数入口。让我们来看看这段代码：

<script src="https://gist.github.com/zhpmatrix/872b4e852f47e1ebf16127c82f65b511.js"></script>

具体流程如下：

1.获取通过交互方式传递的参数，也就是我们的参数配置文件和重写参数。

2.初始化rabit。

3.生成一个配置向量用来存储参数，选用KV格式，第一个参数是随机数种子。

4.将读取到的参数配置文件和重写参数写入配置向量。

5.判断任务类型，具体包括训练(KTrain),载入模型(KDumpModel),预测(KPredict)，执行任务。

6.rabit的扫尾工作。

来聊聊rabit。

在之前的博客文章中谈到过目前并行加速的常见方案，单机采用OpenMP利用多核加速,多机采用MPI消息通信接口进行数据分发和参数更新。xgboost的分布式实现多机之间的通信就是采用rabit的，按照陈天奇的想法，“让平台往接口需求上面走”。MPI一致受人诟病的一点是fault tolerance比较差，而rabit是有较好的容错支持的，具体的方案是：多节点备份，挂了的节点向活着的节点要数据来恢复。

分布式通信框架rabit实际上是对allreduce的容错实现。在接收到任务时，比如求和，首先在节点之间建立树形的连接关系来提高节点间通信效率( O(lgn) ),连接关系建立之后，各个节点可以通过allreduce接口通信内存单元，求和通信拓扑具体可参考[这篇文章](https://zhpmatrix.github.io/2017/02/19/speed-up-distributed/)


参考：

1.xgboost导读和实战











