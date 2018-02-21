---
layout: post
title: "[DL]经典目标检测论文阅读"
excerpt: "春节假期在家简单梳理了一些目标检测领域经典的文章，每篇文章主要包括Contributions，可Follow方向，我的想法，参考文献四部分内容。随着阅读量的增加和阅读深度的增加，这篇博文会保持持续更新。"
date: 2018-02-19 18:24:00
mathjax: true
---

### 综述文章

1.《Speed/accuracy trade-offs for modern convolutional object detectors》Kevin Murphy,Google Research

以Faster R-CNN, R-FCN, SSD为研究范本，研究了feature extractors(backbones), image resolutions, hardware and software platforms（CPU&GPU）的差异。研究的具体方式是在统一的框架上重新实现。文章给出了许多统计图表，非常棒。

### 聊SSD

#### Contributions

1.Multi-Scale Feature Maps

2.Splitting the Region Space（关键联系：类似于RPN中的Anchor Box）

3.The Devil is in the Details(Data Argumentations)

#### 数据增强

horizontal flip/random crop&color distortion/random expansion.

#### 工作联系

模型发展之间的联系：按照目标检测领域流行的分类方式，有两类研究分支，分别是基于sliding windows(**One-Stage?**)和基于region proposal classification(**Two-Stage?**)。在CNN流行之前的两个研究分支的SOTA分别是Deformable Part Model(DPM)和Selective Search。

针对sliding windows的改进工作有OverFeat，YOLO和SSD，SSD在结构上和OverFeat(one-stage,class-specific detection pipeline)以及YOLO有直接的联系；

R-CNN结合了Selective Search和CNN，犹如春雷乍响，region proposal犹如春风般吹遍Detection界的大江南北。R-CNN有两大模块：proposal generation和post-classification。针对post-classification的改进工作有SPPnet
和Fast R-CNN,针对proposal generation的改进工作有以proposals generated directly from a separate deep neural network为目的的工作和Faster R-CNN(two-stage cascade consisting of class-agnostic proposals and class-specific detections)。

#### 可Follow方向

作者在文章和ECCV2016的slide中提到的可做的三个方向：Object Detection+Pose Estimation,Single Shot 3D Bounding Box Detection, Joint Object Detection + Tracking Model(as part of a system using recurrent neural networks to detect and track objects in video simultaneously)

#### 我的想法

1.Extra Feature Layers是固定的，能否根据Task自动扩展？或者说结构和Task之间的联系能否量化？结构确定了问题优化的形式或者空间，如果结构改变，优化目标就发生了变化，传统的方法论能否适用？该问题独立于SSD的结构

2.针对贡献一:multi-scale还有什么有意思的玩儿法？分析multi-scale和“金字塔”系列的关系

3.针对贡献二:default box(anchor box)还可以以什么形态存在？（之所以有2和3的想法，是因为直觉上2和3在灵活度上还远远不够！）

#### 参考文献

1.《SSD: Single Shot MultiBox Detector》Wei Liu等人

2.ssd_eccv2016_slide，作者会上的报告，提到一些文章中没有的细节

### 聊聊R-FCN

#### Contributions

1.position-sensitive strategy manages to **encode useful spatial information for locating objects**,without using any learnable layer after RoI pooling

2.R-FCN的精度和Faster R-CNN相似，但是在training和inference阶段更快。

#### 可Follow方向

1.R-FCN中的R，代表region proposals methods，典型的方法可以是Selective Search和Edge Boxes或者RPN，文章中的R-FCN中的region proposals methods是RPN。寻找更棒的region proposals methods是一个方向

2.将detection的方法用到semantic segmentation中


#### 我的想法

1.简单的美学追求。一定可以更简单。

2.class-agnostic bbox regr（objectness）和class-specific bbox regr（multi-classification） are needed?


#### 参考文献

1.《R-FCN：Object Detection via Region-based Fully Convolutional Networks》


### 聊聊R-CNN

#### Contributions

1.Apply high-capacity convolutional neural networks(CNN) to bottom-up region proposals in order to localize and segment objects

2.when labeled training data is scarce, supervised pre-training for an auxiliary task, followed by domain-speciﬁc ﬁne-tuning, yields a signiﬁcant performance boost

#### 可Follow方向

#### 我的想法

1.用CNN去解决老问题，但是没有从老路子中彻底走出来，不过已经是非常棒的工作了。

#### 参考文献

1.《Rich feature hierarchies for accurate object detection and semantic segmentation》


### 聊聊Fast R-CNN

#### Contributions

1. 比R-CNN，SPPnet更高的检测质量

2.训练过程是单阶段的，使用multi-task loss

3.训练可以更新所有的网络层

4.不需要feature caching

#### 可Follow方向

1.稀疏Object Proposals可以提升检测质量，或许存在一些技术使得Dense Box表现的和稀疏Object Proposals一样好，这样的技术一旦被开发，可以加速目标检测。

#### 我的想法

1.R-CNN和Fast R-CNN中都提到了SVM用于多分类，并且在本文中作者给出了SVM和Softmax孰优孰劣的讨论（Softmax比SVM好一丢丢）；

#### 参考文献

1.《Fast R-CNN》,Ross Girshick(rbg@microsoft.com)

### 聊聊Faster R-CNN


#### Contributions

1.RPN: share full-image convolutional features with the detection network,thus enabling nearly cost-free region proposals. An RPN is a fully convolutional network that simultaneously predicts object bounds and objectness scores at each position.Faster R-CNN merges RPN and Fast R-CNN into a single network by sharing their convolutional features("attention" mechanisms:the RPN component tells the unified network where to look)

#### 可Follow方向

#### 我的想法

1.文中给出了处理不同尺度和大小的范式

#### 参考文献

1.《Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks》,Shaoqing Ren,Kaiming He,Ross Girshick, and Jian Sun

### 聊聊YOLO

#### Contributions

1.对基于滑窗的方法的计算密集的改进

#### 可Follow方向

YOLO的两个问题

1.Can't detect multiple objects in same grid(Anchor boxes)

2.Possibility to detect one object multiple times(Non-max suppression)


#### 我的想法

对YOLO的两个问题的改进方法成为现在目标检测领域中的经典方法

#### 参考文献

1.《Evolution of Object Detection and Localization Algorithms》,Prince Grover,Post

### 聊聊YOLO9000

#### Contributions

1.YOLO9000 is a strong step towards **closing the dataset size gap between classification and detection**


#### 可Follow方向

1.把相似的技术用到弱监督图像分割领域

2.assign weak labels to classification data during training的技术加强

3.整合不同来源和结构的数据进入模型

#### 我的想法

1.WordTree:整合不同来源的数据，组合ImageNet和COCO的数据进行训练

2.联合优化技术(同时在ImageNet和COCO上训练)


#### 参考文献

1.《YOLO9000：Better,Faster,Stronger》

### 聊聊MobileNets和MobileNets v2

#### Contributions

1.MobileNets are based on a **streamlined architecture** that uses **depth-wise separable convolutions** to build light weight deep neural networks, and it uses cases including object detection, finegrain classification, face attributes and large scale geo-localization

2.width multiplier:thinner models   &    resolution multiplier:reduced representation

#### 可Follow方向

#### 我的想法

1.获得针对嵌入式设备的小网络的必要性？

2.获得小网络的方式：a.直接设计小网络；b.shrinking, factorizing or compressing pretrained networks, compression based on product quantization, hashing, pruning, vector quantization and huffman coding, distillation（典型的是模型蒸馏，有人提到数据蒸馏）, design a low bit networks.

#### 参考文献

1.《MobileNets:Efficient Convolutional Neural Networks for Mobile Vision Applications》


### 聊聊Light-Head R-CNN

#### Contributions

#### 可Follow方向

#### 我的想法

#### 参考文献

### 聊聊R-FCN-3000

#### Contributions

#### 可Follow方向

#### 我的想法

#### 参考文献


这篇博客的参考文献:

1.知乎陈泰红:[总结部分经典文献目录和文献阅读笔记](https://zhuanlan.zhihu.com/p/31117359)

2.handong1587的[Github列表](https://handong1587.github.io/deep_learning/2015/10/09/object-detection.html#object-detection-in-3d)，更新非常及时。









