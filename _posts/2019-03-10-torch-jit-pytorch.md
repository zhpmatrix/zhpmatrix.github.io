---
layout: post
title: "[PyTorch]直观认识torch.jit模块"
excerpt: "在之前的一篇博客中讨论了PyTorch的C++前端，而这篇文章是关于PyTorch模型部署的第二篇博客，用具体的代码讨论了Tracing和Script两种方式的区别和联系。"
date: 2019-03-09 18:43:00
mathjax: true
---

<script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=default"></script>

PyTorch1.0后，可以通过TorchScript的方式创建序列化和可优化的模型。可以通过两种方式，分别是Tracing和Script将一个Python代码转化为TorchScript代码，继而导出相应的模型可以继续被优化，同时被C++所调用，最终实现对生产环境下的支持(考虑到多线程执行和性能原因，一般Python代码并不适合做部署)。关于这部分内容的讨论，这已经是第二篇文章了，第一篇文章在这里，[PyTorch的C++前端和模型部署](https://zhpmatrix.github.io/2019/03/01/c++-with-pytorch/)。


### Tracing方式

```
def my_function(x):
    return x * 2

ftrace = torch.jit.trace(my_function, (torch.ones(2,2)))

y = torch.ones(2,2).add_(1.0)

print(ftrace.graph)
print(ftrace.forward(y))

```

输出结果如下：

```
graph(%x : Float(2, 2)) {
  %1 : Long() = prim::Constant[value={2}]()
  %2 : Float(2, 2) = aten::mul(%x, %1)
  return (%2);
}

tensor([[4., 4.],
        [4., 4.]])


```

修改y的值为，如下：

```
y = torch.zeros(2,2).add_(1.0)
```

得到结果，如下：

```

graph(%x : Float(2, 2)) {
  %1 : Long() = prim::Constant[value={2}]()
  %2 : Float(2, 2) = aten::mul(%x, %1)
  return (%2);
}

tensor([[2., 2.],
        [2., 2.]])

```

完全符合预期！实际上，这个例子正是Tracing适合处理的场景，比如对resnet18类似的模型，可以通过Tracing方式得到ScriptModule。作为对比，再来看一个函数实现：

```
def my_function(x):
    if x.mean() > 1.0:
        r = torch.tensor(1.0)
    else:
        r = torch.tensor(2.0)
    return r

ftrace = torch.jit.trace(my_function, (torch.ones(2,2)))
y = torch.ones(2,2).add_(1.0)
print(ftrace.graph)
print(ftrace.forward(y))

```


输出结果如下：

```
graph(%x : Float(2, 2)) {
  %4 : Float() = prim::Constant[value={2}]()
  %5 : Device = prim::Constant[value="cpu"]()
  %6 : int = prim::Constant[value=6]()
  %7 : bool = prim::Constant[value=0]()
  %8 : bool = prim::Constant[value=0]()
  %9 : Float() = aten::to(%4, %5, %6, %7, %8)
  %10 : Float() = aten::detach(%9)
  return (%10);
}

tensor(2.)

```

结果目前来看，符合预期。那么修改y的值呢？如下：

```
y = torch.zeros(2,2).add_(1.0)
```

输出结果为：

```
tensor(2.)
```

竟然不变！难道不应该是tensor(1.)吗？其实这样是符合预期的。Tracing方式对于含有if和for-loop的场景失效。而这种场景的一个经典使用就是RNN系的模型，所以必须解决这个问题。解决方式就是Script方式，代码如下。


### Script方式

```
@torch.jit.script
def my_function(x):
    #if x.mean() > 1.0:
    if bool(x.mean() > 1.0):
        #r = torch.tensor(1.0)
        r = 1
    else:
        #r = torch.tensor(2.0)
        r = 2
    return r

y = torch.ones(2,2).add_(1.0)
print(my_function.graph)
print(my_function(y))

```


输出结果如下：

```
graph(%x : Tensor) {
  %2 : float = prim::Constant[value=1]()
  %5 : int = prim::Constant[value=1]()
  %6 : int = prim::Constant[value=2]()
  %1 : Tensor = aten::mean(%x)
  %3 : Tensor = aten::gt(%1, %2)
  %4 : bool = prim::TensorToBool(%3)
  %r : int = prim::If(%4)
    block0() {
      -> (%5)
    }
    block1() {
      -> (%6)
    }
  return (%r);
}

2

```

修改y的值为，如下：

```
y = torch.zeros(2,2).add_(1.0)
```

得到结果1，完全正确！

### Tracing&Script混合方式

综合上述情况，Script方式适合解决带有if和for-loop的情况，那么问题来了，能否用Script方式去修饰没有if和for-loop的情况呢？结论是显然的，这里不再写代码了。同样，二者的混合使用也是一种场景。

### Tracing&Script的调用关系

Scripted的函数可以调用Tracing过的函数。比如seq2seq框架中，decoder端的beam search一般通过Script修饰，但是可以调用Tracing过的encoder模块。同样，Tracing过的函数可以调用Scripted的函数。至于如何调用，取决于要实现的逻辑的控制流(if&for-loop)的比例。

### 模型保存和加载

save方式是torch.jit.ScriptModule的内置方法，并行于Tracing和Script。这就意味着被修饰过的模型可以直接save。载入的方式在开篇给出的第一篇文章中介绍了C++的载入方式，同样可以通过torch.jit.load()的方式载入。

这篇博客暂时没有探讨Tracing和Script内部的机制，只是从使用层面进行了简单分析。直觉上来看，Script的应用效率应该是要低于Tracing的，但是Tracing处理对象的灵活性是要低于Script的，二者是否在将来会合并成一种更加合理的机制，目前未知，期待吧。同时，从上述代码来看，使用Script来修饰函数的时候，原始的一些代码逻辑需要做对应修改，这部分内容在代码的warning中会提到。至于如何将torch.jit应用于一个复杂模型的持久化，具体改造方式可以读官方文档。


参考文章：

1.[torch.jit](https://pytorch.org/docs/stable/jit.html)

2.[Caffe2+PyTorch=PyTorch1.0](https://www.jqr.com/article/000193)

3.[PyTorch的C++前端和OpenCV混合编译](https://zhuanlan.zhihu.com/p/52154049)

4.Christian S.Perone《PyTorch under the hood: A guide to understand PyTorch internals》














