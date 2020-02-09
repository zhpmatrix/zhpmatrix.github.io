---
layout: post
title: "[LeetCode]设计题目"
excerpt: ""
date: 2020-01-21 18:53:00
mathjax: true
---

#### 1.[最小栈](https://leetcode-cn.com/problems/min-stack/submissions/)

相关题目有：[最大栈](https://leetcode-cn.com/problems/max-stack/)

#### 2.[用队列实现栈](https://leetcode-cn.com/problems/implement-stack-using-queues/submissions/)

队列和栈的互相实现，都可以基于列表来实现。印象中HanLP的基础数据结构实现使用了大量列表。

相关题目有：[用栈实现队列](https://leetcode-cn.com/problems/implement-queue-using-stacks/submissions/)

#### 3.[设计哈希映射](https://leetcode-cn.com/problems/design-hashmap/submissions/)

最简单的一个思路：用两个列表，分别存储key和value。关于python的list如何删除一个元素，可以参考[这里](https://www.cnblogs.com/xiaodai0/p/10564956.html) ，删除可以基于内容，也可以基于位置。

#### 4.[设计哈希集合](https://leetcode-cn.com/problems/design-hashset/submissions/)

简单思路：一个列表

#### 5.[日志速率限制器](359)

题目描述如下：

请你设计一个日志系统，可以流式接收日志以及它的时间戳。

该日志会被打印出来，需要满足一个条件：当且仅当日志内容在过去的10秒钟内没有被打印过。

给你一条日志的内容和它的时间戳（粒度为秒级），如果这条日志在给定的时间戳应该被打印出来，则返回 true，否则请返回 false。

要注意的是，可能会有多条日志在同一时间被系统接收。

示例如下：

```
Logger logger = new Logger();

// 日志内容 "foo" 在时刻 1 到达系统
logger.shouldPrintMessage(1, "foo"); returns true; 

// 日志内容 "bar" 在时刻 2 到达系统
logger.shouldPrintMessage(2,"bar"); returns true;

// 日志内容 "foo" 在时刻 3 到达系统
logger.shouldPrintMessage(3,"foo"); returns false;

// 日志内容 "bar" 在时刻 8 到达系统
logger.shouldPrintMessage(8,"bar"); returns false;

// 日志内容 "foo" 在时刻 10 到达系统
logger.shouldPrintMessage(10,"foo"); returns false;

// 日志内容 "foo" 在时刻 11 到达系统
logger.shouldPrintMessage(11,"foo"); returns true;
```
直接翻译题目的代码如下：

```
class Logger:
	def __init__(self):
		from collections import defaultdict
		self.logs = defaultdict(set)
	def shouldPrintMessage(self, timestamp, message):
		for i in rnage(tmestamp - 9, timestamp + 1):
			if message in self.logs[i]:
				return False
		self.logs[timestamp].add(message)
		return True
```
6.[迭代压缩字符串](604)

题目描述如下：

对于一个压缩字符串，设计一个数据结构，它支持如下两种操作： next 和 hasNext。

给定的压缩字符串格式为：每个字母后面紧跟一个正整数，这个整数表示该字母在解压后的字符串里连续出现的次数。

next() - 如果压缩字符串仍然有字母未被解压，则返回下一个字母，否则返回一个空格。 hasNext() - 判断是否还有字母仍然没被解压。

**注意：**请记得将你的类在 StringIterator中初始化 ，因为静态变量或类变量在多组测试数据中不会被自动清空。

一种解题思路，参考[这里](https://aisky.men/problem/leetcode/LeetCode-604.%20%E8%BF%AD%E4%BB%A3%E5%8E%8B%E7%BC%A9%E5%AD%97%E7%AC%A6%E4%B8%B2.html)。

7.[数据流中的第K大元素](https://leetcode-cn.com/problems/kth-largest-element-in-a-stream/solution/python-3xing-er-fen-otlogn-4-xing-dui-otlogk-by-qq/)

8.[添加与搜索单词-数据结构设计](https://leetcode-cn.com/problems/add-and-search-word-data-structure-design/)

9.[二叉搜索树迭代器](2020-01-22-system-design.md)

基本思路：解决类似设计题的一种思路是通过遍历树结构，将树中的值存储到列表中，通过对列表的操作实现特定的函数。

10.[顶端迭代器](https://leetcode-cn.com/problems/peeking-iterator/submissions/)

基本思路：将iterator中的数据扁平化。

11.[添加和搜索单词-数据结构设计](https://leetcode-cn.com/problems/add-and-search-word-data-structure-design/submissions/)