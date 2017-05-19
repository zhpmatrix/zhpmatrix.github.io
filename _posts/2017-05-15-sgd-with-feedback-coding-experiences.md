---
layout: post
title: "[DL]深度学习Eve折腾记"
excerpt: "#Eve的想法已经转给实验室小伙伴来做了#本文是围绕Eve的算法实现折腾过程，也是自己跑的第一个深度学习实验。主要是验证自己的一个想法，是对Eve中的Clipping操作的一个替代"
date: 2017-05-15 18:34:00
mathjax: true
---
<script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=default"></script>


#### 深度学习机

Down到代码之后，首先保证要能够在本机上run起来。为了可以让代码运行在没有GPU的机器上，我主要做了两件事情：第一是从别的途径快速下载代码，存储在本地，修改keras源代码中的load_data()函数中的路径，避免keras从远程下载(慢);第二是修改由于开源库的更新导致的代码不兼容问题，比如返回值的格式等。但是没有GPU的机器是运行的很慢！第一次接触GPU，是从CUDA编程了解的，直觉上如果是利用GPU，则需要编写一些关于GPU的代码，实则不然。keras作为一个前端，利用Theano或者Tensorflow作为后端，可以直接利用GPU进行加速计算。

![keras](http://wx1.sinaimg.cn/mw690/aba7d18bgy1ffd34zyectj204u0ad3ym.jpg)

为了获得一台深度学习机，可以通过Amazon购买计算资源，或者你拥有一台深度学习机。抱了BOSS的大腿，我们实验室拥有一台深度学习机，内置四块Tesla K80。

#### 代码运行环境

Eve的原始代码是基于python3的，故需要一个python3的运行环境，为了不和原始的python2的运行环境发生冲突，可行的一种方式建立虚拟环境。我在Mac上同样存在python2和python3的运行环境，不过Mac上的运行环境搭建是参照参考1中的方式。

深度学习机是Ubuntu系统，冒冒同学在之前的使用中安装了anaconda,故使用anaconda搭建一个虚拟环境更简单。

    conda create -n py34 python=3.4 anaconda

这个过程可能比较漫长，因为要安装基于python3.4版本的一些库。

进入python3.4的运行环境：

    source activate py34

之前之前已经安装了Keras,Theano,Tensorflow等，故OK！

#### GPU监视

nvidia自带显卡监视工具:nvidia-smi,具体使用方式：

    nvidia-smi -h


    watch -n 1 nvidia-smi

含义：每隔1秒输出一下nvidia-smi的结果。

注意：在使用VNCServer连接远程服务器的时候，需要调整服务器的分辨率。

在终端输入：

    vncserver -geometry 1920x1080 -depth 16

在VNCServer的界面窗口中设置当前分辨率，按照Pixes参数设置和上述相同。


参考文献：

1.[MAC OSX 10.11 配置python3及虚拟环境](http://www.jianshu.com/p/0921fd4d4bca)

2.[TensorFlow教程：使用pip安装TensorFlow](http://suanfazu.com/t/tensorflow-pip-tensorflow/13401)

3.[用Keras训练一个准确率90%+的Cifar-10预测模型](http://nooverfit.com/wp/%E7%94%A8keras%E8%AE%AD%E7%BB%83%E4%B8%80%E4%B8%AA%E5%87%86%E7%A1%AE%E7%8E%8790%E7%9A%84cifar-10%E9%A2%84%E6%B5%8B%E6%A8%A1%E5%9E%8B/)
