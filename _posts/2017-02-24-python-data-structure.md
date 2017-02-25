---
layout: post
title: "[Python]深入理解数据结构"
excerpt: "python中数据结构的理解和应用。"
date: 2017-02-24 12:00:00
---

python有四种内置数据结构和其他高级数据结构，其中四种内置数据结构是列表(list), 元组(tuple), 字典(dict), 集合(set)。

**重要声明：一定要要注意deep copy和shallow copy!此处是大坑！**

list的内部实现是动态数组，存在的问题是当长度增加的时候，需要开辟新的空间，同时进行容器元素的复制移动。当然，在插入和删除元素的时候，被插入和删除元素后继元素也要进行移动。故当需要在容器头部和尾部添加删除元素的时候，可以考虑使用**collections.deque**来替代，据说deque的底层实现逻辑就是list。

比如，几个典型的时间复杂度：len是O(1),min和max是O(n),sort是O(nlogn),delete是O(n)等。

deque是双端队列，内部实现是双向链表。注意是数组链表而不是对象链表，这样可以有更高的效率。显然，双端队列在两端进行操作的时候，具有较高的效率，而对中间元素进行操作，效率较低。

比如，几个典型的时间复杂度：append,appendleft,pop,popleft都是O(1),rotate和remove都是   O(n)等。注意，deque是线程安全的，可以同时从deque集合的左边和右边进行操作而不会有影响。

set的几个操作的时间复杂度通常与集合的长度有关。举个例子，差集操作(set1 - set2), 则时间复杂度为O(len(set1))。

dict是字典，hash结构的时间复杂度通常是O(1)。和list一样，字典存储的也是对象的引用。

参考：

1.[python中的高级数据结构](http://blog.jobbole.com/65218/)

2.[org给出的内置数据结构时间复杂度](https://wiki.python.org/moin/TimeComplexity)

3.[OrderedDict](https://docs.python.org/3/library/collections.html#collections.OrderedDict)

