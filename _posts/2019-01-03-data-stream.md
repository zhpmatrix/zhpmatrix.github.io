---
layout: post
title: "数据流"
tags: [LeetCode]
excerpt: "传统算法中的数据流问题，一个经典的数据场景，流式数据处理"
date: 2019-01-03 18:53:00
mathjax: true
---

#### 1.[数据流的中位数](https://leetcode-cn.com/problems/find-median-from-data-stream/)

中位数是有序列表中间的数。如果列表长度是偶数，中位数则是中间两个数的平均值。例如，

[2,3,4] 的中位数是 3

[2,3] 的中位数是 (2 + 3) / 2 = 2.5

设计一个支持以下两种操作的数据结构：

void addNum(int num) - 从数据流中添加一个整数到数据结构中。

double findMedian() - 返回目前所有元素的中位数。

示例：

```
addNum(1)
addNum(2)
findMedian() -> 1.5
addNum(3) 
findMedian() -> 2
```
进阶:

如果数据流中所有整数都在 0 到 100 范围内，你将如何优化你的算法？

如果数据流中 99% 的整数都在 0 到 100 范围内，你将如何优化你的算法？

第一种思路：用一个数组存储所有数据，每次添加一个新的数据的时候，对数组排序一次。addNum时间复杂度为**O(n)+O(nlogn)**，findMedian查找复杂度为O(1)。这种思路是批式处理思想的体现，多见于数据分析过程中，容易想到但是冗余较多。体现在两个地方：

第一：数组添加数据的时候append操作

第二：每次更新数组后都要排序

既然findMedian要求一个有序数组就OK了，那么在数据流过程中，可以维护一个有序的数据结构。那么addNum的时间复杂度可以变为**O(nlgn)**。这种思路是流式处理思想的体现。

第三：结合数组和中位数的特点，空间换时间，addNum的时间复杂度变为**O(lgn)**。这种思路也可以理解为对问题进一步分解，将一个原来一步解决的问题，分为两步，但是第二步的时间复杂度较低，这是一个分支优化。[这里是一个非常干净的方案](https://zhuanlan.zhihu.com/p/85283794)。


#### 2.[数据流中的移动平均值](https://leetcode-cn.com/problems/moving-average-from-data-stream)

给定一个数据流输入 a1，a2，…，an，…，和固定窗口大小为n，计算固定窗口内的数据的平均值。

测试用例如下：

```
m = MovingAverage(3)
print(m.next(1))
print(m.next(10))
print(m.next(3))
print(m.next(5))
print(m.next(3))
print(m.next(5))
```
预期输出：
```
1.0
5.5
4.666666666666667
6.0
3.6666666666666665
4.333333333333333
```

基本思路：选用一个合适的数据结构用来**模拟**数据流。如下：

```
class MovingAverage:
	def __init__(self, size: int):
		from collections import deque
		#通过设定deque的最大值模拟固定窗口
		self.deque = deque(maxlen=size)
	def next(self, val:int)->float:
		#通过appendleft模拟数据流动
		self.deque.appendleft(val)
		return sum(self.deque) / len(self.deque)
```
deque是一种直接使用比较清爽的结构，用其他数据结构也可以实现。

#### 3.蓄水池采样

给定一个数据流输入 a1，a2，…，an，…，用等概率的方式采样m个数据。


#### 4.[将数据流变为多个不相交区间](https://leetcode-cn.com/problems/data-stream-as-disjoint-intervals/)

给定一个非负整数的数据流输入 a1，a2，…，an，…，将到目前为止看到的数字总结为不相交的区间列表。

例如，假设数据流中的整数为 1，3，7，2，6，…，每次的总结为：

```
[1, 1]
[1, 1], [3, 3]
[1, 1], [3, 3], [7, 7]
[1, 3], [7, 7]
[1, 3], [6, 7]
```
进阶：
如果有很多合并，并且与数据流的大小相比，不相交区间的数量很小，该怎么办?




