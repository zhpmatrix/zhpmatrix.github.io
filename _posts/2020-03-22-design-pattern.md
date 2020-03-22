---
layout: post
title: "[Python]算法开发中的设计模式"
excerpt: "Alex Martelli说，设计模式是被发现，而不是被发明出来的。"
date: 2020-03-22 10:25:00
mathjax: true
---

**前言：**写算法Pipeline，或许同样需要设计模式的加持。当一个模型的完整生命周期结束的时候，如果不想留下一地鸡毛，那么或许可以向设计模式求助。这篇博客，只梳理结合自己实践，个人比较感兴趣的一些设计模式（所以，不全）。

#### 工厂模式

该模式实在是一个常用的模式，可以使用的场景很多，在众多的设计模式中，排名第一，当之无愧。算法Pipeline经常面临的一个问题是：**要处理不同格式的数据。**通常情况下，总是要为每种格式的数据写特定的处理逻辑，针对不同格式的数据，调用特定的逻辑，但是这样的代码组织会显得有点“散”。

需要一个接口能够统一不同的处理逻辑：这个接口负责接收不同格式的数据输入，返回对应的数据。就像一个工厂一样，甲方大大给需求就OK，具体的产品生产交给对应的车间同学。写出的核心代码，类似如下（以一个能够处理JSON和XML格式的工厂接口为例）：

```
def data_factory(filepath):
	if filepath.endswith('json'):
		chejian = JSONCheJian
	elif filepath.endswith('xml'):
		chejian = XMLChejian
	else:
		raise ValueError('对应车间还没成立呢！')
	return chejian(filepath)
```

观察上述代码，核心逻辑就是**转发控制**。具体的实现方式是：借助文件后缀，返回对应的类。设计模式更多时候是一种设计思想，具体实现与编程语言有一定关系。如C++/Java/Python等。

在Caffe的源码中，工厂模式也是核心设计模式。

回顾算法开发过程，用统一的接口处理不同格式的数据是场景之一。那么，同样的数据，不同的metric逻辑，如何设计统一接口呢？预训练过程中，不同的BERT变种作为基础模型呢？

#### 建造者模式

多数情况下，算法开发实际上是在做一套能够找到最优解的系统，而这套系统具有“Pipeline”的特点，是一个线性的组织流程。比如：

```
def run():
	[step() for step in (load_data, train_data, eval_data, test_data)]
```
#### 原型模式

copy.copy和copy.deepcopy()，该模式主要用于创建对象的clone。因为个人见到的场景不是很多，且不谈。印象中，在实现论文《Learning without Forgetting》的时候，有用过model的clone。除此之外，为了防止数据污染，要小心谨慎的使用深浅copy。


#### 适配器模式

该模式也是非常有趣的啊。假设有三种动物，如下：

```
class Dog:
	def wang():
		print('wang')
class Duck:
	def ga():
		print('ga')
class Chicken():
	def ji():
		print('ji')
```
现在，想只调用wang()函数，就能实现实际调用三种动物的叫声函数，怎么办？对Dog而言，直接调用wang()就是实际调用wang()函数，但是对Duck和Checken而言，需要实际调用的是ga和ji函数。**因此，这里需要一层转发：(Duck, wang)->ga和(Chicken,wang)->ji，而执行这个转发逻辑的就是适配器。**如下：

```
class Adapter:
	def __init__(self, obj, adapted_method):
		self.obj = obj
		self.__dict__.update(adapted_method)
duck = Duck()
new_duck = Adapter(duck, dict(wang=duck.ga))
chicken = Chicken()
new_chicken = Adapter(chicken, dict(wang=chicken.ji))
```

或者简单理解为：函数重命名。这里需要理解**self.\_\_dict\_\_**。

#### 装饰器模式

计算一个函数的执行时间，用装饰器来实现，想必很多人已经很熟悉了。示例代码如下：

```
def timer(func):
    def inner(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        print(end-start)
    return inner
    
def func():
	pass

#调用func函数并统计函数的运行时间
@timer
func()
    
```

#### 享元模式

该模式是Cache思想在OOP编程中的体现。主要目的在于优化性能和内存使用，因而不是个人目前关注的重点。

#### 解释器模式

这种模式非常有用。针对解释器，从字面含义上来看，就是编译原理中的解释器。通过读取编辑器写的字符串，经过词法，句法，语义解析等，转化为机器能够理解的语言，之后汇编，链接，可执行等（对C是这样）。因此，这里也是这样的，使用上的体验是：通过定义字符串的方式，操作类和类方法等。这套字符串语言也称DSL。本质上是建立字符串到类或者类方法的mapping关系。

上文提到的适配器模式中的两条规则，其实也可以写成这样。从另外一个角度来说，设计模式是可以结合使用的。

#### 策略模式

解决一个问题时，可以有多种解法，每种解法各有优缺点。当希望在用户端对后端解法切换没有明显感知的时候，就需要策略模式了。典型的例子如：Python中的sorted函数，通过设定key的值，采用不同的排序策略。**在算法开发中，由于针对每个目的的Trick都很多，因此采用该模式实在是一个很朴素的做法了。**

#### 模板模式

主要目的是**消除代码冗余**。将不同算法中相同的部分抽取出来，形成一个模板。通过将不同的部分作为一个参数action传入模板函数，实现不同的算法。同时，不建议用id作为参数传入模板函数，因为这样模板函数要不断修改，同时id的含义不明确。

实际上，和策略模式一样，在日常的算法开发中，该模式同样可以被很广泛的应用。

**总结：**结合算法开发的日常，设计模式对于算法Pipeline的管理应该是有效的。此外，在很多开源框架的源码中，实现了各种各样的设计模式。本质上，是基于设计思想，利用语言Feature做实现。这些设计模式可以方便的clone对象，实现Cache以提升性能，消除冗余设计，提升复用性和更加灵活的控制代码等。每隔一段时间，重新思考一下自己的开发过程，看是否是一个模块被自己改了N多次，一个逻辑被自己以各种方式写了M多次，每次需要更新代码的时候，找不到自己写的逻辑去哪里了...（对，说的是我啦。）