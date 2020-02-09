---
layout: post
title: "[LeetCode]Hash，值得拥有"
excerpt: ""
date: 2020-01-21 18:53:00
mathjax: true
---

总结：Hash的题目，对于简单水平，一般考虑的是collections的应用，重在检索。但是有用Hash做题的想法是无比重要的。

#### 0.Python中Hash的基本实现

直接写代码：

```
nums = [1,3,4,3,1]
hashmap = {}
for num in nums:
	if num not in hashmap:
		hashmap[num] = 1
	else:
		hashmap[num] += 1
return hashmap
```
不过，如果是为了快速AC代码，一般可以直接采用collections中的实现，如下：

```
from collections import Counter
nums = [1,3,4,3,1]
hashmap = Counter(nums)
return hashmap
```

#### 1.[快乐数](https://leetcode-cn.com/problems/happy-number/)，这是一道很快乐的题目

编写一个算法来判断一个数是不是“快乐数”。

一个“快乐数”定义为：对于一个正整数，每一次将该数替换为它每个位置上的数字的平方和，然后重复这个过程直到这个数变为 1，也可能是无限循环但始终变不到 1。如果可以变为 1，那么这个数就是快乐数。

示例如下：

```
输入: 19
输出: true
解释: 
12 + 92 = 82
82 + 22 = 68
62 + 82 = 100
12 + 02 + 02 = 1
```
乍一看这道题目，最简单的思路：模拟？于是写下代码：

```
	while n != 1:
		n = sum([int(char) ** 2 for char in str(n)])
		if n == 1:
			return True
```
那么，如果n永远不会等于1呢？代码就hang住了。“永远不会等于1”的含义是：

（1）当前执行结果和之前所有结果都不同，且都不等于1

（2）当前执行结果和之前某次结果相同，但不等于1。意味着陷入了循环，出不来。

因此，这就是本题的特色。先看一种思路：找规律。规律如果能够找到，代码很简单；如果没有规律或者没有耐心找到规律，可能就比较困难了。这里的规律是：

> n = 4时，永远无限循环下去，怎么用解析的方式证明？

那么，如此一来，代码就很简单了。如下：

```
while True:
	n = sum([int(char) ** 2 for char in str(n)])
	if n == 4:
		return False
	if n == 1:
		return True
```
这里的解法是针对（2）的。那么，**需要思考的问题是（1）会不会发生？**围绕（2），还有两种比较经典的思路。第一种，直接翻译（2）的条件，用一个set记录之前出现过的所有结果。另一种思路和判断链表中是否有环类似，也就是快慢指针的思路。代码如下（足够优美）：

```
slow = n
fast = sum([int(i) ** 2 for i in str(n)])
while slow != fast:
	slow = sum([int(i) ** 2 for i in str(slow)])
	fast = sum([int(i) ** 2 for i in str(fast)])
	fast = sum([int(i) ** 2 for i in str(fast)])
return slow == 1
```

#### 2.[存在重复元素II](https://leetcode-cn.com/problems/contains-duplicate-ii/submissions/)

题目描述：给定一个整数数组和一个整数 k，判断数组中是否存在两个不同的索引 i 和 j，使得 nums [i] = nums [j]，并且 i 和 j 的差的绝对值最大为 k。

基本思路：通过简单的O(n^2)的时间复杂度的两次循环可以解决问题，不过会超时。本质原因在于：计算存在冗余。那么，一种直接的思路是：访问过的就存下来。代码如下：

```
	num2id = {}
	for i, v in enumerate(nums):
		#将时间开销放在基于数据结构的高效检索上
		if v in num2id and (i-num2id[v]) <= k:
			return True
		else:#维护hash结构
			num2id[v] = i
	return False
```

该题所体现的思想可以用在很多地方，比如[两数之和](https://leetcode-cn.com/problems/two-sum/submissions/)问题。
