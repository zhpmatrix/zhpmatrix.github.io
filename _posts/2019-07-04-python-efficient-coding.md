---
layout: post
title: "[Python]Python高级编程"
excerpt: "《Effective Python》笔记"
date: 2019-07-03 18:43:00
mathjax: true
---

想来每隔一段时间都要写点关于python编程的博客。不知不觉已经写了一些，具体如下：

[深入理解python中的数据结构](https://zhpmatrix.github.io/2017/02/24/python-data-structure/)

[后知后觉函数式编程](https://zhpmatrix.github.io/2017/02/22/python-functional-programming/)

[用进程池Pool进行代码加速](https://zhpmatrix.github.io/2017/11/04/speed-up-python/)

[回调函数，线程安全，Monkey Patch和try/except使用](https://zhpmatrix.github.io/2018/06/14/programming-tricks/)

[记一次Debug经历](https://zhpmatrix.github.io/2017/09/24/python-debug-experience/)

[Pandas引用和复制的PK](https://zhpmatrix.github.io/2017/08/13/view-versus-copy/)

[若干有意思的知识点](https://zhpmatrix.github.io/2017/02/22/python-language-tricks/)

[编程复盘](https://zhpmatrix.github.io/2016/12/04/coding-tricks/)

这里再写一篇，每隔一段时间总觉得python写的不够强，很多地方可以优化。这篇博客更多的是《Effective Python-编写高质量Python代码的59个有效方法》的读书笔记，作者是Google的Brett Slatkin。

(1)itertools的使用

在NER任务中，当得到pos对应的lable之后，需要进一步得到entity，这个时候就可以使用itertools中的groupby来实现。如下：

```
label = [(0,'B-PER'),(1,'I-PER'),(2,'I-PER'),(3,'B-ORG')]
for tag, chunk in groupby(label, lambda x:x[1].split('-')[1]):
	print(tag, ','.join(k for w, k in chunk))
```

输出如下：

```
PER B-PER,I-PER,I-PER
ORG B-ORG
```

(2)生成器表达式(**dataloader中可以使用，yield**)

warning：从身边的反馈来看，生成器的使用不当也会带来一些奇怪的问题。


可以避免内存用量问题，同时串在一起的生成器表达式执行速度很快。代码如下：

```
it = (len(x) for x in open('data.txt'))
roots = ((x,x**0.5) for x in it)
print(next(roots))
```

（3）用列表推导来取代map和filter

（4）遵循pep8风格指南

a.使用space(空格)来表示缩紧，而不要用tab（制表符）

b.判断somelist是否为[]或者‘’等空值，不要使用

```
if len(somelist) == 0
```

而是使用

```
if not somelist
```

（5）try/except/pdb的使用方式(**书中建议：尽量使用异常来表示特殊情况，而不要返回None**)

三者结合的新方式，如下：

```
try:
	#step0
except:
	import pdb;pdb.set_trace()
else:
	#step1
```

(6)考虑用生成器来改写直接返回列表的函数（节约内存的大杀器，dataloader实现需关注）

(7)按照列表中字符串的长度给列表进行排序

```
names = ['zhpmatri','zhp','matrix']
sorted(names, key=lambda x: len(x))
```

（8）并发和并行(在数据处理的相关任务中可以重点关注)

a.用subprocess模块来管理子进程

b.可以用线程来执行阻塞式I/O，但不要用它做平行计算

c.在线程中使用Lock来防止数据竞争

d.用Queue来协调各线程之间的工作

e.考虑用协程来并发地运行多个函数

f.考虑用concurrent.futures来实现真正的平行计算

(9)eval来执行一个字符串表达式，使用repr输出一个来自logging的值，可以最大化地保持值本身的信息

（10）性能分析

python提供了两种内置性能分析器，分别叫做profile和cProfile。后者会更好一些，使用后者时对受测程序的效率只会产生很小的影响。而前者会产生较大的开销，使得测试结果变得不准确。

（11）内存使用和泄漏

tracemalloc

总结：比起用Python做后台研发，算法方面对Python的特性需求感觉并不是很高。这应该与两个不同工种的工作流有关。多数情况下，模型代码往往有几个文件组成，即使是框架，也并不需要相对复杂的语言特性。但是对特性的了解，可以帮助我们写出更fancy，更pythonic的code吧。












