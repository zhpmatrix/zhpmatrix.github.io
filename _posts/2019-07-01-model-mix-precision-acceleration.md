---
layout: post
title: "[Pytorch]基于混和精度的模型加速"
excerpt: "pytorch中基于apex使用混合精度加速的四个步骤，原始非apex加速代码也可以做对应的修改，体验fp16可能带来的加速效果。"
date: 2019-07-01 18:43:00
mathjax: true
---

这篇博客是在**pytorch中基于apex使用混合精度加速**的一个偏工程的描述，原理层面的解释并不是这篇博客的目的，不过在参考部分提供了非常有价值的资料，可以进一步研究。

[apex](https://github.com/NVIDIA/apex)是nvidia的一个pytorch扩展，用于支持混合精度训练和分布式训练。其中，混合精度训练可以通过简单的方式开启自动化实现，组里同学交流的结果是：**一般情况下**，自动混合精度训练的效果不如手动修改。分布式训练中，有社区同学心心念念的syncbn的支持。关于syncbn，在去年做CV的时候，我们就有一些来自民间的尝试，不过具体提升还是要考虑具体任务场景。

**那么问题来了，如何在pytorch中使用fp16混合精度训练呢？**

**第零：混合精度训练相关的参数**

```
parser.add_argument('--fp16',
                        action='store_true',
                        help="Whether to use 16-bit float precision instead of 32-bit")
parser.add_argument('--loss_scale',
                        type=float, default=0,
                        help="Loss scaling to improve fp16 numeric stability. Only used when fp16 set to True.\n"
                             "0 (default value): dynamic loss scaling.\n"
                             "Positive power of 2: static loss scaling value.\n")
```

**第一：模型参数转换为fp16**

nn.Module中的half()方法将模型中的float32转化为float16，实现的原理是遍历所有tensor，而float32和float16都是tensor的属性。也就是说，一行代码解决，如下：

```
model.half()
```
**第二：修改优化器**

在pytorch下，当使用fp16时，需要修改optimizer。类似代码如下（代码参考[这里](https://github.com/huggingface/pytorch-pretrained-BERT/blob/dad3c7a485b7ffc6fd2766f349e6ee845ecc2eee/examples/run_classifier.py)）：

```
# Prepare optimizer
    if args.do_train:
        param_optimizer = list(model.named_parameters())
        no_decay = ['bias', 'LayerNorm.bias', 'LayerNorm.weight']
        optimizer_grouped_parameters = [
            {'params': [p for n, p in param_optimizer if not any(nd in n for nd in no_decay)], 'weight_decay': 0.01},
            {'params': [p for n, p in param_optimizer if any(nd in n for nd in no_decay)], 'weight_decay': 0.0}
            ]
        if args.fp16:
            try:
                from apex.optimizers import FP16_Optimizer
                from apex.optimizers import FusedAdam
            except ImportError:
                raise ImportError("Please install apex from https://www.github.com/nvidia/apex to use distributed and fp16 training.")

            optimizer = FusedAdam(optimizer_grouped_parameters,
                                  lr=args.learning_rate,
                                  bias_correction=False,
                                  max_grad_norm=1.0)
            if args.loss_scale == 0:
                optimizer = FP16_Optimizer(optimizer, dynamic_loss_scale=True)
            else:
                optimizer = FP16_Optimizer(optimizer, static_loss_scale=args.loss_scale)
            warmup_linear = WarmupLinearSchedule(warmup=args.warmup_proportion,
                                                 t_total=num_train_optimization_steps)

        else:
            optimizer = BertAdam(optimizer_grouped_parameters,
                                 lr=args.learning_rate,
                                 warmup=args.warmup_proportion,
                                 t_total=num_train_optimization_steps)		
```

**第三：backward时做对应修改**

```
 if args.fp16:
 	optimizer.backward(loss)
 else:
      loss.backward()
```

**第四：学习率修改**

```
if args.fp16:
      # modify learning rate with special warm up BERT uses
      # if args.fp16 is False, BertAdam is used that handles this automatically
     lr_this_step = args.learning_rate * warmup_linear.get_lr(global_step, args.warmup_proportion)
     for param_group in optimizer.param_groups:
            param_group['lr'] = lr_this_step
     optimizer.step()
     optimizer.zero_grad()
```

参考资料：

1.[nv官方repo给了一些基于pytorch的apex加速的实现](https://github.com/NVIDIA/DeepLearningExamples)

实现是基于fairseq实现的，可以直接对比[代码1-apex版](https://github.com/NVIDIA/DeepLearningExamples/blob/master/PyTorch/Translation/Transformer/fairseq/optim/adam.py)和[代码2-非apex版(fairseq官方版)](https://github.com/pytorch/fairseq/blob/master/fairseq/optim/adam.py)，了解是如何基于apex实现加速的。

2.[nv官方关于混合精度优化的原理介绍](https://docs.nvidia.com/deeplearning/sdk/mixed-precision-training/index.html)

按图索骥，可以get到很多更加具体地内容。

3.[低精度表示用于深度学习
训练与推断](http://market.itcgb.com/Contents/Intel/OR_AI_BJ/images/Brian_DeepLearning_LowNumericalPrecision.pdf)

感谢团队同学推荐。





