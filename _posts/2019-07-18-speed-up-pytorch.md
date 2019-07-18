---
layout: post
title: "[PyTorch]PyTorch用于大模型训练"
excerpt: "梳理有助于大模型训练的一些方法，具体包括混合精度加速，XLA加速，分布式训练，梯度累积，梯度Checkpoint相关技术。"
date: 2019-07-18 19:31:00
mathjax: true
---

前言：

>最近部分大佬在内网博客上放了一篇博客，如何使用Tensorflow训练大模型。因此，想PyTorch下应该也有对应技术，于是有了这篇博客。大模型的训练方法，同样适用于一般场景。需要解决的问题包括计算和存储，容易忽略的时间开销在IO。为了得到一个好用的模型，从数据到模型是一个系统工程，即使相关优化技术都用上，也可能比不用任何优化技术的开发周期长的多，比如模型设计不合理，数据不合适，指标有误，代码Bug，系统环境配置等，但是并不妨碍在极限场景下对于该类技术的需求。

刚好[pytorch-transformer](https://huggingface.co/pytorch-transformers/examples.html#introduction)发布，看到文档中有专门讨论了相同的问题，但是整体看下来，虽然huggingface做了对应实现，但是似乎没有严格测试，不管怎样，有了更多可以有所启发的代码可以读一读。

### 混合精度加速

在之前的博客[基于混合精度的模型加速](https://zhpmatrix.github.io/2019/07/01/model-mix-precision-acceleration/)篇中，整理了PyTorch下模型加速的过程和细节。在自己前不久实现的ACL2019的一个工作中，[Github代码地址](https://github.com/zhpmatrix/BERTem)，尝试了混合精度加速。

整体流程同之前的博客，这里需要着重说明一下代码修改的细节。

(1)输入数据类型转换(fp32->fp16)

修改[tacred\_run\_classifier.py](https://github.com/zhpmatrix/BERTem/blob/master/examples/tacred_run_classifier.py)中的输入数据类型：

```
 		all_input_ids = torch.tensor([f.input_ids for f in train_features], dtype=torch.long)
        all_input_mask = torch.tensor([f.input_mask for f in train_features], dtype=torch.long)
        # FloatTensor(forward)
        all_entity_mask = torch.tensor([f.entity_mask for f in train_features], dtype=torch.float)
        all_entity_seg_pos = torch.tensor([f.entity_seg_pos for f in train_features], dtype=torch.long)
        all_entity_span1_pos = torch.tensor([f.entity_span1_pos for f in train_features], dtype=torch.float)
        all_entity_span2_pos = torch.tensor([f.entity_span2_pos for f in train_features], dtype=torch.float)
        all_segment_ids = torch.tensor([f.segment_ids for f in train_features], dtype=torch.long)
        if output_mode == "classification":
            all_label_ids = torch.tensor([f.label_id for f in train_features], dtype=torch.long)
        elif output_mode == "regression":
            all_label_ids = torch.tensor([f.label_id for f in train_features], dtype=torch.float)
```
依据自己的需要，将torch.float转化为torch.float16。对于测试代码做同样的处理。

（2）模型forward函数中的数据类型转换

也就是修改[modeling.py](https://github.com/zhpmatrix/BERTem/blob/master/pytorch_pretrained_bert/modeling.py)中的BertForSequenceClassification的forward函数实现。个人认为，之所以需要修改这里，是由于自己在这块的相关实现并不优雅。

（3）给apex源码打补丁

在上述两步完成之后，正常情况下会遇到一个问题，如下：

```
AttributeError: 'NoneType' object has no attribute 'contiguous'
```
 
 对应的解决方法，参看[issue](https://github.com/NVIDIA/apex/issues/131)。
 
 假设一切顺利的话，就可以正常用起来了。给出我的一些测试结果。在给结果之前，需要说明测试条件。
 
第一：apex官方推荐了两个测试fp16的docker，分别是nvidia出的，和另外一个docker-hub上的。但是自己尝试了各种办法都pull不到nvidia的docker，于是用了后者。据在tensorflow上做加速的同组同学说，nvidia的docker似乎对混合精度加速做了一些优化。

第二：显卡选择，需要tensor core。测试均是在一张TITAN RTX P2上完成。

在具体任务上，延续之前的setting，将train和dev合并共同作为新的train集，test集不变。在fp32
和fp16的两种setting下，比较相同batch\_size下，一个epoch的用时或者每个迭代的用时。

|比较方面|fp32|fp16|备注|
|------|------|------|------|
|训练阶段|1.04it/s|4.41it/s|12.76it/s（独占显卡）|
|推断阶段|4.14it/s|8.63it/s||
|测试集指标|0.65/0.55|0.64/0.53|格式：micro/macor|
|模型大小|421M|212M||

这里借助于apex实现混合精度加速的方法可行，但是不唯一，感兴趣可以进一步探索其他的方式。

### XLA加速

[XLA](https://github.com/tensorflow/tensorflow/blob/master/tensorflow/compiler/xla/g3doc/overview.md)称为加速线性代数库，其实是一个compiler，本来用于优化tensorflow的底层op，但是同样的技术也可以用于PyTorch。该项目还在试验阶段。G家为了推TPU，称通过XLA连接了PyTorch和TPU。[pytorch/xla](https://github.com/pytorch/xla)正是对PyTorch的支持，不过为了测试XLA，同样官方推荐了两个虚拟化相关的镜像。

### 分布式训练

在异构环境下，需要考虑单机多卡和多机多卡的问题。单机多卡是比较常见的情景，但是多机多卡比较少见。自己一直想要尝试一下多机分布式的训练，在很早的时候，[矩阵乘法的分布式实践](https://zhpmatrix.github.io/2017/03/06/matrix-multiplication-mpi-openmp-cuda/)中实现了一些简单的。限于硬件问题，一直没有尝试，最近有大厂的朋友分别在CV和推荐领域遇到需要分布式训练的场景，比如海量的数据等，感觉还是要尝试一下。可以使用的框架是horovod，是一个分布式训练框架，用于支持TensorFlow,Keras,PyTorch,MXNet，主流框架都支持了。同样，PyTorch官方也有自己的一套实现方法。

要实现分布式训练，一般有两种做法：

第一：按照[官方文档](https://github.com/pytorch/pytorch#from-source)去编译PyTorch源码。自己尝试了一下，时间有点久。看了后续的配置项，考虑到可能的集群权限问题，于是放弃了(个人不太喜欢折腾配置之类的事情)。期间要保证首先有一个可用的MPI集群。恰逢[pytorch-transformer](https://huggingface.co/pytorch-transformers/examples.html#introduction)发布，因此想尝试一下。

遇到的一个问题如下：

```
THCudaCheck FAIL file=/opt/conda/conda-bld/pytorch_1550852152579/work/torch/csrc/cuda/Module.cpp line=34 error=10 : invalid device ordinal
Traceback (most recent call last):
  File "run_glue.py", line 475, in <module>
    main()
  File "run_glue.py", line 376, in main
    torch.cuda.set_device(args.local_rank)
  File "/home/zhanghaipeng/.conda/envs/py36_zhp/lib/python3.6/site-packages/torch/cuda/__init__.py", line 264, in set_device
    torch._C._cuda_setDevice(device)
RuntimeError: cuda runtime error (10) : invalid device ordinal at /opt/conda/conda-bld/pytorch_1550852152579/work/torch/csrc/cuda/Module.cpp:34
```

第二：使用horovod。horovod的使用是通过拉取镜像的方式。具体可以读一读[文档](https://github.com/horovod/horovod/blob/master/docs/docker.rst)，相比前者，显得要清爽的多。期间要保证首先实现免密登陆。

在配置Docker的过程中，执行下述命令：

```
horovodrun --verbose -np 2 -H hpc1:1,hpc4:1 -p 12345 python pytorch_synthetic_benchmark.py
```

会遇到如下问题：

```
Filtering local host names.
Checking ssh on all remote hosts.
ssh not successful for host hpc4:
Permission denied, please try again.
Permission denied, please try again.
root@hpc4: Permission denied (publickey,password).
```

怀疑是端口映射的问题（暂未解决）。最终期待的运行方式，[类似这样](https://blog.csdn.net/weixin_38340975/article/details/87971642#root_ssh_117)。

第三: 在写这篇博客时候，头条的[BytePS](https://github.com/bytedance/byteps)也发布了，和Horovod可以对比一下。


### 梯度累积

所谓梯度累积，是用只能塞下batch\_size=8的GPU，去实现batch\_size=32的效果。思路很简单，4个batch后再去更新梯度。但是要注意的是，框架中的backward是针对一个batch的，因此，累积后要除累积步数(=4)。流程如下：

```
gradient_accumulation_steps=4
for step in total_steps:
	 loss = get_loss(...)
	 if gradient_accumulation_steps > 1:
	     loss = loss/gradient_accumulation_steps
	 if (step+1)%gradient_accumulation_steps == 0:
	     optimizer.step()
```

具体代码可以看[tacred\_run\_classifier.py](https://github.com/zhpmatrix/BERTem/blob/master/examples/tacred_run_classifier.py)中与train相关的逻辑。


### 梯度Checkpoint

在神经网络的forward函数中，每层的激活函数值计算之后需要保存下来，当backward时，根据损失函数值和该层对应的激活函数值计算梯度。也就是说，这种情况下显存占用与
层数成正比。当然可以不存储激活值，在backward时，需要激活函数值的时候重新进行forward就可以了。

分析上述讨论，原始的方式是每个层都存储中间计算得到的激活值。比较直接的方法是都不存，不过计算时间感人，其实也就是通过时间换空间，可以用更大的模型了。那么自然有折中的方式，只存部分层的激活函数值。当backward需要激活函数值的时候，取最近的激活值就行。

按照PyTorch官方的一个说法：通过这种方式，可以实现训练4x-10x大的模型。其实，考虑到显存受限，这个区间个人觉得已经很不错了。

### 总结

上述这些技术都是可选的，并不一定要选择，比如参考6中分享了一些优化技术。想再次分享一个观点，一个模型的训练是一个系统工程，可以从各个层面去优化，技术性的或者非技术性的。个人认为，相比技术性的优化，非技术性的优化更重要一些，也就是解决问题的一个顶层思路。另一方面，必要时刻思考一下自己的的资源利用率，有没有最大化生成工具的效能，现在反思一下，实际上我们可能在无意间会造成大量的无效碳排放。

对于多数软件系统，我们总是需要在计算，存储和I/O之间进行trade-off。同样对于大模型的训练，可以从软件层进行优化，比如更节约内存，更快收敛的optimizer，model arch等，可以从硬件系统层进行优化，更好的显卡，更大的带宽等。本着对"分层"和"抽象"的认识，可以更好地做出一些优化决策。


参考：

1.[apex的实践](https://juejin.im/post/5cb04cd15188251af26d25d6)

给出了一些apex实践中遇到的坑。

2.[ResNet50的测试结果](https://github.com/suvojit-0x55aa/mixed-precision-pytorch)

从作者给出的结果来看，在精度没有显著丢失的前提下，模型大小减少了一倍，同时速度有提升。相比于这篇博客的结果，虽然速度提升不是很明显，但是应该也是合理的，fp32->fp16是有代价的。


3.[pytorch gradient checkpoint](https://github.com/prigoyal/pytorch_memonger/blob/master/tutorial/Checkpointing_for_PyTorch_models.ipynb)

主要使用的模块是torch.utils.checkpoint，不但适用于序列模型，同时适用于很多其他的模型。这篇是应该是最好的tutorial，没有之一吧。

4.[tensorflow gradient checkpoint](https://github.com/cybertronai/gradient-checkpointing)

有非常棒的讲解原理的动图。

5.《Divide-and-Conquer Checkpointing for Arbitrary Programs with No User Annotation》

gradient checkpoint的原始论文，38页。

6.[PyTorch性能指南](https://gist.github.com/HudsonHuang/c5137f628667c05c92ed30a2fdb7ffb3)

7.[The Tips On Training Large Batches in PyTorch](https://medium.com/huggingface/training-larger-batches-practical-tips-on-1-gpu-multi-gpu-distributed-setups-ec88c3e51255)

8.[Training Large Model: introduction, tools and examples](https://huggingface.co/pytorch-transformers/examples.html#introduction)

huggingface出品的pytorch-transformer中讨论的关于大模型的训练。
