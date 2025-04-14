---
layout: post
title: "Spark从入门到离家出走"
excerpt: "这篇Blog是关于Spark的第二篇，主要回顾了三道题目，分别是词频统计，大文本去重和topK问题。同时在参考部分，列出了一些非常棒的参考资料。"
date: 2017-11-14 19:14:00
mathjax: true
tags: [工程架构]
---

前言: 明白了基本概念，剩下的架构方面的理解就会容易很多。截止写这篇Blog，还没有遇到必须要使用Spark集群的应用场景，但是想到Spark已成工业界标准，还是读了一些资料。本篇Blog是从题目出发加强对Spark的认识，同时为了辅助题目，列出了一些更有技术深度的参考资料，比如对Shuffle的理解，对Spark的性能调优等。在并行应用比赛中对Spark的使用可以参考这篇[博客](https://zhpmatrix.github.io/2017/08/12/spark/)。

从Spark的词频统计代码开始讨论，代码如下：

```python

text_file = sc.parallelize(["hello","hello world"])
counts = text_file.flatMap(lambda line: line.split(" ")) \
             .map(lambda word: (word, 1)) \
             .reduceByKey(lambda a, b: a + b)
for line in counts.collect():
    print line

```

分析上述代码，不严格地说，**flatMap**之后得到\["hello", "hello", "world"\], **map**之后得到(hello, 1), (hello, 1), (world, 1), **reduceByKey**之后得到(hello, 2), (world, 1)。**collect**之后的结果默认是按照词频升序排列的。输出结果如下：

```python

('world',1)
('hello', 2)

```

[补充1: 如何用Spark实现大文本按每行去重操作？]

```python
from pyspark import SparkContext
sc = SparkContext()

text_file_0 = sc.parallelize(["hello","what","hello","do"])
#text_file_1 = sc.parallelize(["1", "2","3","2","1"])
new_text_file = text_file_0.distinct()
for line in new_text_file.collect():
    print(line)
```

输出结果:

```python
hello
what
do
```

如果用sort data.txt \| uniq文本处理命令来实现，实现是按照每行的第一个字符进行比较去重的，不能实现字符串去重。但是，据说上述命令由于中间数据存储在磁盘上，故不会撑爆内存，可以处理几十G的文本。

[补充2: 如何得到词频中的topK个词汇？]

```python
#接补充1的代码
for item in new_text_file.sortBy(lambda x: x[1]).collect():
    print(item)
```

匿名表达式实现的是按照key进行排序，默认从小到大。同时也可以先KV反转，后使用sortByKey排序。

参考：

0.[Spark从零开始](http://www.imooc.com/learn/814)

慕课网讲解非常清晰的内容，但是只是适合入门，没有达到很高的技术深度。

1.[Spark集群中WordCount运行原理](http://kevin12.iteye.com/blog/2275141)

Blog中有一张关于wordcount的图很赞。

2.[Spark的Shuffle过程](https://my.oschina.net/kavn/blog/758389)

以简要的语言解释了Spark的Shuffle过程。

3.[Shuffle过程](https://spark-internals.books.yourtion.com/markdown/4-shuffleDetails.html)

比较详细的阐述了Shuffle过程。

4.[如何对一个大文本进行按每行去重操作?](https://www.zhihu.com/question/28771744)

知乎的一个回答。

5.[Spark Shuffle的基本原理和特性](http://sharkdtu.com/posts/spark-shuffle.html)

简单扼要的Blog内容，重点关注。

6.[Spark性能优化：数据倾斜调优](https://www.iteblog.com/archives/1671.html)

非常棒的Blog！Spark的性能优化包括开发调优，资源调优，数据倾斜调优，和Shuffle调优。在解释数据倾斜问题时，给出了一个词频统计的图，参考5结合该图，有助于理解**Sort Shuffle**的原理。











