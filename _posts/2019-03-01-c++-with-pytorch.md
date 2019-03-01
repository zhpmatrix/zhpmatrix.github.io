---
layout: post
title: "[PyTorch]PyTorch的C++前端和模型部署"
excerpt: "PyTorch1.0发布后，PyTorch的春天似乎就到了。在此之前，关于PyTorch的吐槽主要集中在不适用生产环境，个人认为某种意义上就是缺少C++的前端。最近用PyTorch复现一篇文章，顺道考察了一下C++端的应用。是的，我从没有喜欢过Tensorflow。"
date: 2019-03-01 18:43:00
mathjax: true
---

<script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=default"></script>

### 一.前言

差不多一年前的这个时候，在狗厂实习的时候，主要用PyTorch做一些事情。那个时候针对PyTorch的模型部署问题，主要讨论ONNX。想像一下今天的DL框架格局，PyTorch，Tensorflow，Keras，Caffe，Caffe2等，持久化模型之间不兼容。常见的一种情况是，一篇论文基于不同框架写不同版本的代码。那么，很显然的一个需求是：

**一个框架下的模型如何可以转化为另一个框架下的模型？**

相关工作有一些，ONNX是其中一个，微软也做过类似工作。但是问题是总会遇到一些无法直接转换的组件。在今天，仍旧可以看到的现象是一篇论文，两个版本的代码实现。早期的ONNX的一个经典用例是将PyTorch的模型通过ONNX转化为Caffe2的模型然后部署在移动IOS端。比如我去年实习期间业余时候尝试的一个[项目](https://github.com/zhpmatrix/Pytorch-SqueezeNet)。

在多个DL框架争雄的局势下，上述的需求就是硬需求，相关工作在推进，希望取得进展吧。不过，这里引发的一个问题是：多框架场景下的多样化部署。这在框架角度给出了一个思考维度。

### 二.用C++载入PyTorch模型

早期的PyTorch只有Python前端，所谓的口号"Python优先"，对于学术界的大部分同学，不关心部署性能，只关心模型等学术问题，因此这样是OK的。但是放在工业界就不行了，模型是要上线的。Python语言太慢，可移植性和适用性根本无法和C++相比。考虑到部署问题，PyTorch总不是最佳的选择。当时的一个想法是，PyTorch训练模型，然后前向推断时将结构和参数灌入到C++代码中，这估计也是早些年的一些做法。但是调研之后，将PyTorch的C++后端拉出来并不容易，而且如果从C++原生代码来写起，工作量也很大。因此，希望有一个C++前端方便做推断部署，相比于此，训练倒是其次。

千呼万唤始出来。PyTorch1.0发布了，截止目前最新版为PyTorch1.0.1。这样，稍后的业界的算法同学的工作流程可能就会变成这样：

论文发布->PyTorch开源代码(或者自己实现)->训练模型->导出模型->载入模型(C++/Python/其他框架/其他硬件平台)

通常PyTorch可以作为想法研究的工具，不作为生产工具。这样一来，研究后的成果可以直接上线，完美。

下面给出一个基本的使用流程。

#### 1.Python端导出模型

```
import torch
import torchvision.models as models

resnet = torch.jit.trace(models.resnet18(), torch.rand(1,3,224,224))
output=resnet(torch.ones(1,3,224,224))
print(output)
resnet.save('resnet.pt')
```

#### 2.C++端载入模型

```
#include <iostream>
#include <torch/script.h>

int main(int argc, const char* argv[]){
    if (argc != 2){
        std::cerr << "where is your model?" << std::endl;
        return -1;
    }
    std::shared_ptr<torch::jit::script::Module> module = torch::jit::load(argv[1]);
    assert(module != nullptr);
    std::cout << "load successfully!" << std::endl;

    //auto module = torch::jit::load("../resnet.pt");
    std::vector<torch::jit::IValue> inputs;
    inputs.push_back(torch::ones({1,3,224,224}));
    at::Tensor output = module->forward(inputs).toTensor();
    std::cout << output.slice(1,0,5);
    return 0;
}
```

#### 3.编译C++代码

C++中使用的关于PyTorch的头文件，主要来自PyTorch提供了一个模块libtorch。不瞒您说，libtorch就是PyTorch中C++前端最为关键的模块了。当然PyTorch的C++后端是Aten模块，基于该模块有Autograd等，主要实现是关于Tensor的各种运算等。

#### 4.运行C++代码

```
./example-cpp resnet.pt
```

在上述过程中，需要编写脚本工具，链接到libtorch库，实现完整的编译过程。完整项目可以看我的[Github链接](https://github.com/zhpmatrix/load-pytorch-model-with-c-)。

其实，导出的模型还可以直接用于node.js呢，具体可以参考资料1。

### 三.PyTorch的C++前端

拥有一个完善的C++前端，当然可以完成上述任务。但是对于C++的同学来说，相当于又有一个C++的深度学习框架，基于C++的DL框架有，但是不多。Caffe作为老大哥，也多是针对CV的同学。自己在做NLP实习的时候也用过一个小众的C++框架，有七牛的朋友讲，公司内部也有自己的C++框架。按照Tensorflow，MXNET等的发展路子，多是写一个C++的框架，然后写一层Python的皮。但是PyTorch的框架本身就是基于Python完成的，注意此处与后端没有C++代码是两码事情。总之，现在有了一套新的可用的C++的API。

给出一些代码作为代码，感受一下画风的变化。

原来的Python代码，我们可以这样实现一个模型：

```
import torch

class Net(torch.nn.Module):
  def __init__(self, N, M):
    super(Net, self).__init__()
    self.W = torch.nn.Parameter(torch.randn(N, M))
    self.b = torch.nn.Parameter(torch.randn(M))

  def forward(self, input):
    return torch.addmm(self.b, input, self.W)
```

现在用C++可以直接这样实现，如下：

```
#include <torch/torch.h>

struct Net : torch::nn::Module {
  Net(int64_t N, int64_t M) {
    W = register_parameter("W", torch::randn({N, M}));
    b = register_parameter("b", torch::randn(M));
  }
  torch::Tensor forward(torch::Tensor input) {
    return torch::addmm(b, input, W);
  }
  torch::Tensor W, b;
};
```

从官方的文档来看，目前的C++前端已经相对完善。可以实现定义模型，载入数据，写训练循环，CPU/GPU切换，Checkpointing/Recovering等。

敲黑板，基于Caffe写C++不开心的同学，可以基于PyTorch来写C++换个心情了。

### 四.后记

这篇博客没什么技术干货，主要是为PyTorch的C++端打Call吧。涉及到的一些技术原理与torch.jit有关，相关细节和讨论可以参考资料1。此外，这篇博客算是一个技术体验吧，实际上至于真正用到工业生产环境时候的感受怎样，还需要进一步观察。人生苦短，我用PyTorch，是的，从没有喜欢过Tensorflow。(_TF粉不要打我，逃......_)

参考资料：

1.《PyTorch under the hood: A guide to understand PyTorch internals》

2.[Using the PyTorch C++ Frontend](https://pytorch.org/tutorials/advanced/cpp_frontend.html#)

3.[Loading A PyTorch Model in C++](https://pytorch.org/tutorials/advanced/cpp_export.html)

4.[Transfering a Model from PyTorch to Caffe2 and Mobile using ONNX](https://pytorch.org/tutorials/advanced/super_resolution_with_caffe2.html)

5.[Deploying a Seq2Seq Model with the Hybrid Frontend](https://pytorch.org/tutorials/beginner/deploy_seq2seq_hybrid_frontend_tutorial.html#)
















